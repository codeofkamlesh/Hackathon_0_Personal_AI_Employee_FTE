#!/bin/bash

# Quick Start Script for AI Employee Bronze Tier
# This script helps you get started quickly

echo "=========================================="
echo "AI Employee Bronze Tier - Quick Start"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check vault structure
echo "Checking vault structure..."
if [ -d "AI_Employee_Vault" ]; then
    echo "✓ AI_Employee_Vault exists"
else
    echo "❌ AI_Employee_Vault not found"
    exit 1
fi

# Display vault status
echo ""
echo "=========================================="
echo "Current Vault Status:"
echo "=========================================="
python3 skills/read_vault_status.py
echo ""

# Instructions
echo "=========================================="
echo "Next Steps:"
echo "=========================================="
echo ""
echo "1. Start the File System Watcher:"
echo "   cd watchers"
echo "   python3 filesystem_watcher.py"
echo ""
echo "2. In another terminal, drop a test file:"
echo "   echo 'Test content' > AI_Employee_Vault/Inbox/test.txt"
echo ""
echo "3. Use Claude Code to process tasks:"
echo "   claude"
echo "   Then ask: 'Process all files in Needs_Action'"
echo ""
echo "4. Check the results:"
echo "   python3 skills/read_vault_status.py"
echo ""
echo "=========================================="
echo "For full documentation, see README.md"
echo "=========================================="
