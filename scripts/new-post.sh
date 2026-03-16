#!/bin/bash
# Quick Start Script for Hugo Blog
# Usage: ./new-post.sh <category> <filename>
# Example: ./new-post.sh insights my-docker-guide

PROJECT_DIR="c:/Users/li/adlink8.github.io"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Show usage
usage() {
    echo "Usage: $0 <category> <filename>"
    echo ""
    echo "Categories:"
    echo "  daily        - Timeline / Daily progress"
    echo "  pitfalls     - Lab Notes / Troubleshooting"
    echo "  insights     - Architecture & Deep dives"
    echo "  reflections  - Retrospectives"
    echo "  project-logs - Project build logs"
    echo ""
    echo "Example:"
    echo "  $0 insights docker-networking-deep-dive"
    exit 1
}

# Check arguments
if [ $# -lt 2 ]; then
    usage
fi

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

# Create the post
echo -e "${YELLOW}Creating new post in $CATEGORY...${NC}"
hugo new "$CATEGORY/$FILENAME.md"

# Get the file path
FILE_PATH="content/$CATEGORY/$FILENAME.md"

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
