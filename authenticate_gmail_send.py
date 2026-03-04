#!/usr/bin/env python3
"""
Gmail API Authentication for SENDING emails
One-time setup to grant send permission
"""

import sys
import pickle
from pathlib import Path

try:
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
except ImportError:
    print("❌ ERROR: Gmail API libraries not installed!")
    print("Install with: pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
    sys.exit(1)

# Scope for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate():
    """Authenticate and save token for sending emails"""

    project_root = Path(__file__).parent
    credentials_path = project_root / 'credentials.json'
    token_path = project_root / 'token_send.pickle'

    print("\n" + "="*70)
    print("GMAIL API AUTHENTICATION - SEND PERMISSION")
    print("="*70)
    print("\nThis script will authenticate your Gmail account for SENDING emails.")
    print("You only need to do this once.\n")

    # Check if credentials.json exists
    if not credentials_path.exists():
        print(f"❌ ERROR: credentials.json not found at {credentials_path}")
        print("\nPlease download OAuth credentials from Google Cloud Console:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Enable Gmail API")
        print("3. Create OAuth 2.0 credentials")
        print("4. Download as credentials.json")
        print("5. Place in project root directory")
        sys.exit(1)

    print(f"✅ Found credentials.json")

    # Check if token already exists
    if token_path.exists():
        print(f"⚠️  Found existing token_send.pickle")
        response = input("Delete and re-authenticate? (yes/no): ").strip().lower()
        if response != 'yes':
            print("Keeping existing token. Exiting.")
            sys.exit(0)
        token_path.unlink()
        print("✅ Deleted old token")

    print("\n" + "="*70)
    print("AUTHENTICATION PROCESS")
    print("="*70)
    print("\nStarting OAuth flow...")
    print("Since you're in WSL, we'll use manual authentication.\n")

    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            str(credentials_path), SCOPES)

        # Get authorization URL
        auth_url, _ = flow.authorization_url(
            prompt='consent',
            access_type='offline'
        )

        print("="*70)
        print("STEP 1: OPEN THIS URL IN YOUR BROWSER")
        print("="*70)
        print("\n" + auth_url + "\n")
        print("="*70)
        print("\nSTEP 2: SIGN IN AND GRANT PERMISSION")
        print("="*70)
        print("- Sign in to your Gmail account")
        print("- Click 'Allow' to grant send permission")
        print("- You'll be redirected to localhost (this is normal)")
        print("\n" + "="*70)
        print("STEP 3: COPY THE AUTHORIZATION CODE")
        print("="*70)
        print("\nAfter granting permission, you'll see a URL like:")
        print("http://localhost:XXXXX/?code=4/0AY0e-g7X...&scope=...")
        print("\nCopy ONLY the code part (between 'code=' and '&scope')")
        print("="*70 + "\n")

        # Get code from user
        code = input("Paste the authorization code here: ").strip()

        if not code:
            print("\n❌ No code provided. Exiting.")
            sys.exit(1)

        print("\n🔄 Exchanging code for token...")
        flow.fetch_token(code=code)
        creds = flow.credentials

        # Save token
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

        print("\n" + "="*70)
        print("✅ AUTHENTICATION SUCCESSFUL!")
        print("="*70)
        print(f"\n✅ Token saved to: {token_path}")
        print("✅ You can now send emails via Gmail API")
        print("\n" + "="*70)
        print("NEXT STEPS")
        print("="*70)
        print("\n1. Test email sending:")
        print("   ./test_gmail_auto.sh")
        print("\n2. Or manually run:")
        print("   python3 skills/automated_gmail_handler.py")
        print("\n" + "="*70)

        # Test the token
        print("\n🧪 Testing token...")
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        print(f"✅ Connected to: {profile.get('emailAddress')}")
        print("\n✅ Setup complete! Gmail automation is ready.\n")

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure you copied the ENTIRE authorization code")
        print("2. Check that Gmail API is enabled in Google Cloud Console")
        print("3. Verify credentials.json is valid")
        print("4. Try running the script again")
        sys.exit(1)

if __name__ == '__main__':
    authenticate()
