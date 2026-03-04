#!/bin/bash
# Quick Setup for Gmail Send Automation
# Run this to complete Silver Tier Gmail automation

echo "=============================================="
echo "GMAIL SEND AUTOMATION - QUICK SETUP"
echo "=============================================="
echo ""
echo "This will set up automatic email sending via Gmail API"
echo "You'll need to authenticate once (takes 2 minutes)"
echo ""

cd "/mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE"

# Check if credentials.json exists
if [ ! -f "credentials.json" ]; then
    echo "❌ ERROR: credentials.json not found"
    echo ""
    echo "Please ensure credentials.json is in the project root"
    echo "Download from: https://console.cloud.google.com/"
    exit 1
fi

echo "✅ Found credentials.json"
echo ""

# Run authentication
echo "Starting authentication..."
echo ""
python3 authenticate_gmail_send.py

# Check if authentication succeeded
if [ -f "token_send.pickle" ]; then
    echo ""
    echo "=============================================="
    echo "✅ SETUP COMPLETE!"
    echo "=============================================="
    echo ""
    echo "Gmail automation is now ready."
    echo ""
    echo "Test it with:"
    echo "  ./test_gmail_auto.sh"
    echo ""
else
    echo ""
    echo "⚠️  Authentication incomplete"
    echo "Please run: python3 authenticate_gmail_send.py"
    echo ""
fi
