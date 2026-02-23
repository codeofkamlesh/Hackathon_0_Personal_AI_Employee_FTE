# Reasoning Loop Agent Skill

Generate structured Plan.md files for action items in the Needs_Action folder.

## Description

The Reasoning Loop is a core component of the Silver Tier Personal AI Employee. It reads action items from the `/Needs_Action` folder, analyzes them, and generates detailed Plan.md files in the `/Plans` folder with step-by-step execution strategies.

## What It Does

1. Scans `/Needs_Action` folder for pending action items
2. Parses each action file and extracts metadata
3. Analyzes the action type and context
4. Generates a structured plan with:
   - Objective and context
   - Step-by-step action items
   - Decision points and branching logic
   - Approval requirements
   - Next actions
5. Saves plan to `/Plans` folder

## When to Use

- After watchers create new action items
- Before processing tasks in Needs_Action
- As part of automated workflow (via cron)
- When you need structured plans for complex tasks

## Usage

### Command Line

```bash
python3 skills/reasoning_loop.py
```

### With Claude Code

```
/reasoning-loop
```

Or simply:
```
Generate plans for all items in Needs_Action
```

### Automated (Cron)

```bash
# Every 30 minutes
*/30 * * * * cd /path/to/project && python3 skills/reasoning_loop.py
```

## Plan Types Generated

### Email Plans
- Analyze sender and content
- Determine response requirements
- Draft reply strategy
- Set urgency level

### LinkedIn Post Plans
- Review brand guidelines
- Suggest content topics
- Structure post format
- Define approval workflow

### File Processing Plans
- Identify file type
- Determine processing steps
- Define output requirements
- Set completion criteria

### Generic Plans
- Analyze action requirements
- Break down into steps
- Identify dependencies
- Define success criteria

## Output Format

Plans are created as Markdown files with:

```markdown
---
type: plan
source: reasoning_loop
action_type: [email|linkedin_post|file_drop|generic]
created: [ISO timestamp]
status: pending
original_file: [source action file]
---

# Plan: [Title]

## Context
[Background information]

## Objective
[What needs to be accomplished]

## Steps
- [ ] Step 1
- [ ] Step 2
- [ ] Step 3

## Decision Points
[Key decisions and branching logic]

## Next Actions
[Immediate next steps]
```

## Integration Points

- **Input**: `/Needs_Action/*.md` files
- **Output**: `/Plans/PLAN_*.md` files
- **References**: `Company_Handbook.md` for guidelines
- **Triggers**: Watchers, cron jobs, manual execution

## Configuration

No configuration required. The skill automatically:
- Detects vault location
- Reads action file metadata
- Generates appropriate plan types
- Handles errors gracefully

## Error Handling

- Skips unparseable files with warning
- Continues processing remaining files
- Logs errors without stopping
- Reports summary at completion

## Performance

- Processes ~10 files per second
- Minimal memory footprint
- No external dependencies
- Instant execution

## Examples

### Example 1: Email Action

**Input**: `EMAIL_20260223_120000_client_inquiry.md`

**Output**: `PLAN_20260223_120100_EMAIL_client_inquiry.md`
- Analyzes email content
- Suggests response strategy
- Identifies urgency
- Creates approval workflow if needed

### Example 2: LinkedIn Post

**Input**: `LINKEDIN_POST_20260223_090000.md`

**Output**: `PLAN_20260223_090100_LINKEDIN_POST.md`
- Reviews brand guidelines
- Suggests post topics
- Structures content format
- Defines HITL approval process

## Best Practices

1. **Run regularly**: Schedule via cron for automatic processing
2. **Review plans**: Check generated plans before execution
3. **Update handbook**: Keep Company_Handbook.md current for better plans
4. **Monitor output**: Review Plans folder periodically
5. **Archive old plans**: Move completed plans to Done folder

## Troubleshooting

**No plans generated:**
- Check if Needs_Action folder has files
- Verify file format (must be .md)
- Check file permissions

**Plans missing details:**
- Update Company_Handbook.md with more guidelines
- Ensure action files have proper frontmatter
- Add more context to action items

**Errors during execution:**
- Check Python version (3.8+)
- Verify vault path exists
- Check file write permissions

## Future Enhancements (Gold Tier)

- AI-powered plan generation using Claude
- Learning from past successful plans
- Automatic plan execution
- Multi-step plan orchestration
- Plan templates and customization

## Related Skills

- `process_needs_action` - Executes plans
- `read_vault_status` - Views current state
- `linkedin_drafter` - Creates LinkedIn content

## Version

Silver Tier - v1.0.0
