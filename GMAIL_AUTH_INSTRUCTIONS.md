# Gmail API Authentication Instructions

## Problem
The automated Gmail handler needs **send permission** to send emails via Gmail API.

## Solution - Manual Authentication (One-Time Setup)

### Step 1: Run the Authentication Script

Open your terminal and run:

```bash
cd /mnt/c/Users/Admin/Documents/GitHub/Hackathon_0_Personal_AI_Employee_FTE
python3 skills/automated_gmail_handler.py
```

### Step 2: Copy the Authentication URL

The script will display an authentication URL like:
```
🔗 Authentication URL:
https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=...
```

**Copy this entire URL**

### Step 3: Open URL in Windows Browser

1. Open your Windows browser (Chrome, Edge, Firefox)
2. Paste the URL
3. Sign in to your Gmail account
4. You'll see: "This app wants to send email on your behalf"
5. Click **Allow** or **Continue**

### Step 4: Get Authorization Code

After granting permission, you'll see a page with an authorization code or be redirected to localhost.

- If redirected to localhost with an error, **copy the 'code' parameter from the URL**
- If you see a code on the page, **copy that code**

Example URL: `http://localhost:45621/?code=4/0AY0e-g7X...&scope=...`
Copy the part after `code=` and before `&`

### Step 5: Paste Code Back

Go back to your terminal and paste the authorization code when prompted:
```
Enter the authorization code: [PASTE CODE HERE]
```

### Step 6: Test Email Sending

Once authenticated, the script will automatically send any approved emails in the `Approved` folder.

## After Authentication

The authentication token will be saved as `token_send.pickle`. You won't need to authenticate again unless:
- The token expires (rare)
- You revoke access in Google Account settings
- You delete the token file

## Testing

Run the test script:
```bash
./test_gmail_auto.sh
```

This will:
1. Create a test email in Approved folder
2. Send it via Gmail API
3. Move it to Done folder with execution log

## Troubleshooting

**"OAuth client was disabled"**
- Your existing token doesn't have send permission
- Delete `token.pickle` and `token_send.pickle`
- Re-run authentication

**"credentials.json not found"**
- Make sure credentials.json is in the project root
- Download from Google Cloud Console if missing

**"Invalid grant"**
- Token expired or revoked
- Delete `token_send.pickle` and re-authenticate

**Browser won't open in WSL**
- This is normal - use the manual URL method above
- Copy/paste the URL into Windows browser

## What This Enables

✅ Automatic email sending via Gmail API
✅ No browser automation needed
✅ Secure OAuth 2.0 authentication
✅ HITL approval workflow (emails must be in Approved folder)
✅ Complete Silver Tier Gmail automation

---
*Part of Silver Tier - Personal AI Employee*
