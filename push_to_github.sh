#!/bin/bash
# One-time setup: clones the repo, copies all ch15 files + updated index.html, commits, and pushes.
# Run this once in Terminal: bash ~/Claude/Projects/History\ ESL\ workshop/push_to_github.sh

set -e

REPO="https://github.com/lexilink-ideation/History-Workshop.git"
SRC="$HOME/Claude/Projects/History ESL workshop"
TMP="/tmp/History-Workshop-push"

echo "🔄 Cloning repo..."
rm -rf "$TMP"
git clone "$REPO" "$TMP"

echo "📋 Copying Chapter 15 lesson files..."
cp "$SRC/ch15-a.html" "$TMP/"
cp "$SRC/ch15-b.html" "$TMP/"
cp "$SRC/ch15-c.html" "$TMP/"
cp "$SRC/ch15-d.html" "$TMP/"
cp "$SRC/ch15-e.html" "$TMP/"
cp "$SRC/ch15-f.html" "$TMP/"
cp "$SRC/ch15-g.html" "$TMP/"

echo "📋 Copying updated index.html..."
cp "$SRC/index.html" "$TMP/"

echo "✅ Committing..."
cd "$TMP"
git add ch15-a.html ch15-b.html ch15-c.html ch15-d.html ch15-e.html ch15-f.html ch15-g.html index.html
git commit -m "Add Chapter 15: The Phoenicians (7 lessons)"

echo "🚀 Pushing to GitHub..."
git push origin main

echo ""
echo "✅ Done! Visit https://lexilink-ideation.github.io/History-Workshop/ to see Chapter 15 live."
