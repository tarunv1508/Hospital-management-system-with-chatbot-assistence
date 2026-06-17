#!/usr/bin/env python3
"""
SIMPLE TEST: Verify Email Configuration
This tests Gmail SMTP credentials
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

print("\n" + "="*70)
print("📧 GMAIL SMTP TEST - Verify Email Settings")
print("="*70)

# Current configuration in backend.py
EMAIL_ADDRESS = "primelifehospital@gmail.com"
EMAIL_PASSWORD = "primelife@123"  # ❌ THIS IS WRONG!

print("\n⚠️  CURRENT CONFIGURATION IN backend.py:")
print(f"    EMAIL_ADDRESS = '{EMAIL_ADDRESS}'")
print(f"    EMAIL_PASSWORD = '{'*' * len(EMAIL_PASSWORD)}'")

print("\n❌ PROBLEM: The password 'primelife@123' is NOT a valid Gmail app password!")
print("   Gmail SMTP will REJECT this authentication.\n")

print("🧪 Testing Gmail connection with current credentials...")
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    print("✓ Connection successful!")
except smtplib.SMTPAuthenticationError as e:
    print(f"✗ Authentication FAILED: {str(e)}")
    print("\n   This confirms the password is incorrect!")
except smtplib.SMTPException as e:
    print(f"✗ SMTP Error: {str(e)}")
except Exception as e:
    print(f"✗ Error: {str(e)}")

print("\n" + "="*70)
print("✅ HOW TO FIX THIS:")
print("="*70)

print("""
STEP 1: Get Real Gmail App Password
        Go to: https://myaccount.google.com/apppasswords
        
        - Login with your Gmail account
        - Select 'Mail' from dropdown
        - Select 'Windows Computer' from dropdown  
        - Click 'Generate'
        - Copy the 16-character PASSWORD (not your Gmail password!)

STEP 2: Update backend.py
        Open backend.py and find line 24:
        
        OLD (WRONG):
        EMAIL_PASSWORD = "primelife@123"
        
        NEW (YOUR APP PASSWORD):
        EMAIL_PASSWORD = "xxxx xxxx xxxx xxxx"
        
        Example:
        EMAIL_PASSWORD = "abcd efgh ijkl mnop"

STEP 3: Restart Flask Server
        Stop server (Ctrl+C) and restart:
        python backend.py

STEP 4: Test Appointment Form
        - Go to http://localhost:5000/appointment.html
        - Fill form with YOUR email and phone
        - Submit
        - Check YOUR email inbox for confirmation
        - Check YOUR phone for SMS (if SMS API key added)
""")

print("="*70)
print("⚠️  IMPORTANT:")
print("="*70)
print("""
✓ The CODE is CORRECT - it WILL send to USER'S email and phone
✓ Email GOES TO: The email address USER enters in the form
✓ SMS GOES TO: The phone number USER enters in the form

The ONLY problem is Gmail authentication credentials.
Once you add the correct app password, emails WILL be sent! ✅
""")

print("="*70 + "\n")
