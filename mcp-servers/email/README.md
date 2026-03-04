# Email MCP Server

Email capabilities for the Personal AI Employee via Model Context Protocol (MCP).

## Overview

This MCP server provides email sending and drafting capabilities with support for Human-in-the-Loop (HITL) approval workflows. It's designed to integrate seamlessly with Claude Code and the AI Employee system.

## Features

- **send_email**: Send emails via SMTP
- **draft_email**: Create email drafts for approval workflow
- Mock mode for safe testing
- Production-ready SMTP configuration support

## Installation

```bash
cd mcp-servers/email
npm install
```

## Configuration

### Mock Mode (Default)

The server runs in mock mode by default, logging emails instead of sending them. Perfect for testing.

### Production Mode

To use real SMTP, configure environment variables:

```bash
export EMAIL_FROM="your-email@example.com"
export SMTP_HOST="smtp.gmail.com"
export SMTP_PORT="587"
export SMTP_USER="your-email@example.com"
export SMTP_PASSWORD="your-app-password"
```

For Gmail:
1. Enable 2-factor authentication
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the app password as SMTP_PASSWORD

## Usage with Claude Code

The server is automatically registered in `.claude/settings.json`:

```json
{
  "mcpServers": {
    "email": {
      "command": "node",
      "args": ["mcp-servers/email/index.js"],
      "env": {
        "EMAIL_FROM": "ai-employee@example.com"
      }
    }
  }
}
```

## Available Tools

### send_email

Send an email to a recipient.

**Parameters:**
- `to` (required): Recipient email address
- `subject` (required): Email subject line
- `body` (required): Email body content (plain text)
- `cc` (optional): CC recipients (comma-separated)
- `attachments` (optional): Array of file paths to attach

**Example:**
```javascript
{
  "to": "client@example.com",
  "subject": "Project Update",
  "body": "Here's the latest update on your project...",
  "cc": "manager@example.com"
}
```

### draft_email

Create an email draft without sending (for approval workflow).

**Parameters:**
- `to` (required): Recipient email address
- `subject` (required): Email subject line
- `body` (required): Email body content

**Example:**
```javascript
{
  "to": "client@example.com",
  "subject": "Proposal",
  "body": "Thank you for your interest..."
}
```

## Testing

### Test the Server

```bash
# Start the server
npm start

# In another terminal, test with MCP client
# (requires @modelcontextprotocol/sdk)
```

### Mock Mode Output

When running in mock mode, you'll see:
```
[MOCK EMAIL] Would send email:
  To: client@example.com
  Subject: Project Update
  Body: Here's the latest update...
```

## Integration with AI Employee

The email MCP server integrates with:

1. **Gmail Watcher**: Monitors incoming emails
2. **Reasoning Loop**: Generates email response plans
3. **HITL Workflow**: Requires approval before sending
4. **Email MCP Server**: Executes approved email sends

### Workflow Example

```
Gmail Watcher → Needs_Action → Reasoning Loop → Plan
                                                   ↓
                                            Draft Email
                                                   ↓
                                         Pending_Approval
                                                   ↓
                                         [Human Review]
                                                   ↓
                                              Approved
                                                   ↓
                                    Email MCP Server (send_email)
                                                   ↓
                                                Done
```

## Security

- Never commits credentials to code
- Uses environment variables for sensitive data
- Mock mode by default for safe testing
- HITL approval for sensitive actions
- Complete audit trail

## Troubleshooting

**Server won't start:**
- Check Node.js version (18+)
- Run `npm install` to install dependencies
- Verify index.js path in settings.json

**Emails not sending:**
- Check SMTP credentials
- Verify firewall/network settings
- Test with mock mode first
- Check server logs for errors

**MCP connection issues:**
- Restart Claude Code
- Check settings.json syntax
- Verify server is running
- Check stdio communication

## Development

### Add New Tools

Edit `index.js` and add to the tools array:

```javascript
{
  name: 'new_tool',
  description: 'Tool description',
  inputSchema: {
    type: 'object',
    properties: {
      // Define parameters
    },
    required: ['param1']
  }
}
```

Then implement the handler in `setupToolHandlers()`.

## Version

Silver Tier - v1.0.0

## License

MIT
