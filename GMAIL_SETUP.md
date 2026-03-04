# Gmail Integration Setup Guide

This guide walks you through setting up Gmail API integration for the AI Employee's Gmail watcher.

## Prerequisites

- Python 3.8 or higher
- Google account with Gmail
- credentials.json file (already in project root)

## Step 1: Install Required Libraries

```bash
pip install -r requirements.txt
```

This installs:
- google-auth
- google-auth-oauthlib
- google-auth-httplib2
- google-api-python-client

## Step 2: Enable Gmail API

Your credentials.json file is already configured for the project. It contains:
- Client ID: `33001390241-vbqerj0dfhv348gbikc8qtihddri8cvi.apps.googleusercontent.com`
- Project: `ai-employee-hac-0-silver-tier`

## Step 3: First-Time Authentication

When you run the Gmail watcher for the first time, it will:

1. Open a browser window for Google OAuth authentication
2. Ask you to sign in to your Google account
3. Request permission to read your Gmail messages
4. Save authentication token to `watchers/token.pickle`

```bash
python3 watchers/gmail_watcher.py
```

**Important:** The browser will open automatically. Follow these steps:
1. Select your Google account
2. Click "Allow" to grant Gmail read permissions
3. The watcher will start monitoring your inbox

## Step 4: Verify Authentication

After successful authentication, you should see:

```
Gmail Watcher started
Vault: /path/to/AI_Employee_Vault
Check interval: 120 seconds
Using real Gmail API
Monitoring for important/unread emails...
```

## Token Management

### Token Location
The authentication token is saved to:
```
watchers/token.pickle
```

### Token Expiration
- Tokens are automatically refreshed when expired
- If refresh fails, you'll be prompted to re-authenticate
- Delete `token.pickle` to force re-authentication

### Security
- **Never commit token.pickle to git** (already in .gitignore)
- Token grants read-only access to Gmail
- Token is stored locally, never sent to external servers

## Troubleshooting

### "Gmail API libraries not installed"

**Solution:**
```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### "credentials.json not found"

**Solution:**
Ensure credentials.json is in the project root directory:
```
Hackathon_0_Personal_AI_Employee_FTE/
├── credentials.json  ← Should be here
├── watchers/
│   └── gmail_watcher.py
```

### "Access blocked: This app's request is invalid"

**Possible causes:**
1. OAuth consent screen not configured
2. Redirect URI mismatch
3. API not enabled in Google Cloud Console

**Solution:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Select project: `ai-employee-hac-0-silver-tier`
3. Enable Gmail API
4. Configure OAuth consent screen
5. Add your email as a test user

### Browser doesn't open automatically

**Solution:**
The authentication URL will be printed to console. Copy and paste it into your browser manually.

### "Invalid grant" error

**Solution:**
Delete the token and re-authenticate:
```bash
rm watchers/token.pickle
python3 watchers/gmail_watcher.py
```

## Mock Mode Fallback

If Gmail API setup fails, the watcher automatically falls back to mock mode:
- No real emails are fetched
- System continues to work for testing
- You'll see: "Using mock Gmail service"

This allows you to test the entire system without Gmail integration.

## Query Customization

By default, the watcher monitors: `is:unread is:important`

To customize, edit `gmail_watcher.py`:

```python
# Monitor all unread emails
messages = self.service.list_messages('is:unread')

# Monitor emails from specific sender
messages = self.service.list_messages('from:client@example.com is:unread')

# Monitor emails with specific subject
messages = self.service.list_messages('subject:"urgent" is:unread')
```

## Production Deployment

For production use:

1. **Service Account**: Consider using a service account instead of OAuth for automated systems
2. **Domain-Wide Delegation**: For G Suite/Workspace, enable domain-wide delegation
3. **Rate Limits**: Gmail API has rate limits (check quotas in Cloud Console)
4. **Error Handling**: Monitor for API errors and implement retry logic
5. **Logging**: Enable detailed logging for troubleshooting

## Testing

### Test Authentication
```bash
python3 watchers/gmail_watcher.py
# Should authenticate and start monitoring
# Press Ctrl+C to stop
```

### Test Email Detection
1. Send yourself an important email
2. Mark it as unread
3. Wait up to 2 minutes (check interval)
4. Check `AI_Employee_Vault/Needs_Action/` for new email action file

### Verify Token Refresh
1. Wait 1 hour (token should still work)
2. Watcher should automatically refresh token
3. No re-authentication required

## Security Best Practices

1. **Credentials Protection**
   - Keep credentials.json secure
   - Never share or commit to public repos
   - Rotate credentials if compromised

2. **Minimal Permissions**
   - Current scope: `gmail.readonly` (read-only)
   - Never request more permissions than needed

3. **Token Storage**
   - token.pickle is encrypted
   - Stored locally only
   - Automatically managed by Google libraries

4. **Audit Trail**
   - All email accesses are logged
   - Check logs in `AI_Employee_Vault/Logs/`

## Next Steps

After Gmail integration is working:

1. Configure email response workflows
2. Set up Email MCP server for sending replies
3. Enable automated email processing
4. Configure cron jobs for continuous monitoring

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review watcher logs
3. Verify Google Cloud Console settings
4. Test with mock mode first

## References

- [Gmail API Documentation](https://developers.google.com/gmail/api)
- [Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)
- [OAuth 2.0 for Desktop Apps](https://developers.google.com/identity/protocols/oauth2/native-app)
