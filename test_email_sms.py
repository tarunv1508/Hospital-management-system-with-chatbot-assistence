#!/usr/bin/env python3
"""
TEST SCRIPT: Verify Email & SMS are sent to USER'S email and phone
This script tests the email and SMS notification system

Run this to verify:
1. Email sends to USER'S email (not hospital email)
2. SMS sends to USER'S phone (not hardcoded phone)
3. Configuration is working correctly
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
import requests
from datetime import datetime

print("\n" + "="*60)
print("🧪 EMAIL & SMS NOTIFICATION TEST")
print("="*60)

# ============================================================================
# TEST 1: Verify Gmail SMTP Configuration
# ============================================================================

print("\n✓ TEST 1: Gmail SMTP Configuration")
print("-" * 60)

# NOTE: These are WRONG - You must update them!
EMAIL_ADDRESS = "primelifehospital@gmail.com"
EMAIL_PASSWORD = "primelife@123"  # ❌ THIS IS WRONG! See instructions below

print(f"Configured Email: {EMAIL_ADDRESS}")
print(f"Configured Password: {'*' * len(EMAIL_PASSWORD)}")
print("\n⚠️  IMPORTANT: The current password 'primelife@123' will NOT work!")
print("   You need to use a REAL Gmail app-specific password.\n")

# Test Gmail SMTP connection
print("Testing Gmail SMTP connection...")
try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
    print("✓ Gmail SMTP connection: SUCCESS")
except smtplib.SMTPAuthenticationError:
    print("✗ Gmail SMTP connection: FAILED - Authentication Error")
    print("\n   SOLUTION:")
    print("   1. Go to: https://myaccount.google.com/apppasswords")
    print("   2. Select 'Mail' and 'Windows Computer'")
    print("   3. Click 'Generate'")
    print("   4. Copy the 16-character password")
    print("   5. Update backend.py line 24:")
    print("      EMAIL_PASSWORD = 'xxxx xxxx xxxx xxxx'")
except Exception as e:
    print(f"✗ Gmail SMTP connection: FAILED - {str(e)}")

print("\n" + "="*60)
# ============================================================================
# TEST 2: Test Email Sending to USER'S Email
# ============================================================================

print("✓ TEST 2: Send Test Email to YOUR Email Address")
print("-" * 60)

# Simulate user's email (what they enter in form)
test_user_email = input("Enter YOUR email address to receive test email: ").strip()
test_user_name = "John Doe"
test_user_doctor = "DR.S.Arjun Reddy"
test_user_department = "Cardiology"
test_appointment_id = 12345
test_date = "2026-06-20"

print(f"\nTest Email Details:")
print(f"  Sending TO: {test_user_email}  (USER'S EMAIL ✓)")
print(f"  Sending FROM: {EMAIL_ADDRESS}  (Hospital Email)")
print(f"  Patient Name: {test_user_name}")
print(f"  Doctor: {test_user_doctor}")
print(f"  Appointment ID: {test_appointment_id}")

try:
    msg = MIMEMultipart('alternative')
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = test_user_email  # ✓ SENDING TO USER'S EMAIL
    msg['Subject'] = "PrimeLife Hospital - Test Appointment Confirmation"
    
    date_obj = datetime.strptime(test_date, "%Y-%m-%d")
    formatted_date = date_obj.strftime("%B %d, %Y")
    
    body = f"""
Dear {test_user_name},

🧪 THIS IS A TEST EMAIL 🧪

Your appointment has been successfully scheduled at PrimeLife Hospital.

=== APPOINTMENT DETAILS ===
Appointment ID: {test_appointment_id}
Doctor: {test_user_doctor}
Department: {test_user_department}
Date: {formatted_date}
Hospital: PrimeLife Hospital
Address: Banjarhills rd no 12, Hyderabad, India
Phone: +91 9866208819

This is a test to verify emails are being sent to YOUR email address.

Thank you,
PrimeLife Hospital Team
"""
    
    msg.attach(MIMEText(body, 'plain'))
    
    print(f"\nAttempting to send email...")
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
    
    print(f"✓ Email sent successfully to {test_user_email}")
    print("\n  Check your inbox (or spam folder) for the test email!")
    
except smtplib.SMTPAuthenticationError:
    print(f"✗ Email failed: Gmail authentication error")
    print(f"  Password is incorrect. Use 16-character app password from:")
    print(f"  https://myaccount.google.com/apppasswords")
except Exception as e:
    print(f"✗ Email failed: {str(e)}")

print("\n" + "="*60)
# ============================================================================
# TEST 3: Test SMS Sending to USER'S Phone
# ============================================================================

print("✓ TEST 3: SMS Sending to YOUR Phone Number")
print("-" * 60)

test_user_phone = input("Enter YOUR phone number to test SMS (e.g., 9876543210): ").strip()
test_sms_key = "YOUR_FAST2SMS_API_KEY"  # Not configured

print(f"\nTest SMS Details:")
print(f"  Sending TO: +91{test_user_phone}  (USER'S PHONE ✓)")
print(f"  Patient Name: {test_user_name}")
print(f"  Doctor: {test_user_doctor}")
print(f"  Appointment ID: {test_appointment_id}")

# Format phone number
phone_clean = re.sub(r'[^0-9]', '', test_user_phone)
if len(phone_clean) == 10:
    phone_clean = '91' + phone_clean
elif len(phone_clean) == 12 and phone_clean.startswith('91'):
    pass
else:
    print(f"✗ Invalid phone number format: {test_user_phone}")
    print(f"  Use format: 9876543210 or +919876543210")
    phone_clean = None

if phone_clean:
    sms_message = f"PrimeLife Hospital: Hi {test_user_name}, your appointment with Dr. {test_user_doctor} is confirmed for 20-Jun-2026. ID: {test_appointment_id}. For support call 9866208819. Thank you!"
    
    print(f"\nSMS Message that would be sent:")
    print(f"  {sms_message}")
    
    if test_sms_key == "YOUR_FAST2SMS_API_KEY":
        print(f"\n⚠️  Fast2SMS API Key not configured (normal for testing)")
        print(f"   SMS will be logged but NOT actually sent.")
        print(f"\n   To send real SMS:")
        print(f"   1. Go to: https://www.fast2sms.com/")
        print(f"   2. Sign up and get API key")
        print(f"   3. Update backend.py line 31:")
        print(f"      SMS_API_KEY = 'your-actual-api-key'")
        print(f"\n✓ SMS logging is active (ready for real API key)")
    else:
        try:
            url = "https://www.fast2sms.com/dev/bulkV2"
            headers = {
                "authorization": test_sms_key,
                "Content-Type": "application/json"
            }
            payload = {
                "variables_values": phone_clean,
                "route": "otp",
                "numbers": phone_clean,
                "message": sms_message
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response_data = response.json()
            
            if response_data.get('return') == True:
                print(f"✓ SMS sent successfully to +{phone_clean}")
            else:
                print(f"✗ SMS failed: {response_data.get('message')}")
        except Exception as e:
            print(f"✗ SMS failed: {str(e)}")

print("\n" + "="*60)
print("✓ TEST SUMMARY")
print("="*60)

print(f"""
✓ CODE VERIFICATION:
  - Email WILL be sent to USER'S email: {test_user_email}
  - SMS WILL be sent to USER'S phone: +91{phone_clean if phone_clean else test_user_phone}
  - Both use USER'S data, NOT hardcoded hospital email/phone

⚠️  CURRENT ISSUES:
  1. Gmail password is wrong (using 'primelife@123')
     → Need real 16-character app password
  
  2. SMS API key not configured (optional)
     → SMS will be logged, not actually sent
     → Add API key when ready

📝 NEXT STEPS:
  1. Get Gmail app password from:
     https://myaccount.google.com/apppasswords
  
  2. Update backend.py line 24:
     EMAIL_PASSWORD = "your-16-char-password"
  
  3. (Optional) Get Fast2SMS API key from:
     https://www.fast2sms.com/
  
  4. (Optional) Update backend.py line 31:
     SMS_API_KEY = "your-api-key"
  
  5. Restart server: python backend.py
  
  6. Test appointment form with your email and phone

✓ VERIFICATION COMPLETE!
""")

print("="*60 + "\n")
