from flask import Flask, request, jsonify
from flask_cors import CORS
import re

app = Flask(__name__)
CORS(app)

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
    "migraine": "neurology",
    "numbness": "neurology",
    "dizziness": "neurology",
    "seizure": "neurology",
    "stroke": "neurology",
    "brain": "neurology",
    "nerve pain": "neurology",
    "tremor": "neurology",
    
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
    "acidity": "gastroenterology",
    "digestion": "gastroenterology",
    "gastric": "gastroenterology",
    "heartburn": "gastroenterology",
    "indigestion": "gastroenterology",
    "ulcer": "gastroenterology",
    "abdominal pain": "gastroenterology",
    
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


def pick_best_department(scores: dict) -> str:
    if not scores:
        return "general"

    max_score = max(scores.values())
    candidate_departments = [d for d, v in scores.items() if v == max_score]

    for dep in DEPARTMENT_PRIORITY:
        if dep in candidate_departments:
            return dep

    return candidate_departments[0]


def assign_doctor(primary_department: str, all_departments: list) -> (str, list):
    primary_doctor_list = DOCTORS.get(primary_department) or DOCTORS.get("general")
    primary_doctor = primary_doctor_list[0]

    alternate_doctors = []
    for dept in all_departments:
        if dept != primary_department and dept in DOCTORS:
            doc = DOCTORS[dept][0]
            if doc not in alternate_doctors and doc != primary_doctor:
                alternate_doctors.append(doc)

    return primary_doctor, alternate_doctors


@app.route("/chat", methods=["POST"])
def chat():
    payload = request.get_json(force=True)
    user_message = (payload.get("message") or "").strip()

    if not user_message:
        return jsonify({"reply": "Please tell me your symptoms to find a suitable doctor."}), 400

    scores = identify_department_scores(user_message)
    primary_department = pick_best_department(scores)
    matched_departments = sorted(scores.keys(), key=lambda d: (-scores.get(d, 0), DEPARTMENT_PRIORITY.index(d) if d in DEPARTMENT_PRIORITY else 999))

    primary_doctor, alternate_doctors = assign_doctor(primary_department, matched_departments)

    if alternate_doctors:
        alt_text = ", ".join(alternate_doctors[:2])
        reply = (
            f"Based on symptoms, the best match is {primary_department.capitalize()} specialist {primary_doctor}. "
            f"As your input spans multiple areas, other suitable doctors could be {alt_text}. "
            "Book the primary doctor via appointment page for fastest care."
        )
    else:
        reply = (
            f"Based on your symptoms, the best match is {primary_department.capitalize()} specialist {primary_doctor}. "
            "Please book an appointment at our hospital reception or via the appointment page."
        )

    return jsonify({
        "department": primary_department,
        "doctor": primary_doctor,
        "alternates": alternate_doctors,
        "reply": reply
    })


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


