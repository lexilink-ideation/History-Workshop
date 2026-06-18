# How to Generate Lessons from a PDF

No API key needed. Claude in Cowork handles the lesson generation.

## Setup (one time only)

```bash
pip3 install pdfminer.six
```

## Step 1 — Run the script

```bash
cd ~/Claude/Projects/History\ ESL\ workshop
python3 generate_lessons.py
```

## Step 2 — Drop a PDF into the `input/` folder

The script will automatically extract all chapters and save them as `.txt` files in the `extracted/` folder.

## Step 3 — Ask Claude to generate the lessons

Once the text is extracted, just tell Claude in Cowork:

> "Generate lessons for Chapter 16 from the extracted text."

Claude will read the `.txt` file and build the 7 HTML lesson files (`ch16-a.html` through `ch16-g.html`) directly in your project folder — no API key required.

## File structure

```
History ESL workshop/
├── input/                  ← drop PDFs here
│   └── processed/          ← PDFs move here after extraction
├── extracted/              ← chapter .txt files appear here
├── ch15-a.html … ch15-g.html   ← Chapter 15 lessons (done)
├── ch16-a.html … ch16-g.html   ← Chapter 16 lessons (generated)
├── generate_lessons.py     ← the extraction script
└── HOW_TO_USE.md
```
