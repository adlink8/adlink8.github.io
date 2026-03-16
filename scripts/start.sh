#!/bin/bash
# Start Hugo server with auto-restart

PROJECT_DIR="c:/Users/li/adlink8.github.io"
PORT=1313

cd "$PROJECT_DIR"

echo "Starting Hugo server..."
echo "URL: http://localhost:$PORT"
echo "Press Ctrl+C to stop"
echo ""

hugo server -D --port $PORT
