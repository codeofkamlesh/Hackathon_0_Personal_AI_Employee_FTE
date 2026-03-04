#!/bin/bash
# Master Orchestrator - Runs both Gmail and LinkedIn workflows
# Monitors watchers and processes approved actions automatically

echo "=============================================="
echo "AI EMPLOYEE ORCHESTRATOR"
echo "Both Gmail and LinkedIn Workflows"
echo "=============================================="
echo ""

PROJECT_DIR="/mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE"
cd "$PROJECT_DIR"

# Function to process pending approvals
process_approvals() {
    echo ""
    echo "🔍 Checking for pending approvals..."

    # Check Pending_Approval folder
    PENDING_COUNT=$(ls -1 AI_Employee_Vault/Pending_Approval/*.md 2>/dev/null | wc -l)
    if [ $PENDING_COUNT -gt 0 ]; then
        echo "📋 Found $PENDING_COUNT item(s) pending approval"
        ls -lh AI_Employee_Vault/Pending_Approval/*.md
        echo ""
        echo "👉 Review files and move to Approved/ or Rejected/"
    fi

    # Check Approved folder
    APPROVED_COUNT=$(ls -1 AI_Employee_Vault/Approved/*.md 2>/dev/null | wc -l)
    if [ $APPROVED_COUNT -gt 0 ]; then
        echo ""
        echo "✅ Found $APPROVED_COUNT approved item(s) - processing..."

        # Process LinkedIn posts
        LINKEDIN_COUNT=$(ls -1 AI_Employee_Vault/Approved/LINKEDIN_POST_*.md 2>/dev/null | wc -l)
        if [ $LINKEDIN_COUNT -gt 0 ]; then
            echo "📱 Processing LinkedIn posts..."
            ./venv/bin/python3 skills/linkedin_poster.py
        fi

        # Process Email replies
        EMAIL_COUNT=$(ls -1 AI_Employee_Vault/Approved/EMAIL_REPLY_*.md 2>/dev/null | wc -l)
        if [ $EMAIL_COUNT -gt 0 ]; then
            echo "📧 Processing email replies..."
            ./venv/bin/python3 skills/gmail_reply_handler.py
        fi
    fi
}

# Function to process needs action items
process_needs_action() {
    echo ""
    echo "🔍 Checking for action items..."

    # Check for emails
    EMAIL_COUNT=$(ls -1 AI_Employee_Vault/Needs_Action/EMAIL_*.md 2>/dev/null | wc -l)
    if [ $EMAIL_COUNT -gt 0 ]; then
        echo "📧 Found $EMAIL_COUNT email(s) - drafting replies..."
        ./venv/bin/python3 skills/email_drafter.py
    fi

    # Check for LinkedIn opportunities
    LINKEDIN_COUNT=$(ls -1 AI_Employee_Vault/Needs_Action/LINKEDIN_POST_*.md 2>/dev/null | wc -l)
    if [ $LINKEDIN_COUNT -gt 0 ]; then
        echo "📱 Found $LINKEDIN_COUNT LinkedIn opportunity(ies) - drafting posts..."
        ./venv/bin/python3 skills/linkedin_drafter.py
    fi
}

echo "Starting orchestrator..."
echo "Press Ctrl+C to stop"
echo ""

# Main loop
ITERATION=0
while true; do
    ITERATION=$((ITERATION + 1))
    echo ""
    echo "=========================================="
    echo "Iteration #$ITERATION - $(date '+%Y-%m-%d %H:%M:%S')"
    echo "=========================================="

    # Process action items
    process_needs_action

    # Process approvals
    process_approvals

    echo ""
    echo "💤 Sleeping for 60 seconds..."
    echo "   (Watchers are running separately)"
    sleep 60
done
