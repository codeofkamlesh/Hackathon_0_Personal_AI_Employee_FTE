#!/bin/bash
# Start both watchers in background using screen

PROJECT_DIR="/mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE"
cd "$PROJECT_DIR"

# Start Gmail watcher in screen
screen -dmS gmail_watcher bash -c "./venv/bin/python watchers/gmail_watcher.py"
echo "✓ Gmail watcher started in screen session 'gmail_watcher'"

# Start LinkedIn watcher in screen
screen -dmS linkedin_watcher bash -c "./venv/bin/python watchers/linkedin_watcher.py"
echo "✓ LinkedIn watcher started in screen session 'linkedin_watcher'"

echo ""
echo "Watchers are now running in background!"
echo ""
echo "To view Gmail watcher:     screen -r gmail_watcher"
echo "To view LinkedIn watcher:  screen -r linkedin_watcher"
echo "To detach from screen:     Press Ctrl+A then D"
echo "To stop watchers:          ./stop_watchers.sh"
