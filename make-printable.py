#!/usr/bin/env python3
"""Build printable fold-over flashcards (PDF) from the Anki TSVs.

One PDF per officer, in ritual order so the sheets can be checked against
the script before they are cut. Cards carry no sequence numbers: once cut
they are meant to be shuffled and drilled in random order, so that a line
can be produced from its cue alone rather than recited as a sequence.

Layout: 4 cards per Letter sheet, 2x2. Each cell is one card, unfolded.
The lower half holds the cue and prints upright; the upper half holds the
line and prints rotated 180. Cut the grid, fold the top half backward
along the dashed line, and the line lands on the back of the cue, upright.
Single-sided printing throughout -- no duplex alignment to get wrong.

Type is set to large-print standards (see CUE_PT / LINE_PT).

Also refreshes the provenance block on docs/print.md -- the bit between the
provenance:start/end markers -- so the page always records which script and
which spreadsheets the PDFs on it were built from, and when. Everything
outside those markers is hand-written prose; the script never touches it.

Usage:  python3 make-printable.py [--out DIR]
Needs Google Chrome for the HTML->PDF step; no other dependencies.
"""

import argparse
import glob
import html
import os
import re
import shutil
import signal
import subprocess
import sys
import time
from datetime import date
import tempfile

# --- Type, in points. Large-print convention is a 16pt floor; 18pt is the
# recommendation. The line is the thing being recalled, so it is never the
# part that shrinks -- only an overlong cue steps down, and not below 14.
LINE_PT = 19
CUE_PT = 17
CUE_MIN_PT = 14
CUE_STEP_CHARS = 130  # every this many characters past the first, step down 1pt

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

PAGE = "docs/print.md"
MARK_START = "<!-- provenance:start -->"
MARK_END = "<!-- provenance:end -->"

# Fallback only. The real value is read from the *From: line of the local
# *_prepared.md files when they're present; a fresh clone doesn't have them.
SCRIPT_VERSION = ("0=0 Opening the Hall of the Neophytes "
                  "\u2014 Het Iteru Redaction v1.0, August 2026")

# Officers in ritual precedence, matching the deck numbering.
ORDER = ["Dadouchos", "Stolistes", "Kerux", "Hegemon", "Hiereus", "All"]

OFFICER_RE = re.compile(r"^Anki_Neophyte_(.+)\.tsv$")
FROM_RE = re.compile(r"^\*From:\s*(.+?)\*\s*$", re.M)
SECTION_RE = re.compile(r"::\d+\.\s*([^:]+)$")


def read_tsv(path):
    """Yield (cue, line, section) for each card row, skipping directives."""
    with open(path, encoding="utf-8") as fh:
        for raw in fh:
            if raw.startswith("#"):
                continue
            row = raw.rstrip("\n").split("\t")
            if len(row) < 2 or not row[0].strip() or not row[1].strip():
                continue
            deck = row[2] if len(row) > 2 else ""
            m = SECTION_RE.search(deck)
            section = m.group(1).replace("_", " ") if m else ""
            yield row[0].strip(), row[1].strip(), section


def cue_size(cue):
    """Step the cue down a point per CUE_STEP_CHARS of overflow, to a floor."""
    plain = re.sub(r"<[^>]+>", "", cue)
    over = max(0, len(plain) - CUE_STEP_CHARS)
    return max(CUE_MIN_PT, CUE_PT - (over // 45))


def card_html(cue, line, section, officer):
    tag = html.escape(" · ".join(p for p in (officer, section) if p))
    return f"""
    <div class="cell">
      <div class="half line"><div class="inner"><p>{line}</p></div></div>
      <div class="fold"></div>
      <div class="half cue"><div class="inner">
        <p style="font-size:{cue_size(cue)}pt">{cue}</p>
        <span class="tag">{tag}</span>
      </div></div>
    </div>"""


CSS = f"""
@page {{ size: Letter; margin: 0.25in; }}
* {{ box-sizing: border-box; }}
body {{
  margin: 0;
  font-family: "Atkinson Hyperlegible", Verdana, Tahoma, sans-serif;
  color: #000; background: #fff;
}}
.sheet {{
  display: grid;
  grid-template-columns: 4in 4in;
  grid-auto-rows: 5.25in;
  page-break-after: always;
}}
.sheet:last-child {{ page-break-after: auto; }}
.cell {{
  width: 4in; height: 5.25in;
  border: 1px dashed #bbb;      /* cut line */
  display: flex; flex-direction: column;
  overflow: hidden;
}}
.half {{ height: 2.625in; display: flex; padding: 0.22in 0.24in; position: relative; }}
.half .inner {{ margin: auto; width: 100%; }}
.line .inner {{ transform: rotate(180deg); }}
.fold {{
  position: absolute;           /* drawn by .cell::after instead */
}}
.cell {{ position: relative; }}
.cell::after {{
  content: ""; position: absolute; left: 0; right: 0; top: 50%;
  border-top: 1px dotted #ddd;  /* fold line */
}}
p {{
  margin: 0;
  line-height: 1.34;
  text-align: left;             /* ragged right; justified text hurts legibility */
  hyphens: none;
  overflow-wrap: break-word;
}}
.line p {{ font-size: {LINE_PT}pt; font-weight: 600; }}
.cue p  {{ font-weight: 400; }}
.cue .tag {{
  position: absolute; left: 0.24in; bottom: 0.12in;
  font-size: 8pt; letter-spacing: 0.04em; color: #999;
}}
b {{ font-weight: 700; }}
i {{ font-style: italic; }}
"""


def build_html(officer, cards):
    cells = [card_html(c, l, s, officer) for c, l, s in cards]
    sheets = []
    for i in range(0, len(cells), 4):
        sheets.append('<div class="sheet">' + "".join(cells[i:i + 4]) + "</div>")
    return (
        "<!doctype html><html><head><meta charset='utf-8'>"
        f"<title>{html.escape(officer)} cards</title><style>{CSS}</style>"
        "</head><body>" + "".join(sheets) + "</body></html>"
    )


def to_pdf(html_path, pdf_path, timeout=90):
    """Render with headless Chrome.

    Chrome 153 writes the PDF and then doesn't exit, so waiting on the
    process hangs forever. Wait for the file to be written and settle
    instead, then stop the process ourselves. The throwaway profile keeps
    it from blocking on the lock held by a normal Chrome window.
    """
    if os.path.exists(pdf_path):
        os.unlink(pdf_path)
    with tempfile.TemporaryDirectory() as profile:
        proc = subprocess.Popen(
            [CHROME, "--headless", "--disable-gpu", "--no-first-run",
             f"--user-data-dir={profile}", "--no-pdf-header-footer",
             f"--print-to-pdf={pdf_path}", f"file://{html_path}"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True,   # its own group, so we can reap the children too
        )
        try:
            deadline = time.time() + timeout
            size = -1
            while time.time() < deadline:
                if proc.poll() is not None and os.path.exists(pdf_path):
                    break                      # exited on its own; older Chrome
                if os.path.exists(pdf_path):
                    now = os.path.getsize(pdf_path)
                    # Same size two polls running, and a complete trailer.
                    if now > 0 and now == size and pdf_complete(pdf_path):
                        break
                    size = now
                time.sleep(0.4)
            else:
                raise RuntimeError(f"Chrome never finished {pdf_path}")
        finally:
            # Kill the whole group. Chrome's renderer children outlive a
            # terminate() on the parent, and the stragglers make the next
            # card's render hang.
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except (ProcessLookupError, PermissionError):
                pass
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                pass

    if not pdf_complete(pdf_path):
        raise RuntimeError(f"Incomplete PDF written to {pdf_path}")


def pdf_complete(path):
    """A PDF that starts with the header and carries its end marker."""
    try:
        with open(path, "rb") as fh:
            if fh.read(5) != b"%PDF-":
                return False
            fh.seek(max(0, os.path.getsize(path) - 2048))
            return b"%%EOF" in fh.read()
    except OSError:
        return False



def script_version(root):
    """Read the redaction from the local prepared scripts, if they're here."""
    for path in sorted(glob.glob(os.path.join(root, "*_prepared.md"))):
        with open(path, encoding="utf-8") as fh:
            m = FROM_RE.search(fh.read(2000))
        if m:
            return m.group(1).strip()
    return SCRIPT_VERSION


def tsv_provenance(root, path):
    """Last commit touching this spreadsheet, as (date, short sha)."""
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%ad|%h", "--date=format:%d %B %Y",
             "--", os.path.basename(path)],
            cwd=root, capture_output=True, text=True, check=True).stdout.strip()
        if out:
            d, sha = out.split("|")
            return d, sha
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        pass
    return "uncommitted", ""


def write_provenance(root, rows, out_rel):
    """Refresh the managed block on the print page, leaving the prose alone."""
    page = os.path.join(root, PAGE)
    if not os.path.exists(page):
        print(f"note: {PAGE} not found, skipping provenance block")
        return
    with open(page, encoding="utf-8") as fh:
        text = fh.read()
    if MARK_START not in text or MARK_END not in text:
        print(f"note: no provenance markers in {PAGE}, leaving it alone")
        return

    lines = [
        MARK_START,
        "",
        f"Generated from the *{script_version(root)}*.",
        "",
        "| Officer | Cards | Sheets |",
        "| --- | ---: | ---: |",
    ]
    for officer, count, sheets, pdf, when, sha in rows:
        lines.append(f"| [{officer}]({out_rel}/{pdf}) | {count} | {sheets} |")
    # Which spreadsheet each PDF came from is for the maintainer, not the
    # people printing, so it goes in a comment: hidden on the published page,
    # visible when editing the Markdown.
    lines += ["", "<!--",
              f"Built {date.today().strftime('%d %B %Y').lstrip('0')}.",
              "Spreadsheet last changed:"]
    for officer, count, sheets, pdf, when, sha in rows:
        lines.append(f"  {officer:<10} {when} {sha}".rstrip())
    lines += ["-->", "", MARK_END]

    head = text.split(MARK_START)[0]
    tail = text.split(MARK_END)[1]
    with open(page, "w", encoding="utf-8") as fh:
        fh.write(head + "\n".join(lines) + tail)
    print(f"{'provenance':<12}  -> {page}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="docs/files/print")
    ap.add_argument("--only", help="build just this officer")
    ap.add_argument("--keep-html", action="store_true")
    args = ap.parse_args()

    root = os.path.dirname(os.path.abspath(__file__))
    os.makedirs(os.path.join(root, args.out), exist_ok=True)

    rows = []
    paths = sorted(glob.glob(os.path.join(root, "Anki_Neophyte_*.tsv")),
                   key=lambda p: ORDER.index(OFFICER_RE.match(os.path.basename(p)).group(1))
                   if OFFICER_RE.match(os.path.basename(p)).group(1) in ORDER else 99)
    for path in paths:
        officer = OFFICER_RE.match(os.path.basename(path)).group(1)
        if args.only and args.only.lower() != officer.lower():
            continue
        cards = list(read_tsv(path))
        if not cards:
            continue

        page = build_html(officer, cards)
        pdf_name = f"Neophyte-{officer}-cards.pdf"
        out_pdf = os.path.join(root, args.out, pdf_name)
        if args.keep_html:
            html_path = os.path.join(root, args.out, f"{officer}.html")
            with open(html_path, "w", encoding="utf-8") as fh:
                fh.write(page)
        else:
            fd, html_path = tempfile.mkstemp(suffix=".html")
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                fh.write(page)
        to_pdf(html_path, out_pdf)
        if not args.keep_html:
            os.unlink(html_path)
        sheets = -(-len(cards) // 4)
        when, sha = tsv_provenance(root, path)
        rows.append((officer, len(cards), sheets, pdf_name, when, sha))
        print(f"{officer:<12} {len(cards):>3} cards  {sheets:>3} sheets  -> {out_pdf}")

    if rows and not args.only:
        # Links on the page are relative to docs/, where the page lives.
        write_provenance(root, rows, os.path.relpath(args.out, "docs"))


if __name__ == "__main__":
    if not os.path.exists(CHROME):
        sys.exit("Google Chrome not found; needed to render the PDF.")
    main()
