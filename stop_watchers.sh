#!/bin/bash
# Stop both watchers

echo "Stopping watchers..."

# Kill Gmail watcher screen session
screen -S gmail_watcher -X quit 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ Gmail watcher stopped"
else
    echo "✗ Gmail watcher was not running"
fi

# Kill LinkedIn watcher screen session
screen -S linkedin_watcher -X quit 2>/dev/null
if [ $? -eq 0 ]; then
    echo "✓ LinkedIn watcher stopped"
else
    echo "✗ LinkedIn watcher was not running"
fi

echo ""
echo "All watchers stopped!"
