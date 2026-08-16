#!/bin/bash
# Quick Start Script for Hugo Blog
# Usage: ./new-post.sh [lang] <category> <filename>
# Example: ./new-post.sh insights my-docker-guide      (English, default)
#          ./new-post.sh zh insights my-docker-guide   (Chinese)

# Resolve repo root from the script's own location
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Show usage
usage() {
    echo "Usage: $0 [lang] <category> <filename>"
    echo ""
    echo "Languages:"
    echo "  en (default) - content/en, served at /"
    echo "  zh           - content/zh, served at /zh/"
    echo ""
    echo "Categories:"
    echo "  daily        - Timeline / Daily progress"
    echo "  pitfalls     - Lab Notes / Troubleshooting"
    echo "  insights     - Architecture & Deep dives"
    echo "  reflections  - Retrospectives"
    echo "  project-logs - Project build logs"
    echo ""
    echo "Examples:"
    echo "  $0 insights docker-networking-deep-dive"
    echo "  $0 zh pitfalls wsl-flashing-failure"
    exit 1
}

# Check arguments
if [ $# -lt 2 ]; then
    usage
fi

# Optional leading language argument
LANG_CODE="en"
if [ $# -ge 3 ]; then
    LANG_CODE=$1
    shift
fi

case $LANG_CODE in
    en|zh)
        ;;
    *)
        echo "Error: Invalid language '$LANG_CODE' (expected en or zh)"
        exit 1
        ;;
esac

CATEGORY=$1
FILENAME=$2

# Validate category
case $CATEGORY in
    daily|pitfalls|insights|reflections|project-logs)
        ;;
    *)
        echo "Error: Invalid category '$CATEGORY'"
        echo "Valid categories: daily, pitfalls, insights, reflections, project-logs"
        exit 1
        ;;
esac

cd "$PROJECT_DIR"

# `hugo new` always targets the default language's contentDir when languages
# use per-language contentDir, so we instantiate the archetype manually.
SRC="archetypes/$CATEGORY.md"
DEST="content/$LANG_CODE/$CATEGORY/$FILENAME.md"

if [ ! -f "$SRC" ]; then
    SRC="archetypes/default.md"
fi

if [ -f "$DEST" ]; then
    echo "Error: $DEST already exists"
    exit 1
fi

echo -e "${YELLOW}Creating new $LANG_CODE post in $CATEGORY...${NC}"
mkdir -p "$(dirname "$DEST")"

TITLE=$(echo "$FILENAME" | tr '-' ' ' | sed -e "s/\b\(.\)/\u\1/g")
DATE=$(date +%Y-%m-%dT%H:%M:%S%:z)

sed -e "s#{{ \.Date }}#$DATE#g" \
    -e "s#{{ replace \.File\.ContentBaseName \"-\" \" \" | title }}#$TITLE#g" \
    "$SRC" > "$DEST"

FILE_PATH="$DEST"

if [ -f "$FILE_PATH" ]; then
    echo -e "${GREEN}Success!${NC} Created: $FILE_PATH"
    echo ""
    echo "File content preview:"
    echo "---"
    head -20 "$FILE_PATH"
    echo "---"
    echo ""
    echo "Edit the file: code $FILE_PATH"
else
    echo "Error: Failed to create post"
    exit 1
fi
