#!/usr/bin/env bash
# Sync AgentsView telemetry into data/ai_activity.json, then commit & push when it changed.
# Used by the daily Task Scheduler job ("Blog AgentsView Sync") and for manual runs.
# Only data/ai_activity.json is ever staged or committed here — everything else in
# the working tree is left untouched.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"
HUGO="${HUGO_BIN:-/d/ADLINK/Myproject/hugo-bin/hugo.exe}"
LOG="${TEMP:-/tmp}/blog-agentsview-sync.log"

# mkdir-based lock — atomic on both Windows and POSIX. The daily task and the
# logon catch-up can overlap; a lock left behind by a hard kill is taken over
# once it is older than an hour.
LOCK_DIR="${TEMP:-/tmp}/blog-agentsview-sync.lock"
if ! mkdir "$LOCK_DIR" 2>/dev/null; then
    age=$(( $(date +%s) - $(stat -c %Y "$LOCK_DIR" 2>/dev/null || echo 0) ))
    if [ "$age" -lt 3600 ]; then
        echo "another sync instance is running; skip"
        exit 0
    fi
    rmdir "$LOCK_DIR" 2>/dev/null || { echo "cannot take over stale lock; skip"; exit 0; }
    mkdir "$LOCK_DIR" 2>/dev/null || { echo "lost stale-lock race; skip"; exit 0; }
fi
trap 'rmdir "$LOCK_DIR" 2>/dev/null' EXIT

{
    echo "=== $(date '+%F %T') sync start ==="
    if python tools/sync_agentsview.py; then
        echo "data unchanged, nothing to push"
        exit 0
    fi

    git add data/ai_activity.json
    if git diff --cached --quiet -- data/ai_activity.json; then
        echo "no staged change (already committed?)"
        exit 0
    fi

    # never deploy data the site cannot build with
    "$HUGO" --minify > /dev/null

    git commit -m "chore(telemetry): refresh AgentsView activity data" -- data/ai_activity.json
    GIT_TERMINAL_PROMPT=0 git pull --ff-only origin main
    GIT_TERMINAL_PROMPT=0 git push origin main
    echo "pushed"
    echo "=== $(date '+%F %T') sync done ==="
} >> "$LOG" 2>&1
