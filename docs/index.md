---
layout: default
title: Neophyte flashcards for Anki — Getting Started
description: Anki flashcards to help OSOGD officers memorize their Neophyte ritual lines.
---

# Neophyte flashcards for Anki — Getting Started

This package contains Anki flashcards for the Neophyte ritual as performed by the [Open Source Order of the Golden Dawn](https://en.wikipedia.org/wiki/Open_Source_Order_of_the_Golden_Dawn). The package is intended for OSOGD members, and particularly for those who hold officer roles and need to memorize their lines.  

<a href="files/Neophyte-OSOGD-latest.apkg" class="btn" download>Download the Neophyte deck</a>

## What is Anki?

Anki is a flashcard program for computers and mobile devices. Instead of reviewing all the material every time, you put aside the items you already know for a while, and then review them only when you're about to forget them. The act of deliberately remembering something you almost forgot fixes it in your memory.  

## What's in these flashcards?

The Anki flashcard package for the Neophyte grade is a single file with virtual decks for each officer. Each officer's deck has subsections for each part of the ritual, so you can further focus your study on a section like the initiation or your opening speech. The subsections for each officer are numbered so they'll show up in ritual order in the deck. Subsections for some officers skip numbers if that officer has no speaking lines in a section.

The deck labelled "All" includes the lines everyone says in unison, and does not mean all the lines for every officer.

## How to use it

To use the Anki Neophyte flashcards, you need to install the Anki software on your computer or mobile device.  

### 1. Install Anki (one time)

Find links to all official versions at the [AnkiWeb Downloads page](https://apps.ankiweb.net/#downloads).

- **iPhone / iPad** — **AnkiMobile** $25 one time. Follow the link from the [official AnkiWeb Downloads page](https://apps.ankiweb.net/docs/AnkiMobile#downloads) to avoid copycats.
- **Android** — **AnkiDroid** Free. Follow the link from the [official AnkiWeb Downloads page](https://apps.ankiweb.net/#downloads).
- **Mac / Windows / Linux** Free. Follow the link from the [official AnkiWeb Downloads page](https://apps.ankiweb.net/#downloads).

### 2. Load the deck

<a href="files/Neophyte-OSOGD-latest.apkg" class="btn" download>Download the Neophyte deck</a>

**iPhone / iPad**

1. Tap **Download the Neophyte deck**.
2. Tap **Download** when your browser asks.
3. Tap the downloaded file. Anki opens and asks to import. Say yes.

**Android**

1. Tap **Download the Neophyte deck**.
2. Open the downloaded file. 
3. AnkiDroid opens and asks to confirm the import. Tap OK.

**Computer**

1. Click **Download the Neophyte deck**.
2. Open the downloaded file. 
3. Anki opens and asks to import. Say yes.

After import, you'll see a **Neophyte** deck with subdecks for each officer (Dadouchos, Stolistes, Kerux, Hegemon, Hiereus) plus **All** for the group-unison lines. The decks are numbered (`01. Dadouchos`, `02. Stolistes`, etc.) so they show up in ritual order rather than alphabetically.

### 3. Study your lines

- Tap any deck to start studying. For example, `Neophyte::03. Kerux` gives you everything for that officer. Tap a subsection like `Neophyte::03. Kerux::02. officers` to study your lines for your opening speech.
- Each card shows a **cue** on the front, the line spoken just before yours. If you have a multi-line speech, the cue might be your own previous line.
- Tap **Show Answer**.
- Rate yourself: **Again / Hard / Good / Easy**. Anki uses your rating to schedule the next review.
- **A little every day** works best. If you need to cram before the ritual, you may need to turn on special study mode in Anki, because it's designed not to overwhelm you with too much new content at once.

## Feedback

I welcome your feedback for how I might improve this study aid. This is an evolving project, so there will surely be room for improvement. I would particularly like to hear if you get stuck setting up for the first time, if the cards don't work, or if there are errors or missing lines. Breaking down the script into flashcards was a fairly laborious process with a number of judgement calls. If this Neophyte deck proves useful and popular, I will create decks for other grades. Let me know if you'd like to help with that.

## Build on this work or contribute

The flashcard packs and the spreadsheets that I used to generate them are both available in the same GitHub repo where this page is hosted. https://github.com/ak-krajewska/osogd-anki

You can download the spreadsheets and use them to create other study aids as you wish. I am open to contributions from OSOGD members who want to help create cards for other rituals or our study materials. Contact me via our group and I will onboard you.

## Release notes

### Version 2 - September 7, 2026

File: `Neophyte-OSOGD-v2.apkg`

This release updates every deck so it matches the latest Neophyte script, _Opening the Hall of the Neophytes, Het Iteru Redaction v1.0 — August 2026_. This release also introduces a few improvements to the cue/line chunking for the Hiereus and Hegemon decks so the lines are easier to memorize. Previously, the KHABS AM PEKHT KONX OM PAX sections for both Hiereus and Hegemon gave only a single previous word as the cue. Now, the cues are the natural context as you'd experience it in the ritual, giving just "KHABS" for "AM" but "KHABS AM PEKHT" for "KONX" and similar. Previously, the `lengthy_explanations` subsection of the Hiereus deck had rather large chunks as the cue/line pairs as I wanted each line to make sense. In practice, I found them too long to memorize. Now, the chunks are smaller, trading stand-alone sense for smaller bits to memorize.

If you previously downloaded version 1 or 1.1, you must delete your Neophyte deck from the Anki app. Then, load the package again from the link under **2. Load the deck**.

A number of the changes in this release re-organize speeches into different cards rather than editing the existing cards, so if you just import the new deck you will end up with duplicates. If you already updated without deleting first, delete your existing Neophyte deck and then load the latest deck.

### Version 1.1 - August 12, 2026

File: `Neophyte-OSOGD-v1.1.apkg`

This release fixes a bug in the Stolistes deck. Previously, the Stolistes cards showed the cue but no line. No other officer deck was affected. To fix your local version, load the package again from the link under **2. Load the deck**.

### Version 1 - August 8, 2026

File: `Neophyte-OSOGD-v1.apkg`

This is the initial release of the Neophyte study deck and is based on _Opening the Hall of the Neophytes, Het Nuit Redaction V6.0 — April 2026_.

The package contains study decks for the Dadouchos, Stolistes, Kerux, Hegemon, Hiereus, and an "All" deck for lines spoken by everyone in unison. A deck for the Hierophant is not included in this release.
