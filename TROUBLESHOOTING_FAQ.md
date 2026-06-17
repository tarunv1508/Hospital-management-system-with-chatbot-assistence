# 🆘 TROUBLESHOOTING & FAQ

---

## ❓ FREQUENTLY ASKED QUESTIONS

### Q1: Will this work without Gmail credentials?
**A:** No. Email sending requires Gmail SMTP configuration. SMS can work without credentials (will just log).

### Q2: Is SMS sending free?
**A:** 
- Email (Gmail): Free
- SMS (Fast2SMS): Paid (₹0.50-2 per SMS in India), but has free trial credits
- SMS (Logging mode): Free for testing

### Q3: Do I need to use Fast2SMS or can I use another SMS provider?
**A:** You can use any SMS provider. See SETUP_EMAIL_SMS.md for alternatives:
- Twilio
- AWS SNS
- MSG91
- Nexmo/Vonage
- Others

### Q4: What happens if email/SMS fails?
**A:** The system logs the error and returns error details. User sees an error message. Appointment is still saved in database.

### Q5: Can users edit their appointment after booking?
**A:** Currently no - you would need to add an edit feature. Users must call hospital to cancel/reschedule.

### Q6: How long does email take to arrive?
**A:** Usually instant (5-10 seconds). Max delay is 5 minutes due to email routing.

### Q7: How long does SMS take to arrive?
**A:** Usually 10-30 seconds. Depends on carrier and network.

### Q8: Can I customize the email template?
**A:** Yes! Edit the HTML in the `send_email_notification()` function in backend.py (lines 45-191).

### Q9: Can I add more SMS providers?
**A:** Yes! You can modify the `send_sms_notification()` function to support additional providers.

### Q10: What if user enters wrong email address?
**A:** System validates email format before sending. If invalid, returns error. Appointment not saved.

### Q11: What if user enters wrong phone number?
**A:** SMS function will try to format it. If invalid format, returns error. But appointment was already saved in DB.

### Q12: Is my data secure?
**A:** 
- Email uses Gmail SMTP SSL (encrypted)
- SMS uses HTTPS to Fast2SMS API (encrypted)
- Database credentials in DB_CONFIG
- Keep credentials in environment variables in production

### Q13: Can I test without actually sending emails?
**A:** Yes, comment out the email/SMS calls in appointment.html temporarily.

### Q14: Why isn't email sending but SMS is?
**A:** Check Gmail credentials. Email configuration is separate from SMS.

### Q15: Can I send emails in bulk?
**A:** The system sends one at a time (when appointment is made). For bulk campaigns, need separate code.

---

## 🐛 COMMON ERRORS & SOLUTIONS

### ERROR 1: "Gmail authentication failed"

**Symptom:**
```
✗ EMAIL FAILED: Gmail authentication failed. 
Please check EMAIL_ADDRESS and EMAIL_PASSWORD in backend.py
```

**Cause:** Wrong email or password

**Solutions:**
1. ✅ Use 16-character APP PASSWORD (not Gmail password)
2. ✅ Get from: https://myaccount.google.com/apppasswords
3. ✅ Ensure 2-Factor Authentication is enabled
4. ✅ Verify EMAIL_ADDRESS matches Gmail account

**Step-by-step fix:**
```bash
1. Go to: https://myaccount.google.com/
2. Click Security → 2-Step Verification (enable if needed)
3. Go to: https://myaccount.google.com/apppasswords
4. Select "Mail" and "Windows Computer"
5. Click Generate
6. Copy the 16-character password
7. Update backend.py:
   EMAIL_PASSWORD = "xxxx xxxx xxxx xxxx"
8. Restart server: python backend.py
```

---

### ERROR 2: "Invalid appointment date"

**Symptom:**
```
✗ Error: Invalid appointment date.
```

**Cause:** Wrong date format or past date

**Solutions:**
1. ✅ Use date picker (not manual typing)
2. ✅ Select future date (not past date)
3. ✅ Format must be YYYY-MM-DD (e.g., 2026-06-20)

**Check:**
- Date must be >= today's date
- Use calendar picker, not text input
- Don't use 01/20/2026, use 2026-06-20

---

### ERROR 3: "Email and SMS show as 'sent' but user didn't receive"

**Symptom:**
- Form shows "✓ Email sent" and "✓ SMS sent"
- But user didn't receive them

**Cause:** Several possibilities

**Solutions:**

**For Email:**
1. ✅ Check spam/junk folder
2. ✅ Verify email address was correct
3. ✅ Check Gmail account isn't rate-limited
4. ✅ Check firewall isn't blocking port 465
5. ✅ Check internet connection

**For SMS:**
1. ✅ Check if SMS API key is actually configured
2. ✅ Verify phone number format (10 or 11 digits, starts with 9)
3. ✅ Check carrier (some carriers block bulk SMS initially)
4. ✅ Check Fast2SMS account has credits

---

### ERROR 4: "SMS only logging, not actually sending"

**Symptom:**
```
✓ SMS READY TO SEND: To enable actual SMS, configure Fast2SMS API key
```

**Cause:** API key not configured

**Solution:**
1. ✅ Create Fast2SMS account: https://www.fast2sms.com/
2. ✅ Get API key from Dashboard
3. ✅ Update backend.py:
   ```python
   SMS_API_KEY = "your-actual-api-key"
   ```
4. ✅ Restart server
5. ✅ Test again

---

### ERROR 5: "Invalid phone number format"

**Symptom:**
```
✗ SMS FAILED: Invalid phone number format
```

**Cause:** Phone number in wrong format

**Solutions:**
1. ✅ Use format: 9876543210 (10 digits)
2. ✅ Or use format: 919876543210 (12 digits with country code)
3. ✅ Or use format: +919876543210 (with +)
4. ✅ Don't use: (987) 654-3210 or 987-654-3210

**Correct formats:**
- 9876543210 ✓
- 919876543210 ✓
- +919876543210 ✓

**Incorrect formats:**
- 098 7654 3210 ✗
- (987) 654-3210 ✗
- 987-654-3210 ✗
- 91-9876543210 ✗

---

### ERROR 6: "SMTP error - connection failed"

**Symptom:**
```
✗ EMAIL FAILED: SMTP error - connection failed
```

**Cause:** Network issue or port blocked

**Solutions:**
1. ✅ Check internet connection
2. ✅ Check port 465 is not blocked by firewall
3. ✅ Try again (might be temporary)
4. ✅ Check Gmail isn't rate-limiting

**To test connection:**
```bash
# Windows PowerShell
Test-NetConnection smtp.gmail.com -Port 465

# Should show: TcpTestSucceeded: True
```

---

### ERROR 7: "All required fields must be filled"

**Symptom:**
```
✗ Error: All required fields must be filled.
```

**Cause:** One or more form fields empty

**Solutions:**
1. ✅ Fill all required fields (marked with *)
2. ✅ Name field: Can't be empty
3. ✅ Email field: Can't be empty
4. ✅ Phone field: Can't be empty
5. ✅ Department field: Must select from dropdown
6. ✅ Doctor field: Must select from dropdown
7. ✅ Date field: Must select date
8. ✅ Notes field: Optional (can be empty)

---

### ERROR 8: "Email is invalid"

**Symptom:**
```
✗ Error: Email is invalid.
```

**Cause:** Email not in correct format

**Solutions:**
1. ✅ Use format: name@domain.com
2. ✅ Valid: user@example.com ✓
3. ✅ Valid: john.doe@company.co.uk ✓
4. ✅ Invalid: user@.com ✗
5. ✅ Invalid: @example.com ✗
6. ✅ Invalid: user@domain ✗

---

### ERROR 9: "Database error: Unable to connect"

**Symptom:**
```
✗ Error: Unable to connect to the database.
```

**Cause:** MySQL not running or wrong credentials

**Solutions:**
1. ✅ Start MySQL service:
   ```bash
   # Windows: Services → MySQL → Start
   # Or: mysql -u root -p
   ```
2. ✅ Check credentials in backend.py:
   ```python
   DB_CONFIG = {
       "host": "localhost",
       "user": "root",
       "password": "your-password",
       "database": "hospital_contact",
   }
   ```
3. ✅ Verify database exists:
   ```bash
   mysql -u root -p
   SHOW DATABASES;
   ```

---

### ERROR 10: "Form won't submit"

**Symptom:** Click button but nothing happens

**Cause:** JavaScript error or validation issue

**Solutions:**
1. ✅ Check browser console (F12 → Console)
2. ✅ Fill all required fields
3. ✅ Check internet connection
4. ✅ Check form has `id="appointment-form"`
5. ✅ Check backend server is running

---

## ⚙️ ADVANCED TROUBLESHOOTING

### Check Backend Logs

**Windows PowerShell:**
```powershell
python backend.py 2>&1 | Tee-Object -FilePath app.log
# View: Get-Content app.log -Tail 50
```

**Linux/Mac:**
```bash
python backend.py 2>&1 | tee app.log
# View: tail -f app.log
```

---

### Test Gmail SMTP Manually

```python
import smtplib
from email.mime.text import MIMEText

email = "your-email@gmail.com"
password = "16-char-app-password"

try:
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(email, password)
        print("✓ Gmail authentication successful!")
except Exception as e:
    print(f"✗ Error: {e}")
```

---

### Test Fast2SMS API Manually

```python
import requests

api_key = "your-fast2sms-api-key"
phone = "919876543210"  # with country code

url = "https://www.fast2sms.com/dev/bulkV2"
headers = {"authorization": api_key}
payload = {
    "numbers": phone,
    "message": "Test message from PrimeLife Hospital",
    "route": "otp"
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

---

### Check Database Records

```bash
mysql -u root -p hospital_contact

# View all appointments
SELECT * FROM appointment_requests;

# View latest appointment
SELECT * FROM appointment_requests ORDER BY id DESC LIMIT 1;

# Check if appointment was saved even if email failed
SELECT * FROM appointment_requests WHERE email = 'user@example.com';
```

---

## 📊 DIAGNOSTIC CHECKLIST

Run through these checks if something isn't working:

### Backend Server
- [ ] Python 3.7+ installed (`python --version`)
- [ ] Flask running (`python backend.py` shows no errors)
- [ ] Port 5000 accessible
- [ ] No other app on port 5000 (`netstat -ano | findstr :5000`)

### Email Configuration
- [ ] Gmail account exists
- [ ] 2-Factor Authentication enabled
- [ ] App password generated
- [ ] EMAIL_ADDRESS in backend.py
- [ ] EMAIL_PASSWORD in backend.py (16-char app password)
- [ ] Internet connection working
- [ ] Port 465 not blocked

### SMS Configuration (Optional)
- [ ] Fast2SMS account created (if using)
- [ ] API key obtained (if using)
- [ ] SMS_API_KEY in backend.py (if using)
- [ ] Phone number format correct

### Database
- [ ] MySQL running
- [ ] Database "hospital_contact" exists
- [ ] Tables exist (`appointment_requests`, etc.)
- [ ] Credentials correct in backend.py

### Frontend
- [ ] HTML file opens without errors
- [ ] Form fields visible
- [ ] Submit button clickable
- [ ] Console (F12) shows no errors

### Test Submission
- [ ] Fill all form fields
- [ ] Phone number format: 10 digits
- [ ] Email format: valid@example.com
- [ ] Future date selected
- [ ] Click "Book Appointment"
- [ ] Wait for response (may take 5-10 seconds)

---

## 🎯 STEP-BY-STEP TEST PROCEDURE

### Full Test (10-15 minutes)

1. **Start Server**
   ```bash
   python backend.py
   ```
   Look for: `Running on http://127.0.0.1:5000`

2. **Open Browser**
   ```
   http://localhost:5000/appointment.html
   ```

3. **Fill Form**
   - Name: `Test User`
   - Email: `your-actual-email@gmail.com`
   - Phone: `9876543210` (or your actual phone)
   - Department: `Cardiology`
   - Doctor: `DR.S.Arjun Reddy`
   - Date: `2026-06-25`

4. **Submit**
   - Click "Book Appointment Now"
   - Wait 3-5 seconds for response

5. **Check Results**
   - ✓ Success message shows appointment ID
   - ✓ Email status shows
   - ✓ SMS status shows

6. **Verify Email**
   - Check inbox (refresh)
   - Look for from: `primelifehospital@gmail.com`
   - Subject: `PrimeLife Hospital - Appointment Confirmation`
   - Should arrive within 30 seconds

7. **Verify SMS** (if API key added)
   - Check phone messages
   - Should arrive within 30 seconds
   - Contains appointment ID and doctor name

8. **Check Database**
   ```bash
   mysql -u root -p hospital_contact
   SELECT * FROM appointment_requests ORDER BY id DESC LIMIT 1;
   ```
   Verify appointment is saved

---

## 💡 TIPS FOR SUCCESS

✓ **Use app password for Gmail, not Gmail password**  
✓ **Test with real phone and email**  
✓ **Check spam folder if email doesn't arrive**  
✓ **Use correct date format in date picker**  
✓ **Ensure MySQL is running before starting server**  
✓ **Check server console for error messages**  
✓ **Restart server after updating credentials**  
✓ **Test one thing at a time (email first, then SMS)**  
✓ **Keep logs for debugging issues later**  
✓ **Use environment variables in production**  

---

## 📞 GETTING MORE HELP

If you're still stuck:

1. **Check all setup files:**
   - QUICK_SETUP.txt
   - SETUP_EMAIL_SMS.md
   - IMPLEMENTATION_SUMMARY.md

2. **Review examples:**
   - EXAMPLES.md (What users will see)

3. **Check error messages:**
   - Server console (shows exact errors)
   - Browser console (F12 → Console)
   - Database logs

4. **Test individually:**
   - Email only (disable SMS)
   - SMS only (if email works)
   - Database (check MySQL)

5. **Verify credentials:**
   - Gmail credentials (EMAIL_ADDRESS, EMAIL_PASSWORD)
   - Fast2SMS API key (if using)
   - MySQL credentials (DB_CONFIG)

---

**Last Updated:** June 15, 2026  
**System Version:** 2.0  
**Support:** See all .md files in project directory
