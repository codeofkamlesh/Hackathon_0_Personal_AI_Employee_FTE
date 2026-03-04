#!/bin/bash
# Simple background process runner

PROJECT_DIR="/mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE"
cd "$PROJECT_DIR"

# Start Gmail watcher
nohup ./venv/bin/python watchers/gmail_watcher.py > logs/gmail_watcher.log 2>&1 &
GMAIL_PID=$!
echo $GMAIL_PID > .gmail_watcher.pid
echo "✓ Gmail watcher started (PID: $GMAIL_PID)"

# Start LinkedIn watcher
nohup ./venv/bin/python watchers/linkedin_watcher.py > logs/linkedin_watcher.log 2>&1 &
LINKEDIN_PID=$!
echo $LINKEDIN_PID > .linkedin_watcher.pid
echo "✓ LinkedIn watcher started (PID: $LINKEDIN_PID)"

echo ""
echo "Watchers running in background!"
echo "Logs: tail -f logs/gmail_watcher.log"
echo "      tail -f logs/linkedin_watcher.log"
