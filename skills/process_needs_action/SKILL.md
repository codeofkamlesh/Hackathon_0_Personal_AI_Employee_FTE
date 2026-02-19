# Process Needs Action

Process all files in the Needs_Action folder and move them to Done when complete.

## Description

This skill reads all markdown files in the AI_Employee_Vault/Needs_Action folder, processes them, and moves them to the Done folder with timestamps. It also updates the Dashboard with activity logs.

## Usage

```bash
python skills/process_needs_action.py [vault_path]
```

Or invoke via Claude Code:
```
Please process all files in the Needs_Action folder
```

## What it does

1. Scans the Needs_Action folder for .md files
2. Reads each file and displays a preview
3. Adds a processing timestamp to the content
4. Moves the file to Done folder with timestamp prefix
5. Updates the Dashboard.md with activity summary

## Parameters

- `vault_path` (optional): Path to the Obsidian vault. Defaults to `AI_Employee_Vault`

## Example

```bash
# Process with default vault path
python skills/process_needs_action.py

# Process with custom vault path
python skills/process_needs_action.py /path/to/vault
```

## Output

The skill will:
- Print progress for each file processed
- Show success (✓) or error (✗) for each operation
- Display final summary of processed files
- Update Dashboard.md with timestamp and count
