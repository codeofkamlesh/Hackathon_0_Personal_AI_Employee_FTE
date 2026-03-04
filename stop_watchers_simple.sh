#!/bin/bash
# Stop simple background processes

if [ -f .gmail_watcher.pid ]; then
    PID=$(cat .gmail_watcher.pid)
    kill $PID 2>/dev/null && echo "✓ Gmail watcher stopped (PID: $PID)" || echo "✗ Gmail watcher not running"
    rm .gmail_watcher.pid
fi

if [ -f .linkedin_watcher.pid ]; then
    PID=$(cat .linkedin_watcher.pid)
    kill $PID 2>/dev/null && echo "✓ LinkedIn watcher stopped (PID: $PID)" || echo "✗ LinkedIn watcher not running"
    rm .linkedin_watcher.pid
fi

echo "All watchers stopped!"
