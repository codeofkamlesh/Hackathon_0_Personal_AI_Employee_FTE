#!/bin/bash
# Check status of both watchers

echo "=== Watcher Status ==="
echo ""

# Check Gmail watcher
if screen -list | grep -q "gmail_watcher"; then
    echo "✓ Gmail watcher: RUNNING"
else
    echo "✗ Gmail watcher: STOPPED"
fi

# Check LinkedIn watcher
if screen -list | grep -q "linkedin_watcher"; then
    echo "✓ LinkedIn watcher: RUNNING"
else
    echo "✗ LinkedIn watcher: STOPPED"
fi

echo ""
echo "=== Recent Activity ==="
echo ""

# Show recent action files
echo "Recent items in Needs_Action:"
ls -lt AI_Employee_Vault/Needs_Action/*.md 2>/dev/null | head -5 | awk '{print $9, $6, $7, $8}'

echo ""
echo "To view logs:"
echo "  Gmail:    screen -r gmail_watcher"
echo "  LinkedIn: screen -r linkedin_watcher"
