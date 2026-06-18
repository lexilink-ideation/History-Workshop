---
name: history-lesson-generator
description: Generate ESL lesson HTML files from a chapter PDF dropped into the input folder
---

You are generating ESL history lessons for the Lexilink Ideation IELTS STUDIO History Workshop site.

**Your job:** Check the input folder for a PDF, extract the chapter text, read `index.html` to find how many lessons the chapter should have, then write that exact number of complete HTML lesson files into the project folder.

## Step 1 — Find the PDF

Check `/Users/yichen/Claude/Projects/History ESL workshop/input/` for any `.pdf` files (exclude the `processed/` subfolder). If none found, reply: "No PDF found in input/ — drop a chapter PDF there and click Run again."

## Step 2 — Extract chapter text and detect chapter number

Use bash with pdfminer to extract the chapter text:
```python
from pdfminer.high_level import extract_text
import re
text = extract_text("PATH_TO_PDF")
# Detect chapter number from "CHAPTER SIXTEEN" / "CHAPTER 16" / "Unit 16" etc.
# Identify: chapter number (as integer), chapter title, all section headings and content
```

## Step 3 — Read index.html to find the lesson list

Parse `/Users/yichen/Claude/Projects/History ESL workshop/index.html` to find the entry for this chapter number. Extract the array of lesson names.

Use bash/python to do this — look for the pattern:
```
{ n:16, title:"...", lessons:["Lesson One Name","Lesson Two Name","Review + Project"] }
```

The lesson names in this array are the **authoritative** lesson titles. Generate exactly this many HTML files (one per lesson name, in order). The last lesson is always the Review + Project lesson.

**Example:** If index.html shows `lessons:["Ashurbanipal's Attack","The Library of Nineveh","Review + Project"]` for chapter 16, generate 3 files: ch16-a.html, ch16-b.html, ch16-c.html.

File naming: ch{N}-a.html, ch{N}-b.html, ch{N}-c.html … up to the letter matching the lesson count (a=1, b=2, c=3, d=4, e=5, f=6, g=7).

## Step 4 — Plan lessons

Map each lesson name from the index to a section of the chapter text, in narrative order. For all lessons except the last:
- Assign a subtitle that expands on the lesson name
- Identify the key content, vocabulary, and grammar focus

For the **last lesson** (Review + Project):
- It covers the full chapter — both narrative sections
- Its story section is a complete chapter recap
- Its Review tab (section 10) uses the special full-chapter format (see Step 5)

## Step 5 — Generate all HTML files

Write files into `/Users/yichen/Claude/Projects/History ESL workshop/`.

**Each HTML file must be complete and self-contained** with inline CSS and JS. Follow this EXACT structure — use `/Users/yichen/Claude/Projects/History ESL workshop/ch15-a.html` as the CSS/layout template and `/Users/yichen/Claude/Projects/History ESL workshop/ch16-c.html` as the model for the Review + Project lesson.

Every lesson has 10 sections (scroll-based, not tabs):

1. **Vocab** — 10 vocabulary cards (click to expand). Each card: word, part of speech, IPA pronunciation, Chinese translation (汉字), definition in simple English, example sentence from the story.

2. **Story** — 400–500 word narrative based on the lesson's section of chapter text, written for ESL A2–B1 learners. Use emoji scene-setters, bold key vocabulary words (`.story-hl`), paragraph breaks, and one `.story-box` pull-quote.

3. **Reading Comprehension** — 6 questions mixing multiple-choice (`mcq`) and True/False (`tf`) with instant feedback.

4. **Grammar** — 3 grammar points arising naturally from the story. Each in a `.grammar-box` with label, rule, and 3–4 `.grammar-eg` examples.

5. **Sentence Builder** — 4 exercises: 2 fill-in-blank, 1 unscramble, 1 Chinese→English translation. Use `checkFill`, `checkUnscramble`, and `revealFill` JS functions.

6. **Speaking 1** — 🟢 3 one-sentence prompts with starter phrases.

7. **Speaking 2** — 🟡 2 multi-sentence prompts + 🔵 1 opinion/debate question.

8. **Ideas & Society** — 4 deep-thinking questions in `.idea-q` cards with emoji.

9. **IELTS Content Builder** — IELTS topic banner, vocab chips, collocations, 3 speaking questions, Task 2 writing prompt.

10. **Review**
    - **For all lessons except the last:** 8 `.star-word` chips + `.think-box` big idea + 3 `.mini-quiz-q` questions.
    - **For the last (Review + Project) lesson only:** dark summary box with full chapter recap → all chapter star words (every word from all lessons) → big idea box → amber project box with 5 numbered steps → 3 final quiz questions.

**CSS and JS:** Copy exactly from ch15-a.html. Do not change variable names or class names.

**Navigation links:**
- Lesson A's prev link → the previous chapter's final lesson (e.g. `ch15-g.html`) or `index.html` if unknown.
- Each lesson's next link → the next lesson file in sequence.
- The last lesson's next link → `https://lexilink-ideation.github.io/History-Workshop/`.

**Hero gradient:** Vary the hero background gradient colour per lesson to make each feel distinct:
- Lesson A: warm orange/amber tones (`#1A0A00 → #3D1800 → #5A2500`)
- Lesson B: cool blue/navy tones (`#000D1A → #001F3F → #003366`)
- Lesson C (Review): green/teal tones (`#0D1A00 → #1A3300 → #2A5200`)
- Lesson D onwards: vary freely (purple, crimson, etc.)

**Progress bar label:** Show "Lesson {16A} of {3}" using the actual chapter number and total lesson count.

## Step 6 — Move the PDF

After all files are written, move the PDF from `input/` to `input/processed/` using bash.

## Step 7 — Update index.html

Edit `/Users/yichen/Claude/Projects/History ESL workshop/index.html` to activate the new chapter.

Find the chapter N entry. It will look like one of these two forms:

**Form A (simple strings — needs upgrading):**
```
{ n:16, title:"...", lessons:["Lesson One","Lesson Two","Review + Project"] },
```

**Form B (already expanded but not live):**
```
{ n:16, title:"...", lessons:[
  { name:"Lesson One", file:"ch16-a.html" },
  ...
] },
```

Replace whichever form is present with the fully expanded, live format:
```
{ n:16, title:"The Return of Assyria",
  lessons:[
    { name:"Ashurbanipal's Attack",  file:"ch16-a.html", live:true },
    { name:"The Library of Nineveh", file:"ch16-b.html", live:true },
    { name:"Review + Project",       file:"ch16-c.html", live:true },
  ],
  progress: 0, live: true },
```

Use the actual chapter number, title, lesson names, and filenames for the chapter you just generated. File names follow the pattern ch{N}-a.html, ch{N}-b.html, etc.

## Step 8 — Git commit and push

Run the following bash commands to commit and deploy everything to GitHub Pages:

```bash
cd "/Users/yichen/Claude/Projects/History ESL workshop"
git add ch{N}-a.html ch{N}-b.html ... index.html
git commit -m "Add Chapter {N} lessons ({Chapter Title})"
git push
```

Replace `{N}` with the actual chapter number and list all generated HTML files. If `git push` fails due to authentication, report the error and ask the user to push manually.

## Step 9 — Report

List all files created, confirm the index was updated, and confirm the git push succeeded (or report any error).
