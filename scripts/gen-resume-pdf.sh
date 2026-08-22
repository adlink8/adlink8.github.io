#!/usr/bin/env bash
# Regenerate /resume.pdf + /zh/resume.pdf from the current resume content.
# Mirrors the CI step in .github/workflows/hugo.yml (headless Chrome print).
#
# Also drops copies into static/ (gitignored) so `hugo server` can serve the
# download link during local preview. CI regenerates the real ones per deploy.
#
# Usage: ./scripts/gen-resume-pdf.sh
set -euo pipefail
cd "$(dirname "$0")/.."

# --- locate a browser (Chrome preferred, Edge fallback on Windows) ---
CHROME=""
for c in google-chrome google-chrome-stable chrome \
         "/c/Program Files/Google/Chrome/Application/chrome.exe" \
         "/c/Program Files (x86)/Microsoft/Edge/Application/msedge.exe" \
         "/c/Program Files/Microsoft/Edge/Application/msedge.exe"; do
    if command -v "$c" >/dev/null 2>&1; then CHROME="$c"; break; fi
done
[ -n "$CHROME" ] || { echo "ERROR: no Chrome/Edge found for headless PDF" >&2; exit 1; }

# --- locate hugo (PATH first, sibling hugo-bin second) ---
HUGO="$(command -v hugo || true)"
if [ -z "$HUGO" ] && [ -x ../hugo-bin/hugo.exe ]; then HUGO=../hugo-bin/hugo.exe; fi
[ -n "$HUGO" ] || { echo "ERROR: hugo not found (PATH or ../hugo-bin)" >&2; exit 1; }

# --- locate python (http server) ---
PYTHON="$(command -v python || command -v python3 || true)"
[ -n "$PYTHON" ] || { echo "ERROR: python not found for local http server" >&2; exit 1; }

"$HUGO" --minify

PORT=8787
"$PYTHON" -m http.server "$PORT" --directory public >/dev/null 2>&1 &
SERVER_PID=$!
trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT
sleep 2

for variant in "resume.pdf:resume" "zh/resume.pdf:zh/resume"; do
    out="${variant%%:*}"; path="${variant#*:}"
    # Windows Chrome needs an absolute Windows path for --print-to-pdf
    out_abs="$(cygpath -w "$PWD/public/$out" 2>/dev/null || echo "$PWD/public/$out")"
    "$CHROME" --headless=new --disable-gpu --no-sandbox \
      --no-pdf-header-footer --print-to-pdf="$out_abs" \
      "http://127.0.0.1:$PORT/$path/" >/dev/null 2>&1
    mkdir -p "$(dirname "static/$out")"
    cp "public/$out" "static/$out"
    echo "generated: public/$out ($(wc -c < "public/$out") bytes) -> static/$out"
done
