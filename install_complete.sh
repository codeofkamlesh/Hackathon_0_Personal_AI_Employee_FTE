#!/bin/bash
# Complete Installation Script for AI Employee System
# Installs all dependencies for Gmail and LinkedIn automation

echo "=============================================="
echo "AI EMPLOYEE - COMPLETE INSTALLATION"
echo "=============================================="
echo ""

PROJECT_DIR="/mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE"
cd "$PROJECT_DIR"

# Step 1: Python virtual environment
echo "Step 1: Setting up Python virtual environment..."
echo "-----------------------------------------------"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Step 2: Install Python dependencies
echo ""
echo "Step 2: Installing Python dependencies..."
echo "-----------------------------------------------"
./venv/bin/pip install -r requirements.txt
echo "✅ Python dependencies installed"

# Step 3: Install Playwright for browser automation
echo ""
echo "Step 3: Installing Playwright for browser automation..."
echo "-----------------------------------------------"
./venv/bin/pip install playwright
./venv/bin/playwright install chromium
echo "✅ Playwright installed"

# Step 4: Install Node.js dependencies for Email MCP
echo ""
echo "Step 4: Installing Email MCP server..."
echo "-----------------------------------------------"
cd mcp-servers/email
npm install
cd ../..
echo "✅ Email MCP server installed"

# Step 5: Make scripts executable
echo ""
echo "Step 5: Making scripts executable..."
echo "-----------------------------------------------"
chmod +x *.sh
chmod +x skills/*.py
chmod +x watchers/*.py
echo "✅ Scripts are executable"

# Step 6: Create necessary directories
echo ""
echo "Step 6: Creating vault directories..."
echo "-----------------------------------------------"
mkdir -p AI_Employee_Vault/{Needs_Action,Pending_Approval,Approved,Rejected,Done,Logs}
mkdir -p logs
echo "✅ Directories created"

echo ""
echo "=============================================="
echo "INSTALLATION COMPLETE!"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Authenticate Gmail: ./venv/bin/python3 watchers/gmail_watcher.py"
echo "2. Test LinkedIn: ./test_linkedin_workflow.sh"
echo "3. Test Gmail: ./test_gmail_workflow.sh"
echo "4. Run both: ./start_watchers.sh && ./orchestrator.sh"
echo ""
