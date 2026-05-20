from flask import Flask, request, jsonify, session
from flask_cors import CORS
from datetime import datetime, timedelta
import re
import json

app = Flask(__name__)
CORS(app)
app.secret_key = 'healthcare_chatbot_secret_key_2024'

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
    return re.sub(r"[^a-z0-9 ]", "", text.lower())


def identify_department_scores(symptoms_text: str) -> dict:
    text = normalize_text(symptoms_text)
    scores = defaultdict(int)

    for keyword, dept in SYMPTOM_KEYWORDS.items():
        if keyword in text:
            scores[dept] += 1

    if not scores:
        # Fallback: match partial symptom tokens to common departments for everyday language.
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
            "pain": "general_medicine",
            "blood": "gastroenterology",
            "stool": "gastroenterology",
            "vomit": "general_medicine",
            "vomiting": "general_medicine",
            "bloating": "gastroenterology",
            "bloated": "gastroenterology",
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
    primary_doctors = get_doctors_for_department(primary_department)
    all_alternative_doctors = []
    
    # Collect alternative doctors from secondary departments
    for dept in matching_departments[1:4]:  # Get up to 3 alternative departments
        dept_doctors = get_doctors_for_department(dept)
        all_alternative_doctors.extend(dept_doctors[:2])  # Top 2 from each dept
    
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
    
    if len(primary_doctors) > 1:
        doctors_str = f"{', '.join(primary_doctors[:-1])} or {primary_doctors[-1]}"
    else:
        doctors_str = primary_doctors[0] if primary_doctors else "our specialist"
    
    reply = (
        f"Based on {symptoms_str} {severity_str}I recommend a **{dept_name}** specialist. "
        f"\n\nPrimary recommendations: **{doctors_str}**"
    )
    
    if all_alternative_doctors:
        alt_str = ", ".join(all_alternative_doctors[:3])
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
        "next_action": "Would you like me to ask follow-up questions or help you book an appointment?"
    }), 200


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "service": "Healthcare Chatbot Backend"})


# Serve the web app pages and assets directly for easy local testing
@app.route("/", defaults={"path": "chatbot.html"})
@app.route("/<path:path>")
def serve_web(path):
    # protect API routes
    if path in ["chat", "health"]:
        return jsonify({"error": "Not a static path"}), 404

    try:
        from flask import send_from_directory
        import os

        static_root = os.path.abspath(os.path.dirname(__file__))
        # if file doesn't exist, fallback to chatbot page
        fullpath = os.path.join(static_root, path)
        if not os.path.exists(fullpath):
            return send_from_directory(static_root, "chatbot.html")
        return send_from_directory(static_root, path)
    except Exception:
        return jsonify({"error": "unable to serve static file"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


