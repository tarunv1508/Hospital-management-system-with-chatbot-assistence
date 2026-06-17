# Email & SMS Configuration Guide

## Overview
This application sends appointment confirmations via **Email** and **SMS**. Follow the steps below to set up both services.

---

## 1. EMAIL CONFIGURATION (Gmail SMTP)

### Step 1: Enable 2-Factor Authentication in Gmail
1. Go to https://myaccount.google.com/
2. Click on **Security** in the left menu
3. Enable **2-Step Verification** if not already enabled

### Step 2: Generate App Password
1. Go to https://myaccount.google.com/apppasswords
2. Select **Mail** and **Windows Computer**
3. Click **Generate**
4. Copy the 16-character password shown

### Step 3: Update backend.py
Open `backend.py` and find these lines (around line 25):

```python
# Email Configuration - Gmail SMTP
EMAIL_ADDRESS = "primelifehospital@gmail.com"
EMAIL_PASSWORD = "primelife@123"  # Use app-specific password for Gmail
```

Replace with:
```python
# Email Configuration - Gmail SMTP
EMAIL_ADDRESS = "your-email@gmail.com"
EMAIL_PASSWORD = "your-16-char-app-password"
```

**Example:**
```python
EMAIL_ADDRESS = "hospital@gmail.com"
EMAIL_PASSWORD = "abcd efgh ijkl mnop"  # 16-character app password from step 2
```

### Step 4: Test Email
Email will automatically send when a user submits an appointment form.

✓ **Email is now configured!**

---

## 2. SMS CONFIGURATION (Fast2SMS - Optional but Recommended)

### Option A: With Fast2SMS API (Recommended for India)

#### Step 1: Create Fast2SMS Account
1. Visit: https://www.fast2sms.com/
2. Sign up for a free account
3. Verify your phone number
4. Go to **Dashboard** → **API**
5. Copy your **API Key**

#### Step 2: Update backend.py
Open `backend.py` and find these lines (around line 30-31):

```python
# SMS Configuration - Fast2SMS (Popular in India)
SMS_API_KEY = "YOUR_FAST2SMS_API_KEY"  # Replace with your Fast2SMS API key
SMS_PROVIDER = "fast2sms"  # Options: 'fast2sms', 'log_only'
```

Replace with:
```python
# SMS Configuration - Fast2SMS (Popular in India)
SMS_API_KEY = "your-fast2sms-api-key-here"
SMS_PROVIDER = "fast2sms"
```

**Example:**
```python
SMS_API_KEY = "5a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p"
SMS_PROVIDER = "fast2sms"
```

#### Step 3: Test SMS
SMS will automatically send when a user submits an appointment form.

✓ **SMS is now configured!**

---

### Option B: Without API Key (Testing/Logging Mode)

If you don't want to use Fast2SMS yet, the system will log the SMS message that would be sent.

Keep the default configuration:
```python
SMS_API_KEY = "YOUR_FAST2SMS_API_KEY"  # Not configured
SMS_PROVIDER = "fast2sms"
```

The SMS will be logged (shown in console) but not actually sent. You can upgrade to actual SMS sending later by adding the API key.

✓ **SMS Logging is active!**

---

## 3. OTHER SMS SERVICE OPTIONS

If you prefer a different SMS service, you can integrate:

### Option 1: Twilio
```bash
pip install twilio
```
- Visit: https://www.twilio.com/
- Get phone number and API credentials
- Modify the `send_sms_notification()` function in `backend.py`

### Option 2: AWS SNS
- AWS account required
- Visit: https://aws.amazon.com/sns/
- Set up credentials in `backend.py`

### Option 3: Other Indian SMS Providers
- **MSG91**: https://msg91.com/
- **Nexmo/Vonage**: https://www.vonage.com/
- **Sms2Reach**: https://www.sms2reach.com/

---

## 4. TESTING THE SYSTEM

### Test Email & SMS
1. Start the Flask server: `python backend.py`
2. Open appointment form: `http://localhost:5000/appointment.html`
3. Fill in the form with:
   - Name: John Doe
   - Email: your-email@gmail.com
   - Phone: 9876543210 (your actual phone)
   - Department: Cardiology
   - Doctor: DR.S.Arjun Reddy
   - Date: 2026-06-20
4. Click **"Book Appointment Now"**

### Expected Results:

#### Email
- Check your inbox at `your-email@gmail.com`
- Look for email from `primelifehospital@gmail.com`
- Subject: "PrimeLife Hospital - Appointment Confirmation"
- Contains formatted HTML email with appointment details

#### SMS
- With API Key: SMS will be received on your phone within 30 seconds
- Without API Key: Check server console for SMS message

### Check Server Console
Look for messages like:
```
✓ EMAIL SENT: Confirmation email successfully sent to user@example.com
✓ SMS SENT: SMS successfully sent to +919876543210
```

---

## 5. TROUBLESHOOTING

### Email Not Sending

**Error: "Gmail authentication failed"**
- Check if EMAIL_ADDRESS is correct
- Verify EMAIL_PASSWORD is the 16-character app password (not your Gmail password)
- Ensure 2-Factor Authentication is enabled on Gmail
- Go to https://myaccount.google.com/apppasswords and regenerate if needed

**Error: "SMTP error"**
- Ensure port 465 is not blocked by firewall
- Check internet connection
- Verify Gmail credentials again

### SMS Not Sending

**SMS only logging (no actual send)**
- This is normal if API_KEY is not configured
- Add Fast2SMS API key to enable actual SMS sending
- Or choose a different SMS provider

**Error: "Invalid phone number"**
- Ensure phone number starts with 9 and has 10 digits (e.g., 9876543210)
- Or include country code +91 (e.g., +919876543210)

**Error: "Network error from Fast2SMS"**
- Check internet connection
- Verify API key is correct
- Check Fast2SMS dashboard for any issues

---

## 6. PRODUCTION SETTINGS

When deploying to production:

1. **Never hardcode credentials in code**
2. Use environment variables:
   ```python
   import os
   EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', 'primelifehospital@gmail.com')
   EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
   SMS_API_KEY = os.getenv('SMS_API_KEY', '')
   ```

3. Set environment variables on your server:
   ```bash
   export EMAIL_ADDRESS="hospital@gmail.com"
   export EMAIL_PASSWORD="abcd efgh ijkl mnop"
   export SMS_API_KEY="your-fast2sms-key"
   ```

4. Use HTTPS for secure transmission

---

## 7. MONITORING

Monitor sent emails and SMS in the application logs:
```bash
tail -f application.log
```

Look for:
- ✓ EMAIL SENT
- ✓ SMS SENT
- ✗ EMAIL FAILED
- ✗ SMS FAILED

---

## 8. FAQ

**Q: Will this cost money?**
- Email (Gmail): Free
- SMS (Fast2SMS): Paid after free credits (₹0.50-2 per SMS in India)
- SMS (Testing): Free (logs only, no actual send)

**Q: Can I use my personal Gmail?**
- Yes, but recommended to use a hospital email account
- Create a dedicated Gmail for PrimeLife Hospital

**Q: How long does email take to arrive?**
- Usually instant (within 5 seconds)
- Max delay: 5 minutes

**Q: How long does SMS take to arrive?**
- Instant (within 30 seconds)
- Depends on SMS provider and carrier

**Q: Can I customize the email template?**
- Yes! Edit the `send_email_notification()` function in `backend.py`
- Modify the HTML template as needed

---

## 9. QUICK START CHECKLIST

- [ ] Enable 2-Factor Authentication in Gmail
- [ ] Generate App Password from Gmail
- [ ] Update EMAIL_ADDRESS in backend.py
- [ ] Update EMAIL_PASSWORD in backend.py with app password
- [ ] (Optional) Create Fast2SMS account
- [ ] (Optional) Add SMS_API_KEY to backend.py
- [ ] Test with sample appointment form
- [ ] Verify email arrives at test email
- [ ] Verify SMS arrives at test phone (if API key added)

---

## 10. SUPPORT

If you need help:
1. Check the troubleshooting section above
2. Review server console logs
3. Verify credentials are correct
4. Try the test appointment again

---

**Version:** 1.0  
**Last Updated:** 2026-06-15  
**System:** PrimeLife Hospital Management
