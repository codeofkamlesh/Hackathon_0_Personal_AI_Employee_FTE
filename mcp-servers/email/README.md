# Email MCP Server

Email capabilities for the Personal AI Employee via Model Context Protocol.

## Features

- Send emails via SMTP
- Draft emails for approval workflow
- Support for CC and attachments
- Mock mode for testing

## Installation

```bash
cd mcp-servers/email
npm install
```

## Configuration

Set environment variables:

```bash
export EMAIL_FROM="your-email@example.com"
export EMAIL_USER="your-smtp-username"
export EMAIL_PASSWORD="your-smtp-password"
```

For Gmail, use an App Password: https://support.google.com/accounts/answer/185833

## Usage

### Standalone Testing

```bash
npm start
```

### With Claude Code

Add to your Claude Code MCP configuration (`~/.config/claude-code/mcp.json`):

```json
{
  "servers": [
    {
      "name": "email",
      "command": "node",
      "args": ["/path/to/mcp-servers/email/index.js"],
      "env": {
        "EMAIL_FROM": "your-email@example.com",
        "EMAIL_USER": "your-smtp-username",
        "EMAIL_PASSWORD": "your-smtp-password"
      }
    }
  ]
}
```

## Available Tools

### send_email

Send an email to a recipient.

**Parameters:**
- `to` (required): Recipient email address
- `subject` (required): Email subject
- `body` (required): Email body (plain text)
- `cc` (optional): CC recipients (comma-separated)
- `attachments` (optional): Array of file paths

**Example:**
```javascript
{
  "to": "client@example.com",
  "subject": "Invoice #123",
  "body": "Please find attached your invoice.",
  "attachments": ["/path/to/invoice.pdf"]
}
```

### draft_email

Create an email draft without sending (for approval workflow).

**Parameters:**
- `to` (required): Recipient email address
- `subject` (required): Email subject
- `body` (required): Email body

## Mock Mode

By default, the server runs in mock mode for testing. Emails are logged but not sent.

To enable real sending, update the `createMockTransporter()` method in `index.js` with real SMTP credentials.

## Security

- Never commit credentials to git
- Use environment variables for sensitive data
- Consider using OAuth2 for Gmail instead of passwords
- Implement rate limiting for production use

## Production Checklist

- [ ] Replace mock transporter with real SMTP
- [ ] Set up proper authentication (OAuth2 recommended)
- [ ] Configure rate limiting
- [ ] Add retry logic for failed sends
- [ ] Implement email validation
- [ ] Add logging and monitoring
- [ ] Set up error notifications

## Troubleshooting

**Server won't start:**
- Check Node.js version (requires 18+)
- Run `npm install` to install dependencies

**Emails not sending:**
- Verify SMTP credentials
- Check firewall/network settings
- Enable "Less secure app access" for Gmail (or use App Password)

**MCP connection issues:**
- Verify path in mcp.json is absolute
- Check Claude Code logs for errors
- Ensure server process is running
