#!/bin/bash
# Hugo Server Watchdog Script
# Auto-restart Hugo server if it crashes

PORT=1313
PROJECT_DIR="c:/Users/li/adlink8.github.io"

echo "=== Hugo Server Watchdog Started ==="
echo "Port: $PORT"
echo "Project: $PROJECT_DIR"
echo "Press Ctrl+C to stop"
echo ""

while true; do
    # Check if Hugo is running
    if ! netstat -ano | grep -q ":$PORT.*LISTENING"; then
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Starting Hugo server..."
        
        # Kill any orphaned process on the port
        PID=$(netstat -ano | grep ":$PORT" | awk '{print $5}' | head -1)
        if [ -n "$PID" ] && [ "$PID" != "0" ]; then
            taskkill //F //PID $PID 2>/dev/null
        fi
        
        # Start Hugo server
        cd "$PROJECT_DIR" && hugo server -D --port $PORT &
        HUGO_PID=$!
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] Hugo server started (PID: $HUGO_PID)"
    fi
    
    # Wait before next check
    sleep 5
done
