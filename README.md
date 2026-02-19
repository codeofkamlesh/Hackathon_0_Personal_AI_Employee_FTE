# Personal AI Employee - Bronze Tier Implementation

A local-first AI Employee system using Claude Code and Obsidian for autonomous task management.

## Overview

This Bronze tier implementation provides the foundational layer for a Personal AI Employee that can:
- Monitor a drop folder for new files
- Process tasks from a Needs_Action queue
- Maintain a dashboard of activities
- Follow rules defined in a Company Handbook

## Architecture

```
AI_Employee_Vault/          # Obsidian vault (knowledge base)
├── Inbox/                  # Drop folder for new files
├── Needs_Action/           # Tasks awaiting processing
├── Done/                   # Completed tasks
├── Plans/                  # Task plans
├── Pending_Approval/       # Actions requiring approval
├── Approved/               # Approved actions
├── Rejected/               # Rejected actions
├── Logs/                   # System logs
├── Dashboard.md            # Real-time status summary
└── Company_Handbook.md     # Operating rules and guidelines

watchers/                   # Perception layer
├── base_watcher.py         # Base class for all watchers
└── filesystem_watcher.py   # Monitors Inbox folder

skills/                     # AI functionality as Agent Skills
├── process_needs_action.py # Process tasks from queue
├── read_vault_status.py    # Display vault status
├── process_needs_action/
│   └── SKILL.md
└── read_vault_status/
    └── SKILL.md
```

## Prerequisites

- Python 3.8 or higher
- Claude Code CLI installed and configured
- Obsidian (optional, for GUI viewing)

## Setup Instructions

### 1. Install Dependencies

```bash
# No external dependencies required for Bronze tier
# Standard library only
```

### 2. Verify Folder Structure

The vault structure should already be created. Verify with:

```bash
python skills/read_vault_status.py
```

### 3. Start the File System Watcher

```bash
cd watchers
python filesystem_watcher.py ../AI_Employee_Vault ../AI_Employee_Vault/Inbox
```

This will monitor the Inbox folder and create action items in Needs_Action when new files are dropped.

### 4. Test the System

Drop a test file into the Inbox:

```bash
echo "Test file content" > AI_Employee_Vault/Inbox/test.txt
```

The watcher will detect it and create an action file in Needs_Action.

### 5. Process Tasks with Claude Code

Use Claude Code to process the tasks:

```bash
claude
```

Then ask Claude to:
- "Show me the vault status"
- "Process all files in Needs_Action"

## Usage

### Running the Watcher

The File System Watcher runs continuously and monitors the Inbox folder:

```bash
python watchers/filesystem_watcher.py [vault_path] [drop_folder]
```

**Parameters:**
- `vault_path`: Path to AI_Employee_Vault (default: ../AI_Employee_Vault)
- `drop_folder`: Path to folder to monitor (default: ../AI_Employee_Vault/Inbox)

**Example:**
```bash
python watchers/filesystem_watcher.py
```

Press Ctrl+C to stop the watcher.

### Using Skills with Claude Code

The system includes two Agent Skills:

**1. Read Vault Status**
```bash
python skills/read_vault_status.py
```
Shows current vault status, folder contents, and pending actions.

**2. Process Needs Action**
```bash
python skills/process_needs_action.py
```
Processes all files in Needs_Action and moves them to Done.

### Workflow Example

1. **Drop a file** into `AI_Employee_Vault/Inbox/`
2. **Watcher detects** the file and creates an action item in `Needs_Action/`
3. **Claude Code reads** the action item from `Needs_Action/`
4. **Claude processes** the task according to `Company_Handbook.md` rules
5. **Task is moved** to `Done/` with timestamp
6. **Dashboard is updated** with activity log

## Bronze Tier Checklist

- [x] Obsidian vault with Dashboard.md and Company_Handbook.md
- [x] One working Watcher script (File System monitoring)
- [x] Claude Code successfully reading from and writing to the vault
- [x] Basic folder structure: /Inbox, /Needs_Action, /Done
- [x] All AI functionality implemented as Agent Skills

## Key Features

### 1. File System Watcher
- Monitors Inbox folder every 30 seconds
- Creates detailed action files for new items
- Tracks file metadata (size, type, timestamp)
- Prevents duplicate processing

### 2. Dashboard
- Real-time system status
- Activity logs
- Task completion metrics
- Alert notifications

### 3. Company Handbook
- Operating rules and guidelines
- Approval thresholds
- Communication templates
- Task prioritization rules

### 4. Agent Skills
- Modular, reusable functionality
- Can be invoked by Claude Code
- Follow SKILL.md specification
- Easy to extend

## Customization

### Modify Watcher Behavior

Edit `watchers/filesystem_watcher.py`:
- Change `check_interval` for different polling frequency
- Modify `create_action_file()` to customize action file format
- Add file type filtering or size limits

### Update Operating Rules

Edit `AI_Employee_Vault/Company_Handbook.md`:
- Adjust approval thresholds
- Add new task prioritization rules
- Customize response templates

### Add New Skills

Create a new skill following this pattern:
```python
# skills/my_skill.py
def my_skill(vault_path: str = None):
    # Your skill logic here
    pass
```

Create corresponding SKILL.md documentation.

## Troubleshooting

### Watcher Not Detecting Files
- Verify the Inbox folder path is correct
- Check file permissions
- Ensure watcher is running (check console output)

### Claude Code Can't Read Vault
- Verify vault path is correct
- Check that Dashboard.md and Company_Handbook.md exist
- Ensure Claude Code has file system access

### Files Not Moving to Done
- Check folder permissions
- Verify the process_needs_action skill is working
- Look for error messages in console output

## Next Steps (Silver Tier)

To upgrade to Silver tier, add:
- Gmail Watcher for email monitoring
- WhatsApp Watcher for message monitoring
- MCP server for external actions
- Human-in-the-loop approval workflow
- Scheduled operations via cron

## Security Notes

- All data stays local (no cloud sync in Bronze tier)
- No external API calls
- No credentials required
- File system access only

## License

This is a hackathon project for educational purposes.

## Support

For questions or issues, refer to the main hackathon documentation or join the Wednesday Research Meetings.
