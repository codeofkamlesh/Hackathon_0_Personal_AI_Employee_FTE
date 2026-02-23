# LinkedIn Drafter Agent Skill

Draft LinkedIn posts with Human-in-the-Loop (HITL) approval workflow.

## Description

The LinkedIn Drafter creates professional LinkedIn posts designed to generate business and sales leads. It implements a strict HITL workflow where posts MUST be approved by a human before posting.

## What It Does

1. Reads Company_Handbook.md for brand voice and guidelines
2. Drafts professional LinkedIn post content
3. Creates approval request in `/Pending_Approval` folder
4. Waits for human to review and approve
5. Executes approved posts (moves to Done with execution log)

## HITL Workflow

```
Draft → Pending_Approval → [Human Review] → Approved → Execute → Done
                                          ↓
                                      Rejected
```

**CRITICAL**: Posts will NEVER be published without explicit human approval.

## When to Use

- When LinkedIn watcher creates posting opportunity
- For scheduled business content
- To generate sales leads
- For brand awareness campaigns

## Usage

### Command Line

```bash
python3 skills/linkedin_drafter.py
```

### With Claude Code

```
/linkedin-drafter
```

Or:
```
Draft a LinkedIn post about our business
```

### Automated (Cron)

```bash
# Daily at 9 AM
0 9 * * 1-5 cd /path/to/project && python3 skills/linkedin_drafter.py
```

## Post Templates

The skill includes three professional post templates:

### 1. Expertise Post
- Showcases your knowledge and experience
- Demonstrates thought leadership
- Includes actionable insights
- Call-to-action for engagement

### 2. Value Proposition Post
- Highlights business value
- Addresses common pain points
- Presents solutions
- Encourages conversation

### 3. Success Story Post
- Shares client results
- Demonstrates ROI
- Builds credibility
- Attracts similar clients

## Approval Process

### Step 1: Review Draft

Navigate to `/Pending_Approval` and open the post file:

```markdown
---
type: approval_request
action: linkedin_post
status: pending
---

# LinkedIn Post Approval Required

## Draft Post Content

[Post content here]

## Instructions

To APPROVE: Move to /Approved folder
To REJECT: Move to /Rejected folder
```

### Step 2: Edit (Optional)

You can edit the post content directly in the file before approving.

### Step 3: Approve or Reject

**To Approve:**
```bash
mv AI_Employee_Vault/Pending_Approval/LINKEDIN_POST_*.md AI_Employee_Vault/Approved/
```

**To Reject:**
```bash
mv AI_Employee_Vault/Pending_Approval/LINKEDIN_POST_*.md AI_Employee_Vault/Rejected/
```

### Step 4: Execution

Run the drafter again to execute approved posts:

```bash
python3 skills/linkedin_drafter.py
```

Approved posts are moved to `/Done` with execution logs.

## Post Guidelines

All posts follow these principles:

- **Professional tone**: Business-appropriate language
- **Value-focused**: Provides insights or solutions
- **Engaging**: Encourages comments and connections
- **Branded**: Reflects company voice and values
- **Actionable**: Clear call-to-action
- **Optimized length**: 150-300 words
- **Hashtags**: 3-5 relevant tags

## Output Format

### Approval Request

```markdown
---
type: approval_request
action: linkedin_post
created: [timestamp]
status: pending
requires_approval: true
---

# LinkedIn Post Approval Required

## Draft Post Content

[Post content with emojis, formatting, hashtags]

## Instructions

[Approval/rejection instructions]

## Posting Checklist

- [ ] Content is accurate
- [ ] Tone matches brand
- [ ] No sensitive info
- [ ] CTA is clear
- [ ] Hashtags relevant
```

### Execution Log

```markdown
---
type: execution_log
action: linkedin_post
executed: [timestamp]
status: ready_for_manual_posting
---

# LinkedIn Post Execution Log

## Status

✓ Post approved by human
✓ Ready for manual posting

## Approved Content

[Final post content]

## Next Steps (Manual)

1. Log into LinkedIn
2. Create new post
3. Copy content
4. Post to feed
```

## Integration Points

- **Input**: LinkedIn watcher triggers or manual execution
- **Reference**: `Company_Handbook.md` for brand guidelines
- **Approval**: `/Pending_Approval` folder
- **Execution**: `/Approved` folder
- **Archive**: `/Done` folder

## Configuration

Customize post templates by editing the `draft_linkedin_post()` function in `linkedin_drafter.py`.

Add your own templates:

```python
posts = {
    'custom_topic': """Your custom post template here""",
}
```

## Safety Features

1. **Mandatory Approval**: No post can be published without human review
2. **Edit Before Approve**: Modify content before approving
3. **Rejection Option**: Easy to reject unwanted posts
4. **Audit Trail**: All posts logged in Done folder
5. **Expiration**: Approval requests expire after 24 hours

## Silver vs Gold Tier

**Silver Tier (Current):**
- Drafts posts automatically
- Requires manual posting to LinkedIn
- Human copies content and posts

**Gold Tier (Future):**
- Automated posting via LinkedIn MCP server
- Direct API integration
- Scheduled posting
- Engagement tracking

## Examples

### Example 1: Daily Business Post

```bash
# Morning: Drafter creates post
python3 skills/linkedin_drafter.py
# → Creates LINKEDIN_POST_20260223_090000.md in Pending_Approval

# You review and approve
mv AI_Employee_Vault/Pending_Approval/LINKEDIN_POST_*.md AI_Employee_Vault/Approved/

# Execute approved post
python3 skills/linkedin_drafter.py
# → Creates execution log in Done folder
# → You manually post to LinkedIn
```

### Example 2: Automated Daily Workflow

```bash
# Cron runs drafter at 9 AM
0 9 * * 1-5 python3 skills/linkedin_drafter.py

# You check Pending_Approval during morning routine
# Approve good posts, reject others

# Cron runs execution at 10 AM
0 10 * * 1-5 python3 skills/linkedin_drafter.py

# You post approved content to LinkedIn
```

## Best Practices

1. **Review daily**: Check Pending_Approval folder each morning
2. **Edit freely**: Customize posts to match current context
3. **Track results**: Note which post types get best engagement
4. **Update templates**: Refine based on performance
5. **Maintain consistency**: Post regularly for best results

## Troubleshooting

**No posts generated:**
- Check if LinkedIn watcher is running
- Verify Company_Handbook.md exists
- Check vault path

**Can't approve posts:**
- Verify Approved folder exists
- Check file permissions
- Use absolute paths when moving files

**Posts not executing:**
- Run drafter after approving
- Check for files in Approved folder
- Verify Done folder exists

## Related Skills

- `linkedin_watcher` - Creates posting opportunities
- `reasoning_loop` - Generates plans for posts
- `read_vault_status` - Views pending approvals

## Version

Silver Tier - v1.0.0 (HITL with manual posting)
