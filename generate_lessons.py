#!/usr/bin/env python3
"""
Lexilink History Workshop — PDF Chapter Extractor
==================================================
Drop a PDF (one chapter of Story of the World) into the `input/` folder.
This script extracts the chapter text and saves it as a .txt file,
ready for Claude (in Cowork) to generate the lesson HTML files.

Usage:
  1. Install the one dependency:
       pip3 install pdfminer.six
  2. Run:
       python3 generate_lessons.py
  3. Drop a chapter PDF into the input/ folder.
  4. Tell Claude: "Generate lessons for Chapter X from the extracted text."

No API key needed — Claude in Cowork handles the lesson generation.
"""

import re
import sys
import time
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
INPUT_DIR  = SCRIPT_DIR / "input"
OUTPUT_DIR = SCRIPT_DIR / "extracted"
DONE_DIR   = SCRIPT_DIR / "input" / "processed"

ORDINAL_MAP = {
    "ONE":1,"TWO":2,"THREE":3,"FOUR":4,"FIVE":5,"SIX":6,"SEVEN":7,
    "EIGHT":8,"NINE":9,"TEN":10,"ELEVEN":11,"TWELVE":12,"THIRTEEN":13,
    "FOURTEEN":14,"FIFTEEN":15,"SIXTEEN":16,"SEVENTEEN":17,"EIGHTEEN":18,
    "NINETEEN":19,"TWENTY":20,"TWENTY-ONE":21,"TWENTY-TWO":22,
    "TWENTY-THREE":23,"TWENTY-FOUR":24,"TWENTY-FIVE":25,
}


def install_pdfminer():
    try:
        from pdfminer.high_level import extract_text
        return extract_text
    except ImportError:
        import subprocess
        print("[setup] Installing pdfminer.six...")
        subprocess.check_call([sys.executable, "-m", "pip3", "install",
                               "pdfminer.six", "-q"])
        from pdfminer.high_level import extract_text
        return extract_text


def extract_all_chapters(pdf_path: Path, extract_text) -> list[dict]:
    """Extract all chapters from the PDF as a list of dicts."""
    print(f"  Reading PDF... (this may take a moment)")
    full = extract_text(str(pdf_path))

    pattern = re.compile(
        r'CHAPTER\s+(ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|'
        r'ELEVEN|TWELVE|THIRTEEN|FOURTEEN|FIFTEEN|SIXTEEN|SEVENTEEN|'
        r'EIGHTEEN|NINETEEN|TWENTY(?:[-–]\w+)?|\d+)',
        re.IGNORECASE
    )
    matches = list(pattern.finditer(full))
    if not matches:
        raise ValueError("No chapter markers (CHAPTER ONE, CHAPTER TWO, etc.) found in PDF.")

    chapters = []
    for idx, m in enumerate(matches):
        start = m.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(full)
        text = full[start:end].strip()

        word = m.group(1).upper()
        num = ORDINAL_MAP.get(word) or (int(word) if word.isdigit() else None)

        # Title = first meaningful non-chapter line
        title = ""
        for line in text.split("\n")[1:6]:
            line = line.strip()
            if line and not line.upper().startswith("CHAPTER"):
                title = line
                break

        chapters.append({"number": num, "title": title, "text": text})

    return chapters


def process_pdf(pdf_path: Path):
    extract_text = install_pdfminer()

    print(f"\n{'='*55}")
    print(f"PDF: {pdf_path.name}")
    print("="*55)

    try:
        chapters = extract_all_chapters(pdf_path, extract_text)
    except Exception as e:
        print(f"✗ Error: {e}")
        return

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"\nFound {len(chapters)} chapters:\n")
    for ch in chapters:
        label = f"Chapter {ch['number']}: {ch['title']}"
        out_file = OUTPUT_DIR / f"chapter_{ch['number']:02d}.txt"
        out_file.write_text(ch["text"], encoding="utf-8")
        size = len(ch["text"])
        print(f"  ✓ {label:<40} → {out_file.name}  ({size:,} chars)")

    DONE_DIR.mkdir(parents=True, exist_ok=True)
    dest = DONE_DIR / pdf_path.name
    shutil.move(str(pdf_path), str(dest))

    print(f"""
✅ Done! Extracted {len(chapters)} chapters to:
   {OUTPUT_DIR}

Next step — tell Claude in Cowork:
   "Generate lessons for Chapter 16 from the extracted text."
   (Claude will read the .txt file and build the HTML lessons.)
""")


# ─── Folder watcher ──────────────────────────────────────────────────────────

def run_watcher():
    try:
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler
        has_watchdog = True
    except ImportError:
        has_watchdog = False

    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Process any PDFs already sitting in input/
    existing = list(INPUT_DIR.glob("*.pdf"))
    for pdf in existing:
        process_pdf(pdf)

    if not has_watchdog:
        # Fallback: simple polling loop
        print("\n[Watching input/ folder — drop a PDF in to process it]")
        print("Press Ctrl+C to stop.\n")
        seen = {p.name for p in existing}
        try:
            while True:
                for pdf in INPUT_DIR.glob("*.pdf"):
                    if pdf.name not in seen:
                        seen.add(pdf.name)
                        time.sleep(1)
                        process_pdf(pdf)
                time.sleep(2)
        except KeyboardInterrupt:
            print("\nStopped.")
        return

    # Use watchdog if available
    class Handler(FileSystemEventHandler):
        def __init__(self):
            self.seen = set()
        def _handle(self, path):
            p = Path(path)
            if p.suffix.lower() == ".pdf" and p.name not in self.seen:
                self.seen.add(p.name)
                time.sleep(1)
                if p.exists():
                    process_pdf(p)
        def on_created(self, e):
            if not e.is_directory: self._handle(e.src_path)
        def on_moved(self, e):
            self._handle(e.dest_path)

    print("\n╔══════════════════════════════════════════════════════╗")
    print("║  Lexilink — PDF Chapter Extractor (watch mode)      ║")
    print("╠══════════════════════════════════════════════════════╣")
    print(f"║  Watching:  input/                                   ║")
    print(f"║  Output:    extracted/                               ║")
    print("║  Drop a chapter PDF into input/ to extract it.      ║")
    print("║  Press Ctrl+C to stop.                               ║")
    print("╚══════════════════════════════════════════════════════╝\n")

    obs = Observer()
    obs.schedule(Handler(), str(INPUT_DIR), recursive=False)
    obs.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
        print("\nStopped.")
    obs.join()


if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--pdf", help="Process a specific PDF right now")
    args = p.parse_args()

    if args.pdf:
        process_pdf(Path(args.pdf))
    else:
        run_watcher()
