# Read Vault Status

Read and display the current status of the AI Employee vault.

## Description

This skill provides a comprehensive overview of the AI Employee vault, including folder status, dashboard summary, and pending actions.

## Usage

```bash
python skills/read_vault_status.py [vault_path]
```

Or invoke via Claude Code:
```
Show me the vault status
```

## What it does

1. Displays vault location and timestamp
2. Shows status of all folders (Inbox, Needs_Action, Done, etc.)
3. Counts items in each folder
4. Extracts and displays Dashboard summary
5. Lists pending actions (up to 5 most recent)

## Parameters

- `vault_path` (optional): Path to the Obsidian vault. Defaults to `AI_Employee_Vault`

## Example

```bash
# Check status with default vault path
python skills/read_vault_status.py

# Check status with custom vault path
python skills/read_vault_status.py /path/to/vault
```

## Output

The skill displays:
- Folder existence and item counts
- Dashboard summary (tasks completed, messages processed)
- Recent activity from Dashboard
- List of pending action files
