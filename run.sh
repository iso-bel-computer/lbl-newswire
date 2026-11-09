#!/usr/bin/env bash
set -u

PROJECT_DIR="$HOME/services/PolicyDashboard"
PORT=8765
STARTUP_TIMEOUT=300   # seconds to wait for the model to load
LOG_DIR="$PROJECT_DIR/logs"

cd "$PROJECT_DIR" || exit 1
mkdir -p "$LOG_DIR"

# Don't let two runs overlap (e.g. if one hangs)
exec 9>/tmp/policyscraper.lock
flock -n 9 || { echo "$(date) - already running, skipping"; exit 0; }

setsid ./venv/bin/local-jev serve --model nli-deberta-large >> "$LOG_DIR/llm-server.log" 2>&1 &
SERVER_PID=$!

cleanup() {
    if kill -0 "$SERVER_PID" 2>/dev/null; then
        kill -TERM -- "-$SERVER_PID" 2>/dev/null
        for _ in {1..20}; do
            kill -0 "$SERVER_PID" 2>/dev/null || return
            sleep 0.5
        done
        kill -KILL -- "-$SERVER_PID" 2>/dev/null
    fi
}
trap cleanup EXIT

ready=0
for ((i = 0; i < $STARTUP_TIMEOUT; i++)); do
    if (exec 3<>/dev/tcp/127.0.0.1/$PORT) 2>/dev/null; then
        ready=1
        break
    fi
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
        echo "$(date) - LLM server died during startup (see llm-server.log)"
        exit 1
    fi
    sleep 1
done

if [ "$ready" -ne 1 ]; then
    echo "$(date) - LLM server not ready after ${STARTUP_TIMEOUT}s"
    exit 1
fi

./venv/bin/python ./main.py

status=$?

cleanup

if [ "$status" -ne 0 ]; then
    echo "$(date) - scraper exited with status $status, skipping upload"
    exit "$status"
fi

scp -i "$HOME/.ssh/id_ed25519" -o BatchMode=yes \
    data/articles.db 1sobel@ssh.pythonanywhere.com:./lbl-newswire/data/articles.db \
    || echo "$(date) - upload failed"
