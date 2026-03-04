#!/bin/bash
# Install Chromium dependencies for WSL/Ubuntu

echo "Installing Chromium browser dependencies..."
echo "This requires sudo password"
echo ""

sudo apt-get update
sudo apt-get install -y \
    libnspr4 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0

echo ""
echo "✅ Dependencies installed!"
echo "Now run: ./test_linkedin_simple.sh"
