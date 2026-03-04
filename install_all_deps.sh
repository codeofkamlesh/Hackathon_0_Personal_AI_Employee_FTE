#!/bin/bash
# Complete Dependency Installer - Run this ONCE with sudo
# This installs ALL Chromium dependencies automatically

echo "=========================================="
echo "Installing ALL Chromium Dependencies"
echo "=========================================="
echo ""

# Use Playwright's built-in installer (handles everything)
./venv/bin/playwright install-deps chromium

echo ""
echo "=========================================="
echo "✅ ALL DEPENDENCIES INSTALLED"
echo "=========================================="
echo ""
echo "Now test with: ./test_linkedin_auto.sh"
