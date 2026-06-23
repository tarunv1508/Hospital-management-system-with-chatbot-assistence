from flask import Flask, request, jsonify, session, make_response, redirect, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
from typing import Optional
import os
import re
import json
import ssl
import bcrypt
import jwt
import mysql.connector
import logging
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'healthcare_chatbot_secret_key_2024')
JWT_SECRET = os.getenv('JWT_SECRET', 'healthcare_jwt_secret_2024')
JWT_ALGORITHM = 'HS256'
JWT_EXPIRATION_SECONDS = 3600

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

HOSPITAL_PHONE = "+919866208819"


def load_env_file(path=".env"):
    if not os.path.exists(path):
        return

    app.logger.info(f"Loading environment variables from {path}")
    with open(path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


load_env_file()

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "varma1508",
    "database": "hospital_contact",
}

SMTP_USER = os.getenv("SMTP_USER") or os.getenv("EMAIL_ADDRESS")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or os.getenv("EMAIL_PASSWORD")
SMTP_FROM_ADDRESS = os.getenv("SMTP_FROM_ADDRESS") or (f"PrimeLife Hospital <{SMTP_USER}>")
SMTP_FROM_EMAIL = os.getenv("SMTP_FROM_EMAIL") or SMTP_USER

SMTP_CONFIG = {
    "host": os.getenv("SMTP_HOST", "smtp.gmail.com"),
    "port": int(os.getenv("SMTP_PORT", "587")),
    "user": SMTP_USER,
    "password": SMTP_PASSWORD,
    "from_address": SMTP_FROM_ADDRESS,
    "from_email": SMTP_FROM_EMAIL,
}

if not SMTP_CONFIG["user"] or not SMTP_CONFIG["password"]:
    app.logger.warning(
        "SMTP credentials are not configured. Set SMTP_USER/EMAIL_ADDRESS and SMTP_PASSWORD/EMAIL_PASSWORD environment variables."
    )

if not SMTP_CONFIG["from_address"]:
    SMTP_CONFIG["from_address"] = f"PrimeLife Hospital <{SMTP_CONFIG['user']}>"


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _format_sql_date(value):
    if value is None:
        return None
    try:
        return value.strftime("%Y-%m-%d")
    except Exception:
        try:
            return str(value)
        except Exception:
            return None


def _format_sql_time(value):
    if value is None:
        return None
    # MySQL TIME can be returned as datetime.time or datetime.timedelta depending on connector
    try:
        # datetime.time and datetime.datetime have strftime
        return value.strftime("%H:%M")
    except Exception:
        pass
    if isinstance(value, timedelta):
        total = int(value.total_seconds())
        hh = (total // 3600) % 24
        mm = (total % 3600) // 60
        return f"{hh:02d}:{mm:02d}"
    try:
        return str(value)
    except Exception:
        return None


def verify_admin_credentials(username: str, password: str) -> bool:
    conn = get_db_connection()
    if not conn or not conn.is_connected():
        app.logger.error("Unable to connect to DB while verifying admin credentials.")
        return False

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, username, passwordHash FROM Admin WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        if not user:
            return False
        stored_hash = user["passwordHash"].encode("utf-8")
        return bcrypt.checkpw(password.encode("utf-8"), stored_hash)
    except mysql.connector.Error as err:
        app.logger.error(f"Admin login query failed: {err}")
        return False
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


def create_jwt_token(admin_id: int, username: str) -> str:
    payload = {
        "admin_id": admin_id,
        "username": username,
        "exp": datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION_SECONDS),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def verify_jwt_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def admin_required() -> bool:
    token = request.cookies.get("admin_token")
    if not token:
        return False
    payload = verify_jwt_token(token)
    if not payload:
        return False
    request.admin_payload = payload
    return True


def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        app.logger.error(f"DB connection failed: {err}")
        return None


def send_appointment_confirmation_email(to_email, appointment_data):
    subject = "PrimeLife Hospital Appointment Confirmation"
    body = (
        f"Dear {appointment_data['name']},\n\n"
        f"Your appointment has been confirmed with PrimeLife Hospital. Here are the details:\n\n"
        f"Appointment ID: {appointment_data['appointment_id']}\n"
        f"Department: {appointment_data['department']}\n"
        f"Doctor: {appointment_data['doctor']}\n"
        f"Date: {appointment_data['appointment_date']}\n"
        f"Phone: {appointment_data['phone']}\n"
        f"Notes: {appointment_data['notes'] or 'N/A'}\n\n"
        "Please arrive 15 minutes before your scheduled time. If you need to reschedule, reply to this email or call us at "
        f"{HOSPITAL_PHONE}.\n\n"
        "Thank you for choosing PrimeLife Hospital.\n"
        "Best regards,\n"
        "PrimeLife Hospital Team"
    )

    if not SMTP_CONFIG["user"] or not SMTP_CONFIG["password"]:
        raise ValueError(
            "SMTP credentials are missing. Set SMTP_USER/EMAIL_ADDRESS and SMTP_PASSWORD/EMAIL_PASSWORD."
        )

    message = MIMEText(body)
    message["Subject"] = subject
    message["From"] = SMTP_CONFIG["from_address"]
    message["To"] = to_email
    envelope_from = SMTP_CONFIG["from_email"] or SMTP_CONFIG["user"]

    context = ssl.create_default_context()
    app.logger.info(f"Connecting to SMTP server {SMTP_CONFIG['host']}:{SMTP_CONFIG['port']} as {SMTP_CONFIG['user']}")

    with smtplib.SMTP(SMTP_CONFIG["host"], SMTP_CONFIG["port"]) as server:
        server.ehlo()
        server.starttls(context=context)
        server.ehlo()
        server.login(SMTP_CONFIG["user"], SMTP_CONFIG["password"])
        server.sendmail(envelope_from, [to_email], message.as_string())
        app.logger.info(f"Appointment confirmation email sent to {to_email}")

# Doctor roster and symptom mapping - Comprehensive dataset
DOCTORS = {
    "cardiology": ["DR.S.Arjun Reddy", "DR.Rajesh Kumar", "DR.Vikram Singh"],
    "neurology": ["DR.S.SaiPriya", "DR.T.Anu", "DR.Neha Sharma"],
    "pediatrics": ["DR.N.MadhuLatha", "DR.Priya Verma", "DR.Arun Nair"],
    "orthopedics": ["DR.M.Sameer", "DR.Ravi Patel", "DR.Suresh Gupta"],
    "dermatology": ["DR.N.lohith", "DR.Anjali Singh", "DR.Meera Joshi"],
    "oncology": ["DR.T.Anu", "DR.Ashok Kumar", "DR.Sneha Desai"],
    "general_medicine": ["DR.S.Arjun Reddy", "DR.Ramesh Kumar", "DR.Pooja Menon"],
    "ent": ["DR.Vikram Sharma", "DR.Anand Gupta", "DR.Shruti Patel"],
    "gastroenterology": ["DR.Rohit Verma", "DR.Priya Singh", "DR.Aditya Sengupta"],
    "nephrology": ["DR.Sanjay Kumar", "DR.Meera Nair", "DR.Rajiv Desai"],
    "urology": ["DR.Harsh Patel", "DR.Vikas Sharma", "DR.Amit Singh"],
    "pulmonology": ["DR.Deepak Verma", "DR.Sneha Kumar", "DR.Arjun Sharma"],
    "endocrinology": ["DR.Divya Singh", "DR.Ashok Nair", "DR.Priya Gupta"],
    "gynecology": ["DR.Ragini Sharma", "DR.Neha Verma", "DR.Anjali Patel"],
    "psychiatry": ["DR.Ramesh Singh", "DR.Anjali Kumar", "DR.Vikram Desai"],
    "general": ["DR.S.Arjun Reddy", "DR.Ramesh Kumar", "DR.Pooja Menon", "DR.Vikram Singh", "DR.S.SaiPriya", "DR.N.MadhuLatha"]
}

SYMPTOM_KEYWORDS = {
    # Cardiology
    "chest pain": "cardiology",
    "heart palpitations": "cardiology",
    "shortness of breath": "cardiology",
    "high blood pressure": "cardiology",
    "high bp": "cardiology",
    "irregular heartbeat": "cardiology",
    "cardiac": "cardiology",
    
    # Neurology
    "headache": "neurology",
    "headach": "neurology",
    "head ache": "neurology",
    "migraine": "neurology",
    "numbness": "neurology",
    "dizziness": "neurology",
    "seizure": "neurology",
    "stroke": "neurology",
    "brain": "neurology",
    "nerve pain": "neurology",
    "tremor": "neurology",
    "pressure in my head": "neurology",
    "pain in my head": "neurology",
    "feeling dizzy": "neurology",
    
    # Dermatology
    "skin rash": "dermatology",
    "acne": "dermatology",
    "itchy skin": "dermatology",
    "eczema": "dermatology",
    "allergies": "dermatology",
    "skin infection": "dermatology",
    "hives": "dermatology",
    "psoriasis": "dermatology",
    
    # ENT
    "ear pain": "ent",
    "throat infection": "ent",
    "sinus": "ent",
    "sore throat": "ent",
    "nasal": "ent",
    "hearing loss": "ent",
    "ear infection": "ent",
    "tonsil": "ent",
    
    # Gastroenterology
    "stomach pain": "gastroenterology",
    "tummy pain": "gastroenterology",
    "acidity": "gastroenterology",
    "digesting": "gastroenterology",
    "digestion": "gastroenterology",
    "not digesting": "gastroenterology",
    "food not digesting": "gastroenterology",
    "food is not digesting": "gastroenterology",
    "cant digest": "gastroenterology",
    "cannot digest": "gastroenterology",
    "stomach upset": "gastroenterology",
    "feeling sick": "gastroenterology",
    "acid reflux": "gastroenterology",
    "gastric": "gastroenterology",
    "heartburn": "gastroenterology",
    "indigestion": "gastroenterology",
    "ulcer": "gastroenterology",
    "abdominal pain": "gastroenterology",
    "bloated": "gastroenterology",
    "bloating": "gastroenterology",
    
    # Orthopedics
    "joint pain": "orthopedics",
    "broken bone": "orthopedics",
    "arthritis": "orthopedics",
    "back pain": "orthopedics",
    "fracture": "orthopedics",
    "bone pain": "orthopedics",
    "sprain": "orthopedics",
    "muscle pain": "orthopedics",
    
    # Nephrology
    "kidney": "nephrology",
    "kidney problems": "nephrology",
    "urine infection": "nephrology",
    "renal": "nephrology",
    
    # Urology
    "urinary": "urology",
    "urinary issues": "urology",
    "prostate": "urology",
    "prostate problems": "urology",
    "bladder": "urology",
    
    # Pulmonology
    "breathing difficulty": "pulmonology",
    "asthma": "pulmonology",
    "lung infection": "pulmonology",
    "lung": "pulmonology",
    "cough": "pulmonology",
    "bronchitis": "pulmonology",
    "pneumonia": "pulmonology",
    "respiratory": "pulmonology",
    
    # Endocrinology
    "diabetes": "endocrinology",
    "thyroid": "endocrinology",
    "hormonal": "endocrinology",
    "hormonal imbalance": "endocrinology",
    "thyroid issues": "endocrinology",
    "blood sugar": "endocrinology",
    
    # Gynecology & Obstetrics
    "pregnancy": "gynecology",
    "menstrual": "gynecology",
    "menstrual problems": "gynecology",
    "gynecology": "gynecology",
    "obstetrics": "gynecology",
    "womens health": "gynecology",
    
    # Pediatrics
    "baby": "pediatrics",
    "child": "pediatrics",
    "vaccination": "pediatrics",
    "pediatric": "pediatrics",
    "infant": "pediatrics",
    
    # Psychiatry
    "mental stress": "psychiatry",
    "anxiety": "psychiatry",
    "depression": "psychiatry",
    "psychiatric": "psychiatry",
    "mental health": "psychiatry",
    "stress": "psychiatry",
    
    # Oncology
    "cancer": "oncology",
    "lump": "oncology",
    "weight loss": "oncology",
    "tumor": "oncology",
    "uncontrolled cell growth": "oncology",
    
    # General Medicine
    "fever": "general_medicine",
    "cold": "general_medicine",
    "general weakness": "general_medicine",
    "fatigue": "general_medicine",
    "weakness": "general_medicine",
    "nausea": "general_medicine",
    "vomiting": "general_medicine",
    "diarrhea": "general_medicine",
    "feeling sick": "general_medicine",
    "not feeling well": "general_medicine",
    "i feel sick": "general_medicine",
    "i am not well": "general_medicine",
}


from collections import defaultdict


def normalize_text(text: str) -> str:
    normalized = re.sub(r"[^a-z0-9 ]", " ", text.lower())
    normalized = re.sub(r"\s+", " ", normalized).strip()
    return normalized


def identify_department_scores(symptoms_text: str) -> dict:
    text = normalize_text(symptoms_text)
    scores = defaultdict(int)

    # Match longer phrases first to reduce generic fallback matches.
    for keyword in sorted(SYMPTOM_KEYWORDS.keys(), key=lambda k: -len(k)):
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, text):
            dept = SYMPTOM_KEYWORDS[keyword]
            scores[dept] += 2 if len(keyword.split()) > 1 else 1

    # Boost departments when the user mentions a known disease or condition name.
    for disease, dept in DISEASE_MAPPING.items():
        pattern = r"\b" + re.escape(disease) + r"\b"
        if re.search(pattern, text):
            scores[dept] += 3

    if not scores:
        # Fallback: match partial symptom tokens to common departments.
        tokens = set(text.split())
        fallback_tokens = {
            "head": "neurology",
            "headache": "neurology",
            "headach": "neurology",
            "dizzy": "neurology",
            "food": "gastroenterology",
            "digest": "gastroenterology",
            "stomach": "gastroenterology",
            "tummy": "gastroenterology",
            "sick": "general_medicine",
            "nausea": "general_medicine",
            "fever": "general_medicine",
            "weakness": "general_medicine",
            "fatigue": "general_medicine",
            "vomit": "general_medicine",
            "pain": "general_medicine",
            "blood": "gastroenterology",
            "stool": "gastroenterology",
            "vomiting": "general_medicine",
            "bloating": "gastroenterology",
            "bloated": "gastroenterology",
            "cough": "pulmonology",
            "breath": "pulmonology",
            "breathing": "pulmonology",
            "joint": "orthopedics",
            "bone": "orthopedics",
            "skin": "dermatology",
            "rash": "dermatology",
            "swelling": "orthopedics",
            "kidney": "nephrology",
            "urine": "urology",
            "menstrual": "gynecology",
            "pregnancy": "gynecology",
            "anxiety": "psychiatry",
            "depression": "psychiatry",
        }
        for token, dept in fallback_tokens.items():
            if token in tokens:
                scores[dept] += 1

    return dict(scores)


DEPARTMENT_PRIORITY = [
    "cardiology",
    "neurology",
    "oncology",
    "orthopedics",
    "dermatology",
    "ent",
    "gastroenterology",
    "nephrology",
    "urology",
    "pulmonology",
    "endocrinology",
    "gynecology",
    "psychiatry",
    "pediatrics",
    "general_medicine",
    "general",
]


# Disease/Condition mapping to departments
DISEASE_MAPPING = {
    "heart disease": "cardiology",
    "hypertension": "cardiology",
    "arrhythmia": "cardiology",
    "migraine": "neurology",
    "parkinson": "neurology",
    "epilepsy": "neurology",
    "fracture": "orthopedics",
    "arthritis": "orthopedics",
    "psoriasis": "dermatology",
    "eczema": "dermatology",
    "leukemia": "oncology",
    "bronchitis": "pulmonology",
    "asthma": "pulmonology",
    "diabetes": "endocrinology",
    "thyroid disorder": "endocrinology",
    "gastritis": "gastroenterology",
    "ulcer": "gastroenterology",
    "kidney disease": "nephrology",
    "prostate": "urology",
    "ent infection": "ent",
    "women health": "gynecology",
    "anxiety": "psychiatry",
    "depression": "psychiatry",
}

def get_matching_departments(scores: dict) -> list:
    """Return all matching departments sorted by relevance score"""
    if not scores:
        return ["general"]
    
    sorted_depts = sorted(scores.items(), key=lambda x: -x[1])
    return [dept for dept, _ in sorted_depts]

def pick_best_department(scores: dict) -> str:
    """Pick the single best department from all matches"""
    if not scores:
        return "general"

    max_score = max(scores.values())
    candidate_departments = [d for d, v in scores.items() if v == max_score]

    for dep in DEPARTMENT_PRIORITY:
        if dep in candidate_departments:
            return dep

    return candidate_departments[0]

def get_doctors_for_department(dept: str) -> list:
    """Get all doctors for a given department"""
    return DOCTORS.get(dept, DOCTORS.get("general", []))


def build_doctor_entries(department: str, doctor_names: list) -> list:
    return [{"name": name, "department": department} for name in doctor_names]

def rank_doctors(primary_dept: str, all_depts: list, symptom_text: str) -> dict:
    """Rank all matching doctors from primary and secondary departments"""
    doctors_with_scores = {}
    
    # Primary department doctors get highest score
    primary_doctors = get_doctors_for_department(primary_dept)
    for doc in primary_doctors:
        doctors_with_scores[doc] = {"score": 10, "department": primary_dept}
    
    # Secondary department doctors get lower score
    for dept in all_depts:
        if dept != primary_dept:
            dept_doctors = get_doctors_for_department(dept)
            for doc in dept_doctors:
                if doc not in doctors_with_scores:
                    doctors_with_scores[doc] = {"score": 5, "department": dept}
    
    return doctors_with_scores

def generate_disease_info(department: str) -> dict:
    """Generate information about common diseases in a department"""
    disease_info = {
        "cardiology": {
            "conditions": ["Heart disease", "High blood pressure", "Arrhythmia", "Heart failure"],
            "description": "Cardiovascular diseases affect the heart and blood vessels."
        },
        "neurology": {
            "conditions": ["Migraines", "Stroke", "Epilepsy", "Parkinson's disease"],
            "description": "Neurological conditions affect the nervous system."
        },
        "orthopedics": {
            "conditions": ["Fractures", "Arthritis", "Sprains", "Disc herniation"],
            "description": "Orthopedic conditions affect bones, joints, and muscles."
        },
        "dermatology": {
            "conditions": ["Psoriasis", "Eczema", "Acne", "Skin infections"],
            "description": "Dermatological conditions affect the skin and related tissues."
        },
        "pulmonology": {
            "conditions": ["Asthma", "Bronchitis", "Pneumonia", "COPD"],
            "description": "Pulmonary conditions affect the respiratory system."
        },
        "general_medicine": {
            "conditions": ["Fever", "Cold", "Flu", "General weakness"],
            "description": "General health conditions affecting overall well-being."
        }
    }
    return disease_info.get(department, {"conditions": ["General conditions"], "description": "Healthcare conditions"})


def analyze_severity(symptom_text: str) -> str:
    """Analyze the severity of symptoms mentioned"""
    severe_keywords = ["severe", "extreme", "unbearable", "critical", "emergency", "hospital", "urgent", "life threatening"]
    moderate_keywords = ["persistent", "chronic", "recurring", "regular", "constant"]
    mild_keywords = ["mild", "slight", "minor", "little", "small"]
    
    text_lower = symptom_text.lower()
    
    for keyword in severe_keywords:
        if keyword in text_lower:
            return "severe"
    
    for keyword in moderate_keywords:
        if keyword in text_lower:
            return "moderate"
    
    for keyword in mild_keywords:
        if keyword in text_lower:
            return "mild"
    
    return "unknown"

def extract_key_symptoms(symptom_text: str) -> list:
    """Extract and highlight key symptoms from the text"""
    symptoms_found = []
    text_lower = normalize_text(symptom_text)
    
    for keyword in SYMPTOM_KEYWORDS:
        if keyword in text_lower:
            symptoms_found.append(keyword)
    
    return list(set(symptoms_found))  # Remove duplicates

def generate_followup_questions(department: str, symptoms: list) -> list:
    """Generate intelligent follow-up questions based on symptoms and department"""
    followup_map = {
        "cardiology": [
            "Do you have a family history of heart disease?",
            "Have you experienced shortness of breath?",
            "Do you have high blood pressure or take blood pressure medication?"
        ],
        "neurology": [
            "When did the headaches start?",
            "Do you experience vision problems?",
            "Have you had any recent head injuries?"
        ],
        "orthopedics": [
            "Was there an injury or accident?",
            "Is the pain constant or intermittent?",
            "Does any movement make it worse?"
        ],
        "dermatology": [
            "Is the skin condition itchy or painful?",
            "Has it been spreading?",
            "How long have you had this condition?"
        ],
        "pulmonology": [
            "Do you smoke or have you smoked?",
            "Is there any chest pain with breathing?",
            "Have you been exposed to dust or pollutants?"
        ],
        "gastroenterology": [
            "Is there any blood in your stool?",
            "What foods trigger your symptoms?",
            "How often are you experiencing these symptoms?"
        ]
    }
    
    return followup_map.get(department, [
        "When did these symptoms start?",
        "Have you experienced similar symptoms before?",
        "Are you taking any medications?"
    ])

def is_affirmative(text: str) -> bool:
    return any(word in text for word in ["yes", "yeah", "yep", "sure", "of course", "definitely", "absolutely"])

def is_negative(text: str) -> bool:
    return any(word in text for word in ["no", "not", "never", "none", "nope"])

@app.route("/chat", methods=["POST"])
def chat():
    """Enhanced chatbot endpoint with multi-turn conversation support"""
    payload = request.get_json(force=True)
    user_message = (payload.get("message") or "").strip()
    
    if not user_message:
        return jsonify({
            "reply": "Hello! I'm your healthcare assistant. Could you describe your symptoms or health concerns? You can tell me things like 'I have a severe headache and dizziness' or 'I'm experiencing chest pain when I exercise.'",
            "doctors": [],
            "departments": [],
            "suggestions": [
                "I have a headache and dizziness",
                "I'm experiencing chest pain",
                "I have persistent stomach pain",
                "I'm feeling very anxious and stressed"
            ],
            "follow_up_questions": []
        }), 400
    
    # Identify all matching departments
    scores = identify_department_scores(user_message)
    last_followup_dept = session.get("followup_department")

    if not scores and last_followup_dept:
        # Use the previous follow-up department as a context hint for short answers like "yes" or "no".
        scores[last_followup_dept] = 1

    if not scores:
        # No specific symptoms found
        return jsonify({
            "reply": "I didn't catch enough detail yet. Please describe what you feel in normal words, for example: 'my food is not digesting', 'I have a headache', or 'I'm feeling dizzy and tired'. You don't need to know exact medical terms.",
            "doctors": [],
            "departments": [],
            "suggestions": [
                "My food is not digesting",
                "I have a headache and dizziness",
                "I am feeling very tired and sick",
                "I have stomach pain after eating"
            ],
            "follow_up_questions": []
        }), 200
    
    # Get key information
    primary_department = pick_best_department(scores)
    matching_departments = get_matching_departments(scores)
    key_symptoms = extract_key_symptoms(user_message)
    severity = analyze_severity(user_message)
    
    # Get doctors
    doctors_ranked = rank_doctors(primary_department, matching_departments, user_message)
    primary_doctors = build_doctor_entries(primary_department, get_doctors_for_department(primary_department))
    all_alternative_doctors = []
    alternative_names = set([doc['name'] for doc in primary_doctors])

    # Collect alternative doctors from secondary departments
    for dept in matching_departments[1:4]:  # Get up to 3 alternative departments
        dept_doctors = get_doctors_for_department(dept)
        for doc in dept_doctors[:2]:
            if doc not in alternative_names:
                all_alternative_doctors.append({"name": doc, "department": dept})
                alternative_names.add(doc)
    
    # Generate intelligent response
    disease_info = generate_disease_info(primary_department)
    followup_questions = generate_followup_questions(primary_department, key_symptoms)
    
    # Keep follow-up context for short replies to the question
    session["followup_department"] = primary_department
    session["last_followup_questions"] = followup_questions[:2]
    session.modified = True
    
    # Build comprehensive response
    symptoms_str = ", ".join(key_symptoms) if key_symptoms else "your symptoms"
    severity_str = f"with {severity} severity " if severity != "unknown" else ""
    
    dept_name = primary_department.replace("_", " ").title()
    
    primary_doctor_names = [doc['name'] for doc in primary_doctors]
    if len(primary_doctor_names) > 1:
        doctors_str = f"{', '.join(primary_doctor_names[:-1])} or {primary_doctor_names[-1]}"
    else:
        doctors_str = primary_doctor_names[0] if primary_doctor_names else "our specialist"
    
    reply = (
        f"Based on {symptoms_str} {severity_str}I recommend a **{dept_name}** specialist. "
        f"\n\nPrimary recommendations: **{doctors_str}**"
    )
    
    if all_alternative_doctors:
        alt_str = ", ".join([doc['name'] for doc in all_alternative_doctors[:3]])
        reply += f"\n\nAlternative specialists: {alt_str}"
    
    reply += (
        f"\n\n**About {dept_name}:**\n{disease_info['description']}"
        f"\n\nCommon conditions: {', '.join(disease_info['conditions'])}"
    )
    
    return jsonify({
        "reply": reply,
        "primary_department": primary_department,
        "matching_departments": matching_departments,
        "primary_doctors": primary_doctors,
        "alternative_doctors": all_alternative_doctors[:3],
        "symptoms_found": key_symptoms,
        "severity": severity,
        "follow_up_questions": followup_questions[:2],
        "suggestions": [
            "I have chest pain and dizziness",
            "I need help with stomach pain",
            "I feel anxious and cannot sleep",
            "I have a skin rash and itching"
        ],
        "next_action": "Would you like me to ask follow-up questions or help you book an appointment?"
    }), 200


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "Healthcare Chatbot Backend"})


@app.route("/contact", methods=["POST"])
def contact_submit():
    form = request.form
    name = (form.get("name") or "").strip()
    email = (form.get("email") or "").strip()
    subject = (form.get("subject") or "").strip()
    message = (form.get("message") or "").strip()

    if not all([name, email, subject, message]):
        return "All fields are required.", 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Email is invalid.", 400

    conn = get_db_connection()
    if not conn or not conn.is_connected():
        return "Unable to connect to the database.", 500

    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO contact_messages (name, email, subject, message) VALUES (%s, %s, %s, %s)",
            (name, email, subject, message)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return "OK", 200
    except mysql.connector.Error as err:
        app.logger.error(f"Contact insert failed: {err}")
        return f"Database error: {err}", 500


@app.route("/appointment", methods=["POST"])
def appointment_submit():
    form = request.form
    name = (form.get("name") or "").strip()
    email = (form.get("email") or "").strip()
    phone = (form.get("phone") or "").strip()
    department = (form.get("department") or "").strip()
    doctor = (form.get("doctor") or "").strip()
    appointment_date = (form.get("date") or "").strip()
    appointment_time = (form.get("time") or "").strip()
    notes = (form.get("message") or "").strip()

    if not all([name, email, phone, department, doctor, appointment_date, appointment_time]):
        return jsonify({"status": "ERROR", "message": "All required fields must be filled."}), 400

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return jsonify({"status": "ERROR", "message": "Email is invalid."}), 400

    try:
        scheduled_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"status": "ERROR", "message": "Invalid appointment date."}), 400

    try:
        scheduled_time = datetime.strptime(appointment_time, "%H:%M").time()
    except ValueError:
        return jsonify({"status": "ERROR", "message": "Invalid appointment time."}), 400

    conn = get_db_connection()
    if not conn or not conn.is_connected():
        return jsonify({"status": "ERROR", "message": "Unable to connect to the database."}), 500

    try:
        cursor = conn.cursor(dictionary=True, buffered=True)
        
        # Get department
        cursor.execute(
            "SELECT id, name FROM Department WHERE slug = %s",
            (department,)
        )
        department_row = cursor.fetchone()
        if not department_row:
            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Unknown department selected."}), 400

        department_id = department_row["id"]
        department_name = department_row["name"]

        # Get doctor
        cursor.execute(
            "SELECT id FROM Doctor WHERE name = %s AND departmentId = %s",
            (doctor, department_id)
        )
        doctor_row = cursor.fetchone()
        if not doctor_row:
            cursor.close()
            conn.close()
            return jsonify({"status": "ERROR", "message": "Selected doctor is not available for this department."}), 400

        doctor_id = doctor_row["id"]
        
        # Insert appointment
        cursor.execute(
            "INSERT INTO Appointment (doctorId, departmentId, patientName, email, phone, appointment_date, appointment_time, notes, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (doctor_id, department_id, name, email, phone, scheduled_date, scheduled_time, notes, "Pending")
        )
        conn.commit()
        appointment_id = cursor.lastrowid
        cursor.close()
        conn.close()

        appointment_data = {
            "appointment_id": appointment_id,
            "name": name,
            "doctor": doctor,
            "department": department_name,
            "appointment_date": scheduled_date.strftime("%Y-%m-%d"),
            "appointment_time": scheduled_time.strftime("%H:%M"),
            "email": email,
            "phone": phone,
            "notes": notes,
        }

        try:
            send_appointment_confirmation_email(email, appointment_data)
        except Exception as err:
            app.logger.error(f"Failed to send appointment email: {err}")
            return jsonify({
                "status": "ERROR",
                "message": "Appointment saved, but email could not be sent. Please contact support."
            }), 500

        return jsonify({
            "status": "OK",
            "appointment_id": appointment_id,
            "name": name,
            "doctor": doctor,
            "department": department,
            "appointment_date": scheduled_date.strftime("%Y-%m-%d"),
            "appointment_time": scheduled_time.strftime("%H:%M"),
            "email": email,
            "phone": phone,
            "message": "Appointment confirmed!"
        }), 200
    except mysql.connector.Error as err:
        app.logger.error(f"Appointment insert failed: {err}")
        return jsonify({"status": "ERROR", "message": f"Database error: {err}"}), 500


@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json(silent=True) or request.form
    username = (data.get("username") or "").strip()
    password = (data.get("password") or "").strip()

    if not username or not password:
        return jsonify({"status": "ERROR", "message": "Username and password are required."}), 400

    conn = get_db_connection()
    if not conn or not conn.is_connected():
        return jsonify({"status": "ERROR", "message": "Unable to connect to the database."}), 500

    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, username, passwordHash FROM Admin WHERE username = %s",
            (username,)
        )
        user = cursor.fetchone()
        if not user:
            return jsonify({"status": "ERROR", "message": "Invalid admin username or password."}), 401

        if not bcrypt.checkpw(password.encode("utf-8"), user["passwordHash"].encode("utf-8")):
            return jsonify({"status": "ERROR", "message": "Invalid admin username or password."}), 401

        token = create_jwt_token(user["id"], user["username"])
        response = jsonify({"status": "OK", "message": "Admin login successful."})
        response.set_cookie("admin_token", token, httponly=True, samesite="Lax")
        return response
    except mysql.connector.Error as err:
        app.logger.error(f"Admin login query failed: {err}")
        return jsonify({"status": "ERROR", "message": "Database error."}), 500
    finally:
        if cursor is not None:
            cursor.close()
        conn.close()


@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    response = jsonify({"status": "OK", "message": "Logged out successfully."})
    response.set_cookie("admin_token", "", expires=0, httponly=True, samesite="Lax")
    return response


@app.route("/api/admin/summary", methods=["GET"])
def admin_summary():
    if not admin_required():
        return jsonify({"status": "ERROR", "message": "Unauthorized access."}), 401

    conn = get_db_connection()
    if not conn or not conn.is_connected():
        return jsonify({"status": "ERROR", "message": "Unable to connect to the database."}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) AS total_appointments FROM Appointment")
        total_appointments = cursor.fetchone().get("total_appointments", 0) or 0

        cursor.execute("SELECT COUNT(*) AS total_departments FROM Department")
        total_departments = cursor.fetchone().get("total_departments", 0) or 0

        cursor.execute("SELECT COUNT(DISTINCT name, departmentId) AS total_doctors FROM Doctor")
        total_doctors = cursor.fetchone().get("total_doctors", 0) or 0

        cursor.execute("SELECT id, name FROM Department ORDER BY name ASC")
        departments = cursor.fetchall()

        for department in departments:
            cursor.execute("SELECT COUNT(DISTINCT name, departmentId) AS doctor_count FROM Doctor WHERE departmentId = %s", (department["id"],))
            department["doctor_count"] = cursor.fetchone().get("doctor_count", 0) or 0

        cursor.close()
        conn.close()
        return jsonify({
            "status": "OK",
            "summary": {
                "total_appointments": total_appointments,
                "total_departments": total_departments,
                "total_doctors": total_doctors,
                "departments": departments,
            },
        }), 200
    except mysql.connector.Error as err:
        app.logger.error(f"Admin summary failed: {err}")
        return jsonify({"status": "ERROR", "message": "Database error."}), 500


@app.route("/api/departments", methods=["GET"])
def get_departments():
    if not admin_required():
        return jsonify({"status": "ERROR", "message": "Unauthorized access."}), 401

    conn = get_db_connection()
    if not conn or not conn.is_connected():
        return jsonify({"status": "ERROR", "message": "Unable to connect to the database."}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, slug FROM Department")
        departments = cursor.fetchall()

        for department in departments:
            cursor.execute("SELECT COUNT(*) AS doctor_count FROM Doctor WHERE departmentId = %s", (department["id"],))
            count_row = cursor.fetchone()
            department["doctor_count"] = count_row["doctor_count"] if count_row else 0

        cursor.close()
        conn.close()
        return jsonify({"status": "OK", "departments": departments}), 200
    except mysql.connector.Error as err:
        app.logger.error(f"Get departments failed: {err}")
        return jsonify({"status": "ERROR", "message": "Database error."}), 500


@app.route("/api/departments/<int:department_id>/doctors", methods=["GET"])
def get_department_doctors(department_id):
    if not admin_required():
        return jsonify({"status": "ERROR", "message": "Unauthorized access."}), 401

    conn = get_db_connection()
    if not conn or not conn.is_connected():
        return jsonify({"status": "ERROR", "message": "Unable to connect to the database."}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT id, name, specialization, photoUrl FROM Doctor WHERE departmentId = %s ORDER BY name ASC",
            (department_id,)
        )
        raw_doctors = cursor.fetchall()
        doctors = []
        seen_doctors = set()
        for doctor in raw_doctors:
            key = (doctor["name"], department_id)
            if key in seen_doctors:
                continue
            seen_doctors.add(key)
            doctors.append(doctor)

        doctor_ids = [doctor["id"] for doctor in doctors]

        if doctor_ids:
            format_strings = ",".join(["%s"] * len(doctor_ids))
            cursor.execute(
                f"SELECT doctorId, COUNT(*) AS appointment_count FROM Appointment WHERE doctorId IN ({format_strings}) GROUP BY doctorId",
                tuple(doctor_ids)
            )
            counts = {row["doctorId"]: row["appointment_count"] for row in cursor.fetchall()}
        else:
            counts = {}

        for doctor in doctors:
            doctor["appointment_count"] = counts.get(doctor["id"], 0)

        cursor.close()
        conn.close()
        return jsonify({"status": "OK", "doctors": doctors}), 200
    except mysql.connector.Error as err:
        app.logger.error(f"Get department doctors failed: {err}")
        return jsonify({"status": "ERROR", "message": "Database error."}), 500


@app.route("/api/doctors/<int:doctor_id>/appointments", methods=["GET"])
def get_doctor_appointments(doctor_id):
    if not admin_required():
        return jsonify({"status": "ERROR", "message": "Unauthorized access."}), 401

    conn = get_db_connection()
    if not conn or not conn.is_connected():
        return jsonify({"status": "ERROR", "message": "Unable to connect to the database."}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT a.id, a.patientName, a.email, a.phone, a.notes, a.appointment_date, a.appointment_time, doc.name AS doctor, dep.name AS department "
            "FROM Appointment a "
            "JOIN Doctor doc ON a.doctorId = doc.id "
            "JOIN Department dep ON a.departmentId = dep.id "
            "WHERE a.doctorId = %s "
            "ORDER BY a.appointment_date ASC, a.appointment_time ASC",
            (doctor_id,)
        )
        rows = cursor.fetchall()
        appointments = []
        for row in rows:
            appointment_date = row.get("appointment_date")
            appointment_time = row.get("appointment_time")
            appointments.append({
                "id": row.get("id"),
                "patientName": row.get("patientName"),
                "email": row.get("email"),
                "phone": row.get("phone"),
                "notes": row.get("notes"),
                "department": row.get("department"),
                "doctor": row.get("doctor"),
                "appointment_date": _format_sql_date(appointment_date),
                "appointment_time": _format_sql_time(appointment_time),
            })
        cursor.close()
        conn.close()
        return jsonify({"status": "OK", "appointments": appointments}), 200
    except mysql.connector.Error as err:
        app.logger.error(f"Get doctor appointments failed: {err}")
        return jsonify({"status": "ERROR", "message": "Database error."}), 500


@app.route("/admin/doctor-appointments", methods=["GET"])
def admin_doctor_appointments():
    if not admin_required():
        return jsonify({"status": "ERROR", "message": "Unauthorized access."}), 401

    department = (request.args.get("department") or "").strip()
    doctor = (request.args.get("doctor") or "").strip()

    if not department or not doctor:
        return jsonify({"status": "ERROR", "message": "Department and doctor are required."}), 400

    conn = get_db_connection()
    if not conn or not conn.is_connected():
        return jsonify({"status": "ERROR", "message": "Unable to connect to the database."}), 500

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT a.id, a.patientName AS name, a.email, a.phone, dep.name AS department, doc.name AS doctor, a.appointment_date, a.appointment_time, a.notes "
            "FROM Appointment a "
            "JOIN Doctor doc ON a.doctorId = doc.id "
            "JOIN Department dep ON a.departmentId = dep.id "
            "WHERE (dep.slug = %s OR dep.name = %s) AND doc.name = %s "
            "ORDER BY a.appointment_date ASC, a.appointment_time ASC",
            (department, department, doctor)
        )
        appointments = []
        for row in cursor:
            appointment_date = row.get("appointment_date")
            appointment_time = row.get("appointment_time")
            appointments.append({
                "id": row.get("id"),
                "name": row.get("name"),
                "email": row.get("email"),
                "phone": row.get("phone"),
                "department": row.get("department"),
                "doctor": row.get("doctor"),
                "appointment_date": _format_sql_date(appointment_date),
                "appointment_time": _format_sql_time(appointment_time),
                "notes": row.get("notes"),
            })

        cursor.close()
        conn.close()
        return jsonify({"status": "OK", "appointments": appointments}), 200
    except mysql.connector.Error as err:
        app.logger.error(f"Doctor appointment query failed: {err}")
        return jsonify({"status": "ERROR", "message": f"Database error: {err}"}), 500


# Serve the web app pages and assets directly for easy local testing
@app.route("/", defaults={"path": "chatbot.html"})
@app.route("/<path:path>")
def serve_web(path):
    try:
        from flask import send_from_directory
        import os

        static_root = os.path.abspath(os.path.dirname(__file__))
        # protect API routes and admin endpoints
        first_segment = path.split("/")[0]
        if first_segment == "admin":
            return send_from_directory(static_root, "admin.html")
        if first_segment in ["chat", "health"] and not path.endswith(".html"):
            return jsonify({"error": "Not a static path"}), 404

        # if file doesn't exist, fallback to chatbot page
        fullpath = os.path.join(static_root, path)
        if not os.path.exists(fullpath):
            resp = send_from_directory(static_root, "chatbot.html")
        else:
            resp = send_from_directory(static_root, path)

        # During development, instruct browsers not to cache static files
        resp.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        resp.headers['Pragma'] = 'no-cache'
        resp.headers['Expires'] = '0'
        return resp
    except Exception:
        return jsonify({"error": "unable to serve static file"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


