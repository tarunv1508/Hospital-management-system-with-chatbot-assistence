// Hospital Departments and Services Data
const departmentsData = {
  cardiology: {
    id: "cardiology",
    name: "Cardiology",
    title: "Cardiology Department",
    shortDescription: "Comprehensive heart care with advanced diagnostic tools and treatment options for cardiovascular conditions.",
    longDescription: "Our Cardiology Department is dedicated to the diagnosis, treatment, and prevention of heart and blood vessel diseases. We offer state-of-the-art technology and experienced cardiologists to provide comprehensive cardiovascular care. Whether you're dealing with heart disease, hypertension, or preventive care, our team is committed to maintaining your heart health.",
    icon: "fas fa-heartbeat",
    image: "assets/img/health/cardiology-2.webp",
    services: [
      { name: "ECG Testing", description: "Advanced electrocardiography for heart rhythm assessment" },
      { name: "Heart Surgery", description: "Minimally invasive and open heart surgical procedures" },
      { name: "Angiography", description: "Diagnostic imaging of blood vessels and heart chambers" },
      { name: "Cardiac Rehabilitation", description: "Recovery and strengthening programs post-surgery" }
    ],
    features: [
      { icon: "bi-award", text: "Board-certified cardiologists" },
      { icon: "bi-clock-history", text: "24/7 cardiac emergency care" },
      { icon: "bi-shield-plus", text: "Advanced treatment options" },
      { icon: "bi-heart-pulse", text: "Patient-centered care" }
    ],
    conditions: ["Coronary Artery Disease", "Heart Failure", "Arrhythmias", "Hypertension", "Valve Disease", "Myocardial Infarction"],
    doctors: ["DR.S.Arjun Reddy", "DR.Rajesh Kumar", "DR.Vikram Singh"]
  },

  neurology: {
    id: "neurology",
    name: "Neurology",
    title: "Neurology Department",
    shortDescription: "Expert neurological care for brain and nervous system disorders with state-of-the-art imaging technology.",
    longDescription: "Our Neurology Department specializes in the diagnosis and treatment of diseases affecting the brain, spinal cord, and nerves. Our expert neurologists utilize cutting-edge diagnostic equipment and advanced treatment protocols to manage complex neurological conditions. From stroke management to chronic neurological diseases, we provide comprehensive neurological care.",
    icon: "fas fa-brain",
    image: "assets/img/health/neurology-3.webp",
    services: [
      { name: "MRI Scans", description: "High-resolution magnetic resonance imaging" },
      { name: "Stroke Care", description: "Emergency stroke management and recovery" },
      { name: "EEG Testing", description: "Electroencephalography for brain activity monitoring" },
      { name: "Neurological Examination", description: "Comprehensive neurological assessment" }
    ],
    features: [
      { icon: "bi-award", text: "Specialist neurologists" },
      { icon: "bi-clock-history", text: "Emergency neurology 24/7" },
      { icon: "bi-shield-plus", text: "Advanced imaging facilities" },
      { icon: "bi-heart-pulse", text: "Comprehensive care programs" }
    ],
    conditions: ["Stroke", "Epilepsy", "Parkinson's Disease", "Multiple Sclerosis", "Migraine", "Dementia"],
    doctors: ["DR.S.SaiPriya", "DR.T.Anu", "DR.Neha Sharma"]
  },

  orthopedics: {
    id: "orthopedics",
    name: "Orthopedics",
    title: "Orthopedics Department",
    shortDescription: "Specialized bone and joint treatment including sports medicine and reconstructive surgery procedures.",
    longDescription: "Our Orthopedics Department provides comprehensive care for musculoskeletal conditions. Our experienced orthopedic surgeons specialize in joint replacement, sports medicine, and reconstructive surgery. We combine surgical expertise with rehabilitation programs to restore function and improve quality of life.",
    icon: "fas fa-bone",
    image: "assets/img/health/orthopedics-1.webp",
    services: [
      { name: "Joint Replacement", description: "Hip, knee, and shoulder replacement surgery" },
      { name: "Sports Medicine", description: "Treatment of sports-related injuries" },
      { name: "Arthroscopy", description: "Minimally invasive joint surgery" },
      { name: "Fracture Management", description: "Treatment and rehabilitation of fractures" }
    ],
    features: [
      { icon: "bi-award", text: "Expert orthopedic surgeons" },
      { icon: "bi-clock-history", text: "Same-day appointments available" },
      { icon: "bi-shield-plus", text: "Advanced surgical techniques" },
      { icon: "bi-heart-pulse", text: "Physical therapy programs" }
    ],
    conditions: ["Osteoarthritis", "Rheumatoid Arthritis", "Rotator Cuff Injury", "ACL Tear", "Bone Fractures", "Spinal Disorders"],
    doctors: ["DR.M.Sameer", "DR.Ravi Patel", "DR.Suresh Gupta"]
  },

  pediatrics: {
    id: "pediatrics",
    name: "Pediatrics",
    title: "Pediatrics Department",
    shortDescription: "Dedicated healthcare for children from infancy through adolescence with specialized treatment protocols.",
    longDescription: "Our Pediatrics Department provides specialized medical care for infants, children, and adolescents. Our pediatricians are trained to handle the unique healthcare needs of growing children. We offer preventive care, immunizations, and treatment for childhood illnesses in a child-friendly environment.",
    icon: "fas fa-child",
    image: "assets/img/health/pediatrics-4.webp",
    services: [
      { name: "Well-Child Visits", description: "Routine check-ups and developmental screening" },
      { name: "Immunizations", description: "Complete vaccination programs for children" },
      { name: "Pediatric Surgery", description: "Surgical care for children" },
      { name: "Neonatal Care", description: "Specialized care for newborns" }
    ],
    features: [
      { icon: "bi-award", text: "Pediatric specialists" },
      { icon: "bi-clock-history", text: "Child-friendly facilities" },
      { icon: "bi-shield-plus", text: "Preventive care focus" },
      { icon: "bi-heart-pulse", text: "Family-centered approach" }
    ],
    conditions: ["Asthma", "Ear Infections", "Allergies", "Growth Disorders", "Behavioral Issues", "Developmental Delays"],
    doctors: ["DR.N.MadhuLatha", "DR.Priya Verma", "DR.Arun Nair"]
  },

  dermatology: {
    id: "dermatology",
    name: "Dermatology",
    title: "Dermatology Department",
    shortDescription: "Comprehensive skin care services including diagnosis and treatment of skin, hair, and nail conditions.",
    longDescription: "Our Dermatology Department offers expert care for all skin, hair, and nail conditions. From acne and eczema to skin cancer screening and cosmetic treatments, our dermatologists provide comprehensive dermatological services using the latest technology and treatment methods.",
    icon: "fas fa-spa",
    image: "assets/img/health/dermatology-1.webp",
    services: [
      { name: "Skin Cancer Screening", description: "Early detection and treatment of skin cancers" },
      { name: "Acne Treatment", description: "Comprehensive acne management programs" },
      { name: "Cosmetic Procedures", description: "Laser and non-invasive cosmetic treatments" },
      { name: "Hair Loss Treatment", description: "Solutions for hair loss and baldness" }
    ],
    features: [
      { icon: "bi-award", text: "Certified dermatologists" },
      { icon: "bi-clock-history", text: "Advanced laser technology" },
      { icon: "bi-shield-plus", text: "Cosmetic expertise" },
      { icon: "bi-heart-pulse", text: "Personalized treatment plans" }
    ],
    conditions: ["Eczema", "Psoriasis", "Acne", "Rosacea", "Hair Loss", "Warts"],
    doctors: ["DR.N.lohith", "DR.Anjali Singh", "DR.Meera Joshi"]
  },

  oncology: {
    id: "oncology",
    name: "Oncology",
    title: "Oncology Department",
    shortDescription: "Specialized cancer treatment and care with multidisciplinary approach and advanced therapeutic options.",
    longDescription: "Our Oncology Department provides comprehensive cancer care with a multidisciplinary team approach. We offer chemotherapy, radiation therapy, targeted therapy, and immunotherapy. Our goal is to provide personalized cancer treatment plans that maximize effectiveness while minimizing side effects.",
    icon: "fas fa-pills",
    image: "assets/img/health/oncology-2.webp",
    services: [
      { name: "Chemotherapy", description: "Drug therapy for cancer treatment" },
      { name: "Radiation Therapy", description: "Targeted radiation treatment" },
      { name: "Tumor Surgery", description: "Surgical removal of tumors" },
      { name: "Palliative Care", description: "Comfort and symptom management" }
    ],
    features: [
      { icon: "bi-award", text: "Oncology specialists" },
      { icon: "bi-clock-history", text: "Multidisciplinary team" },
      { icon: "bi-shield-plus", text: "Advanced treatment options" },
      { icon: "bi-heart-pulse", text: "Supportive care programs" }
    ],
    conditions: ["Breast Cancer", "Lung Cancer", "Colon Cancer", "Lymphoma", "Leukemia", "Prostate Cancer"],
    doctors: ["DR.T.Anu", "DR.Ashok Kumar", "DR.Sneha Desai"]
  },

  ent: {
    id: "ent",
    name: "ENT (Otolaryngology)",
    title: "ENT Department",
    shortDescription: "Specialized care for ear, nose, and throat conditions with surgical and non-surgical treatment options.",
    longDescription: "Our ENT Department specializes in the diagnosis and treatment of disorders affecting the ear, nose, throat, head, and neck. Our otolaryngologists provide both medical and surgical treatments for a wide range of ENT conditions, ensuring optimal hearing, breathing, and quality of life.",
    icon: "fas fa-ear",
    image: "assets/img/health/neurology-4.webp",
    services: [
      { name: "Hearing Assessment", description: "Comprehensive audiological testing" },
      { name: "Sinus Surgery", description: "Surgical treatment of sinus conditions" },
      { name: "Throat Surgery", description: "Surgical procedures for throat conditions" },
      { name: "Hearing Aids", description: "Fitting and management of hearing aids" }
    ],
    features: [
      { icon: "bi-award", text: "ENT specialists" },
      { icon: "bi-clock-history", text: "Advanced diagnostic equipment" },
      { icon: "bi-shield-plus", text: "Surgical expertise" },
      { icon: "bi-heart-pulse", text: "Hearing rehabilitation" }
    ],
    conditions: ["Hearing Loss", "Sinusitis", "Throat Infection", "Tinnitus", "Dizziness", "Sleep Apnea"],
    doctors: ["DR.Vikram Sharma", "DR.Anand Gupta", "DR.Shruti Patel"]
  },

  gastroenterology: {
    id: "gastroenterology",
    name: "Gastroenterology",
    title: "Gastroenterology Department",
    shortDescription: "Expert diagnosis and treatment of digestive system disorders using advanced endoscopic procedures.",
    longDescription: "Our Gastroenterology Department specializes in the diagnosis and treatment of diseases affecting the digestive system. We offer advanced endoscopic procedures, surgical interventions, and medical management for gastrointestinal conditions.",
    icon: "fas fa-utensils",
    image: "assets/img/health/laboratory-3.webp",
    services: [
      { name: "Endoscopy", description: "Diagnostic and therapeutic endoscopic procedures" },
      { name: "Colonoscopy", description: "Colorectal screening and treatment" },
      { name: "Ulcer Treatment", description: "Management of gastric and duodenal ulcers" },
      { name: "IBD Management", description: "Treatment of inflammatory bowel disease" }
    ],
    features: [
      { icon: "bi-award", text: "Gastroenterologists" },
      { icon: "bi-clock-history", text: "Advanced endoscopy units" },
      { icon: "bi-shield-plus", text: "Nutritional counseling" },
      { icon: "bi-heart-pulse", text: "Preventive care focus" }
    ],
    conditions: ["Gastroesophageal Reflux", "Irritable Bowel Syndrome", "Crohn's Disease", "Ulcerative Colitis", "Gallstones", "Liver Disease"],
    doctors: ["DR.Rohit Verma", "DR.Priya Singh", "DR.Aditya Sengupta"]
  },

  nephrology: {
    id: "nephrology",
    name: "Nephrology",
    title: "Nephrology Department",
    shortDescription: "Expert kidney care and dialysis services for acute and chronic renal conditions.",
    longDescription: "Our Nephrology Department offers comprehensive care for kidney diseases, electrolyte imbalances, and hypertension management. We provide advanced dialysis support and personalized treatment plans for patients at every stage of renal health.",
    icon: "fas fa-tint",
    image: "assets/img/health/consultation-4.webp",
    services: [
      { name: "Dialysis Support", description: "Chronic and acute dialysis care with patient-centered management" },
      { name: "Kidney Disease Management", description: "Diagnosis and treatment of kidney disorders and hypertension" },
      { name: "Renal Biopsy", description: "Accurate diagnosis through advanced kidney tissue sampling" },
      { name: "Electrolyte Care", description: "Specialized management of fluid and electrolyte imbalances" }
    ],
    features: [
      { icon: "bi-award", text: "Kidney specialists" },
      { icon: "bi-clock-history", text: "Dialysis units available" },
      { icon: "bi-shield-plus", text: "Hypertension care" },
      { icon: "bi-heart-pulse", text: "Chronic disease monitoring" }
    ],
    conditions: ["Chronic Kidney Disease", "Kidney Stones", "Hypertension", "Dialysis", "Electrolyte Disorders"],
    doctors: ["DR.Sanjay Kumar", "DR.Meera Nair", "DR.Rajiv Desai"]
  },

  urology: {
    id: "urology",
    name: "Urology",
    title: "Urology Department",
    shortDescription: "Complete urinary tract and male reproductive health services with the latest surgical techniques.",
    longDescription: "Our Urology Department provides diagnosis and treatment for urinary tract disorders, prostate conditions, and male reproductive health. We combine minimally invasive surgery with medical therapies to protect kidney and bladder function.",
    icon: "fas fa-viruses",
    image: "assets/img/health/consultation-4.webp",
    services: [
      { name: "Stone Management", description: "Shock wave lithotripsy and surgical removal of kidney stones" },
      { name: "Prostate Care", description: "Diagnosis and treatment of prostate enlargement and prostate cancer" },
      { name: "Bladder Health", description: "Treatment of urinary incontinence and infections" },
      { name: "Male Fertility", description: "Comprehensive evaluation and care for male reproductive health" }
    ],
    features: [
      { icon: "bi-award", text: "Urology specialists" },
      { icon: "bi-clock-history", text: "Minimally invasive surgery" },
      { icon: "bi-shield-plus", text: "Advanced diagnostics" },
      { icon: "bi-heart-pulse", text: "Patient-centered care" }
    ],
    conditions: ["Kidney Stones", "Prostate Disorders", "Urinary Incontinence", "Bladder Infections", "Male Infertility"],
    doctors: ["DR.Harsh Patel", "DR.Vikas Sharma", "DR.Amit Singh"]
  },

  pulmonology: {
    id: "pulmonology",
    name: "Pulmonology",
    title: "Pulmonology Department",
    shortDescription: "Specialized care for respiratory and lung conditions, including asthma and COPD management.",
    longDescription: "Our Pulmonology Department provides advanced respiratory care for conditions such as asthma, COPD, pneumonia, and lung infections. We offer pulmonary function testing, inhalation therapy, and critical respiratory support.",
    icon: "fas fa-lungs",
    image: "assets/img/health/consultation-4.webp",
    services: [
      { name: "Breathing Therapy", description: "Supportive care for asthma and chronic lung disease" },
      { name: "Pulmonary Testing", description: "Lung function tests for accurate respiratory diagnosis" },
      { name: "Sleep Apnea Care", description: "Evaluation and treatment for sleep-related breathing disorders" },
      { name: "Pneumonia Management", description: "Comprehensive treatment for infections affecting the lungs" }
    ],
    features: [
      { icon: "bi-award", text: "Respiratory specialists" },
      { icon: "bi-clock-history", text: "Pulmonary rehabilitation" },
      { icon: "bi-shield-plus", text: "Diagnostic imaging" },
      { icon: "bi-heart-pulse", text: "Chronic care programs" }
    ],
    conditions: ["Asthma", "COPD", "Pneumonia", "Sleep Apnea", "Lung Infections"],
    doctors: ["DR.Deepak Verma", "DR.Sneha Kumar", "DR.Arjun Sharma"]
  },

  endocrinology: {
    id: "endocrinology",
    name: "Endocrinology",
    title: "Endocrinology Department",
    shortDescription: "Hormonal health care for diabetes, thyroid disorders, and metabolic conditions.",
    longDescription: "Our Endocrinology Department offers expert care for hormonal and metabolic disorders. We diagnose and manage diabetes, thyroid disease, adrenal disorders, and osteoporosis with personalized treatment plans.",
    icon: "fas fa-vial",
    image: "assets/img/health/consultation-4.webp",
    services: [
      { name: "Diabetes Management", description: "Comprehensive care for type 1 and type 2 diabetes" },
      { name: "Thyroid Care", description: "Diagnosis and treatment of thyroid imbalances" },
      { name: "Hormone Therapy", description: "Management of hormonal disorders and metabolic health" },
      { name: "Bone Health", description: "Osteoporosis screening and treatment" }
    ],
    features: [
      { icon: "bi-award", text: "Endocrine specialists" },
      { icon: "bi-clock-history", text: "Chronic disease management" },
      { icon: "bi-shield-plus", text: "Hormone testing" },
      { icon: "bi-heart-pulse", text: "Personalized nutrition care" }
    ],
    conditions: ["Diabetes", "Thyroid Disorders", "Hormonal Imbalance", "Osteoporosis", "Adrenal Disorders"],
    doctors: ["DR.Divya Singh", "DR.Ashok Nair", "DR.Priya Gupta"]
  },

  gynecology: {
    id: "gynecology",
    name: "Gynecology",
    title: "Gynecology Department",
    shortDescription: "Women’s health services including prenatal care, menstrual health, and reproductive wellness.",
    longDescription: "Our Gynecology Department provides compassionate care for women’s health across all life stages. We offer prenatal services, gynecological screenings, menopause support, and reproductive health counseling.",
    icon: "fas fa-female",
    image: "assets/img/health/maternal-2.webp",
    services: [
      { name: "Prenatal Care", description: "Comprehensive pregnancy monitoring and support" },
      { name: "Menstrual Health", description: "Diagnosis and treatment for menstrual disorders" },
      { name: "Fertility Counseling", description: "Reproductive health guidance and fertility evaluation" },
      { name: "Gynecologic Surgery", description: "Minimally invasive and general gynecologic procedures" }
    ],
    features: [
      { icon: "bi-award", text: "Women’s health experts" },
      { icon: "bi-clock-history", text: "Prenatal and postnatal care" },
      { icon: "bi-shield-plus", text: "Reproductive health services" },
      { icon: "bi-heart-pulse", text: "Personalized family planning" }
    ],
    conditions: ["Pregnancy Care", "Menstrual Disorders", "Fertility Issues", "Menopause Support", "Gynecologic Surgery"],
    doctors: ["DR.Ragini Sharma", "DR.Neha Verma", "DR.Anjali Patel"]
  },

  psychiatry: {
    id: "psychiatry",
    name: "Psychiatry",
    title: "Psychiatry Department",
    shortDescription: "Mental health support for anxiety, depression, stress, and behavioral wellness.",
    longDescription: "Our Psychiatry Department provides mental health assessment and treatment through counseling, medication management, and behavioral therapies. We support emotional wellness and recovery for patients facing anxiety, depression, and stress-related conditions.",
    icon: "fas fa-user-md",
    image: "assets/img/health/staff-8.webp",
    services: [
      { name: "Counseling Services", description: "Individual and group therapy for mental health support" },
      { name: "Medication Management", description: "Psychiatric medication review and monitoring" },
      { name: "Stress Management", description: "Therapies for anxiety and emotional wellness" },
      { name: "Behavioral Health", description: "Comprehensive care for mood and behavioral conditions" }
    ],
    features: [
      { icon: "bi-award", text: "Mental health specialists" },
      { icon: "bi-clock-history", text: "Therapy and counseling" },
      { icon: "bi-shield-plus", text: "Medication support" },
      { icon: "bi-heart-pulse", text: "Holistic wellness plans" }
    ],
    conditions: ["Anxiety", "Depression", "Stress Disorders", "Bipolar Disorder", "Sleep Disorders"],
    doctors: ["DR.Ramesh Singh", "DR.Anjali Kumar", "DR.Vikram Desai"]
  },

  general_medicine: {
    id: "general_medicine",
    name: "General Medicine",
    title: "General Medicine Department",
    shortDescription: "Primary care for acute illness, preventive health, and routine wellness visits.",
    longDescription: "Our General Medicine Department provides primary care services for common health concerns, preventive check-ups, and long-term wellness management. We focus on early diagnosis and personalized treatment to keep patients healthy.",
    icon: "fas fa-notes-medical",
    image: "assets/img/health/consultation-4.webp",
    services: [
      { name: "Health Checkups", description: "Routine wellness visits and preventive screenings" },
      { name: "Acute Illness Care", description: "Diagnosis and treatment for common infections and conditions" },
      { name: "Chronic Disease Follow-up", description: "Management of hypertension, diabetes, and other chronic conditions" },
      { name: "Vaccination Services", description: "Immunizations for adults and seniors" }
    ],
    features: [
      { icon: "bi-award", text: "Primary care physicians" },
      { icon: "bi-clock-history", text: "Same-day consultations" },
      { icon: "bi-shield-plus", text: "Preventive screening" },
      { icon: "bi-heart-pulse", text: "Family health focus" }
    ],
    conditions: ["Fever", "Infections", "Chronic Disease Management", "General Weakness", "Preventative Care"],
    doctors: ["DR.S.Arjun Reddy", "DR.Ramesh Kumar", "DR.Pooja Menon"]
  },

  general: {
    id: "general",
    name: "General Consultation",
    title: "General Consultation",
    shortDescription: "Accessible general health assessment and referrals for all non-emergency concerns.",
    longDescription: "Our General Consultation service provides flexible access to medical evaluation for a wide range of symptoms. We help patients find the right care pathway and coordinate referrals to specialist departments when needed.",
    icon: "fas fa-stethoscope",
    image: "assets/img/health/consultation-4.webp",
    services: [
      { name: "Initial Medical Evaluation", description: "Comprehensive health assessment and medical advice" },
      { name: "Specialist Referral", description: "Coordinated referrals to specialists based on your symptoms" },
      { name: "Wellness Counseling", description: "Guidance on healthy lifestyle choices and prevention" },
      { name: "Follow-up Care", description: "Ongoing monitoring and support for non-emergency concerns" }
    ],
    features: [
      { icon: "bi-award", text: "General physicians" },
      { icon: "bi-clock-history", text: "Easy appointment access" },
      { icon: "bi-shield-plus", text: "Care coordination" },
      { icon: "bi-heart-pulse", text: "Referral support" }
    ],
    conditions: ["Routine Health Concerns", "New Symptoms", "Referrals", "Preventive Care", "General Advice"],
    doctors: ["DR.S.Arjun Reddy", "DR.Ramesh Kumar", "DR.Pooja Menon", "DR.Vikram Singh", "DR.S.SaiPriya", "DR.N.MadhuLatha"]
  }
};

// Services Data
const servicesData = {
  cardiology: {
    id: "cardiology",
    name: "Cardiology Services",
    title: "Comprehensive Cardiac Care",
    shortDescription: "Advanced cardiac services with state-of-the-art diagnostic and treatment facilities.",
    longDescription: "Our cardiology service offers comprehensive evaluation and management of all cardiovascular conditions. We combine diagnostic expertise with therapeutic innovation to provide optimal cardiac care.",
    icon: "fas fa-heartbeat",
    image: "assets/img/health/cardiology-2.webp",
    details: [
      { icon: "bi-activity", title: "Cardiac Assessment", description: "Complete cardiovascular evaluation and risk assessment" },
      { icon: "bi-diagram-2", title: "Advanced Imaging", description: "Echocardiography, stress testing, and CT angiography" },
      { icon: "bi-prescription2", title: "Treatment Planning", description: "Personalized treatment plans for cardiac conditions" }
    ]
  },

  emergency: {
    id: "emergency",
    name: "Emergency Care Services",
    title: "24/7 Emergency Medical Services",
    shortDescription: "Round-the-clock emergency medical services with rapid response teams and critical care capabilities.",
    longDescription: "Our Emergency Department operates 24/7 with a fully equipped trauma center and critical care unit. We handle all types of emergencies with rapid assessment, diagnosis, and treatment.",
    icon: "fas fa-ambulance",
    image: "assets/img/health/emergency-2.webp",
    details: [
      { icon: "bi-activity", title: "Trauma Center", description: "Comprehensive trauma care with surgical capability" },
      { icon: "bi-diagram-2", title: "Critical Care", description: "Advanced ICU and critical care services" },
      { icon: "bi-prescription2", title: "Emergency Surgery", description: "On-demand emergency surgical services" }
    ]
  },

  laboratory: {
    id: "laboratory",
    name: "Laboratory Services",
    title: "Advanced Diagnostic Laboratory",
    shortDescription: "Comprehensive laboratory testing with rapid results and high accuracy.",
    longDescription: "Our state-of-the-art laboratory provides comprehensive diagnostic testing services. We offer blood tests, pathology services, and specialized testing with rapid turnaround times.",
    icon: "fas fa-microscope",
    image: "assets/img/health/laboratory-3.webp",
    details: [
      { icon: "bi-activity", title: "Blood Testing", description: "Complete blood work and hematology services" },
      { icon: "bi-diagram-2", title: "Pathology", description: "Tissue analysis and histopathology services" },
      { icon: "bi-prescription2", title: "Specialized Testing", description: "Advanced diagnostic and molecular testing" }
    ]
  },

  radiology: {
    id: "radiology",
    name: "Radiology Services",
    title: "Medical Imaging Services",
    shortDescription: "Advanced medical imaging using X-ray, CT, MRI, and ultrasound technology.",
    longDescription: "Our radiology department is equipped with the latest imaging technology. We provide comprehensive diagnostic and interventional radiology services for all medical conditions.",
    icon: "fas fa-radiation",
    image: "assets/img/health/facilities-6.webp",
    details: [
      { icon: "bi-activity", title: "CT Scanning", description: "High-resolution computed tomography imaging" },
      { icon: "bi-diagram-2", title: "MRI Imaging", description: "Advanced magnetic resonance imaging" },
      { icon: "bi-prescription2", title: "Ultrasound", description: "Real-time ultrasound imaging services" }
    ]
  },

  physiotherapy: {
    id: "physiotherapy",
    name: "Physiotherapy Services",
    title: "Rehabilitation & Physical Therapy",
    shortDescription: "Comprehensive rehabilitation services for post-surgery recovery and chronic pain management.",
    longDescription: "Our physiotherapy department offers personalized rehabilitation programs for various conditions. We combine manual therapy with modern therapeutic techniques to restore function and mobility.",
    icon: "fas fa-person-walking",
    image: "assets/img/health/staff-10.webp",
    details: [
      { icon: "bi-activity", title: "Post-Surgery Rehab", description: "Specialized rehabilitation after surgical procedures" },
      { icon: "bi-diagram-2", title: "Pain Management", description: "Physical therapy for chronic pain relief" },
      { icon: "bi-prescription2", title: "Sports Injury", description: "Treatment and rehabilitation of sports injuries" }
    ]
  },

  dentistry: {
    id: "dentistry",
    name: "Dental Services",
    title: "Comprehensive Dental Care",
    shortDescription: "Complete dental services including preventive care, cosmetic, and surgical procedures.",
    longDescription: "Our dental services provide comprehensive oral healthcare. We offer preventive care, cosmetic dentistry, and advanced surgical procedures in a comfortable environment.",
    icon: "fas fa-tooth",
    image: "assets/img/health/dermatology-4.webp",
    details: [
      { icon: "bi-activity", title: "Preventive Care", description: "Regular cleaning and dental health maintenance" },
      { icon: "bi-diagram-2", title: "Cosmetic Dentistry", description: "Teeth whitening and cosmetic restoration" },
      { icon: "bi-prescription2", title: "Oral Surgery", description: "Tooth extraction and implant placement" }
    ]
  }
};

// Doctor Details
const doctorDetails = {
  "DR.S.Arjun Reddy": {
    name: "DR.S.Arjun Reddy",
    specialty: "Cardiologist, General Medicine",
    experience: "18+ Years",
    qualification: "MD (Cardiology), FACC",
    description: "Dr. Arjun Reddy is a renowned cardiologist with extensive experience in cardiac care. Specialized in interventional cardiology and cardiac rehabilitation.",
    image: "assets/img/health/staff-1.webp",
    phone: "+1 (555) 123-4567",
    email: "arjun.reddy@hospital.com",
    availability: "Mon-Fri 9:00 AM - 5:00 PM"
  },
  "DR.Rajesh Kumar": {
    name: "DR.Rajesh Kumar",
    specialty: "Cardiologist",
    experience: "15+ Years",
    qualification: "MD (Cardiology)",
    description: "Expert in cardiac imaging and non-invasive cardiology. Dr. Kumar brings comprehensive experience in echocardiography and cardiac diagnostics.",
    image: "assets/img/health/staff-2.webp",
    phone: "+1 (555) 234-5678",
    email: "rajesh.kumar@hospital.com",
    availability: "Mon, Wed, Fri 10:00 AM - 6:00 PM"
  },
  "DR.Vikram Singh": {
    name: "DR.Vikram Singh",
    specialty: "Cardiologist",
    experience: "12+ Years",
    qualification: "MD (Cardiology), DM",
    description: "Specialized in electrophysiology and arrhythmia management. Dr. Singh is skilled in pacemaker implantation and ablation procedures.",
    image: "assets/img/health/staff-3.webp",
    phone: "+1 (555) 345-6789",
    email: "vikram.singh@hospital.com",
    availability: "Tue, Thu, Sat 11:00 AM - 7:00 PM"
  },
  "DR.S.SaiPriya": {
    name: "DR.S.SaiPriya",
    specialty: "Neurologist",
    experience: "14+ Years",
    qualification: "MD (Neurology), DNB",
    description: "Expert in stroke management and neurological emergencies. Dr. Priya specializes in minimally invasive neurology procedures.",
    image: "assets/img/health/staff-1.webp",
    phone: "+1 (555) 456-7890",
    email: "saipriya@hospital.com",
    availability: "Mon-Fri 9:00 AM - 5:00 PM"
  },
  "DR.T.Anu": {
    name: "DR.T.Anu",
    specialty: "Neurologist, Oncologist",
    experience: "16+ Years",
    qualification: "MD (Neurology), DM (Oncology)",
    description: "Specialist in neuro-oncology and complex neurological conditions. Dr. Anu has extensive experience in tumor management.",
    image: "assets/img/health/staff-2.webp",
    phone: "+1 (555) 567-8901",
    email: "anu.t@hospital.com",
    availability: "Tue, Thu, Sat 10:00 AM - 6:00 PM"
  },
  "DR.Neha Sharma": {
    name: "DR.Neha Sharma",
    specialty: "Neurologist",
    experience: "11+ Years",
    qualification: "MD (Neurology)",
    description: "Specialized in pediatric neurology and developmental disorders. Dr. Sharma is passionate about patient care and rehabilitation.",
    image: "assets/img/health/staff-3.webp",
    phone: "+1 (555) 678-9012",
    email: "neha.sharma@hospital.com",
    availability: "Mon, Wed, Fri 2:00 PM - 8:00 PM"
  },
  "DR.M.Sameer": {
    name: "DR.M.Sameer",
    specialty: "Orthopedic Surgeon",
    experience: "17+ Years",
    qualification: "MS (Orthopedics), MCh",
    description: "Expert in joint replacement surgery and sports medicine. Dr. Sameer has performed over 5000 successful orthopedic procedures.",
    image: "assets/img/health/staff-1.webp",
    phone: "+1 (555) 789-0123",
    email: "sameer.m@hospital.com",
    availability: "Mon, Tue, Thu, Fri 9:00 AM - 5:00 PM"
  },
  "DR.Ravi Patel": {
    name: "DR.Ravi Patel",
    specialty: "Orthopedic Surgeon",
    experience: "13+ Years",
    qualification: "MS (Orthopedics)",
    description: "Specialized in arthroscopic surgery and sports injuries. Dr. Patel uses advanced minimally invasive techniques.",
    image: "assets/img/health/staff-2.webp",
    phone: "+1 (555) 890-1234",
    email: "ravi.patel@hospital.com",
    availability: "Wed, Fri, Sat 10:00 AM - 6:00 PM"
  },
  "DR.Suresh Gupta": {
    name: "DR.Suresh Gupta",
    specialty: "Orthopedic Surgeon",
    experience: "15+ Years",
    qualification: "MS (Orthopedics), DNB",
    description: "Expert in spine surgery and complex orthopedic cases. Dr. Gupta is known for his patient-centric approach.",
    image: "assets/img/health/staff-3.webp",
    phone: "+1 (555) 901-2345",
    email: "suresh.gupta@hospital.com",
    availability: "Tue, Thu, Sat 11:00 AM - 7:00 PM"
  },
  "DR.N.MadhuLatha": {
    name: "DR.N.MadhuLatha",
    specialty: "Pediatrician",
    experience: "16+ Years",
    qualification: "MD (Pediatrics), DM",
    description: "Renowned pediatrician with expertise in child development and growth. Dr. Madhulatha is skilled in handling complex pediatric cases.",
    image: "assets/img/health/staff-1.webp",
    phone: "+1 (555) 012-3456",
    email: "madhulatha@hospital.com",
    availability: "Mon-Fri 9:00 AM - 5:00 PM"
  },
  "DR.Priya Verma": {
    name: "DR.Priya Verma",
    specialty: "Pediatrician",
    experience: "12+ Years",
    qualification: "MD (Pediatrics)",
    description: "Specialized in neonatal care and pediatric nutrition. Dr. Verma is compassionate and child-friendly in her approach.",
    image: "assets/img/health/staff-2.webp",
    phone: "+1 (555) 123-0456",
    email: "priya.verma@hospital.com",
    availability: "Tue, Thu, Sat 10:00 AM - 6:00 PM"
  },
  "DR.Arun Nair": {
    name: "DR.Arun Nair",
    specialty: "Pediatrician",
    experience: "10+ Years",
    qualification: "MD (Pediatrics), DNB",
    description: "Expert in immunization and preventive pediatrics. Dr. Nair is dedicated to promoting child health and wellness.",
    image: "assets/img/health/staff-3.webp",
    phone: "+1 (555) 234-0567",
    email: "arun.nair@hospital.com",
    availability: "Mon, Wed, Fri 2:00 PM - 8:00 PM"
  },
  "DR.N.lohith": {
    name: "DR.N.lohith",
    specialty: "Dermatologist",
    experience: "13+ Years",
    qualification: "MD (Dermatology), DDV",
    description: "Expert in cosmetic dermatology and skin disease management. Dr. Lohith uses modern laser and non-invasive treatments.",
    image: "assets/img/health/staff-1.webp",
    phone: "+1 (555) 345-0678",
    email: "lohith.n@hospital.com",
    availability: "Mon, Wed, Fri 10:00 AM - 6:00 PM"
  },
  "DR.Anjali Singh": {
    name: "DR.Anjali Singh",
    specialty: "Dermatologist",
    experience: "11+ Years",
    qualification: "MD (Dermatology)",
    description: "Specialized in acne management and skin rejuvenation. Dr. Singh offers personalized dermatological solutions.",
    image: "assets/img/health/staff-2.webp",
    phone: "+1 (555) 456-0789",
    email: "anjali.singh@hospital.com",
    availability: "Tue, Thu, Sat 11:00 AM - 7:00 PM"
  },
  "DR.Meera Joshi": {
    name: "DR.Meera Joshi",
    specialty: "Dermatologist",
    experience: "9+ Years",
    qualification: "MD (Dermatology), IADVL",
    description: "Expert in hair care and scalp disorders. Dr. Joshi provides comprehensive dermatological care for all ages.",
    image: "assets/img/health/staff-3.webp",
    phone: "+1 (555) 567-0890",
    email: "meera.joshi@hospital.com",
    availability: "Mon, Fri, Sat 2:00 PM - 8:00 PM"
  },
  "DR.T.Anu": {
    name: "DR.T.Anu",
    specialty: "Oncologist",
    experience: "16+ Years",
    qualification: "MD (Oncology), DM",
    description: "Specialist in medical oncology with focus on personalized cancer treatment. Dr. Anu combines expertise with compassionate care.",
    image: "assets/img/health/staff-1.webp",
    phone: "+1 (555) 678-0901",
    email: "anu.t@hospital.com",
    availability: "Tue, Thu, Sat 10:00 AM - 6:00 PM"
  },
  "DR.Ashok Kumar": {
    name: "DR.Ashok Kumar",
    specialty: "Oncologist",
    experience: "14+ Years",
    qualification: "MD (Oncology), DM",
    description: "Expert in surgical oncology and cancer rehabilitation. Dr. Kumar is known for his holistic approach to cancer care.",
    image: "assets/img/health/staff-2.webp",
    phone: "+1 (555) 789-0912",
    email: "ashok.kumar@hospital.com",
    availability: "Mon, Wed, Fri 9:00 AM - 5:00 PM"
  },
  "DR.Sneha Desai": {
    name: "DR.Sneha Desai",
    specialty: "Oncologist",
    experience: "12+ Years",
    qualification: "MD (Oncology), DM",
    description: "Specialized in radiation oncology and treatment planning. Dr. Desai is committed to improving cancer patient outcomes.",
    image: "assets/img/health/staff-3.webp",
    phone: "+1 (555) 890-0123",
    email: "sneha.desai@hospital.com",
    availability: "Tue, Thu, Sat 11:00 AM - 7:00 PM"
  },
  "DR.Vikram Sharma": {
    name: "DR.Vikram Sharma",
    specialty: "ENT Specialist",
    experience: "15+ Years",
    qualification: "MS (ENT), MCh",
    description: "Expert in otologic surgery and hearing restoration. Dr. Sharma specializes in complex ear, nose, and throat procedures.",
    image: "assets/img/health/staff-1.webp",
    phone: "+1 (555) 901-0234",
    email: "vikram.sharma@hospital.com",
    availability: "Mon, Tue, Thu, Fri 9:00 AM - 5:00 PM"
  },
  "DR.Anand Gupta": {
    name: "DR.Anand Gupta",
    specialty: "ENT Specialist",
    experience: "12+ Years",
    qualification: "MS (ENT)",
    description: "Specialized in sinus surgery and voice disorders. Dr. Gupta uses endoscopic techniques for minimal invasiveness.",
    image: "assets/img/health/staff-2.webp",
    phone: "+1 (555) 012-0345",
    email: "anand.gupta@hospital.com",
    availability: "Wed, Fri, Sat 10:00 AM - 6:00 PM"
  },
  "DR.Shruti Patel": {
    name: "DR.Shruti Patel",
    specialty: "ENT Specialist, Audiologist",
    experience: "10+ Years",
    qualification: "MS (ENT), Au.D",
    description: "Expert in pediatric ENT and hearing aid fitting. Dr. Patel is passionate about improving quality of life through better hearing.",
    image: "assets/img/health/staff-3.webp",
    phone: "+1 (555) 123-0456",
    email: "shruti.patel@hospital.com",
    availability: "Mon, Wed, Fri 2:00 PM - 8:00 PM"
  },
  "DR.Rohit Verma": {
    name: "DR.Rohit Verma",
    specialty: "Gastroenterologist",
    experience: "14+ Years",
    qualification: "MD (Medicine), DM (Gastroenterology)",
    description: "Specialist in endoscopic procedures and liver disease. Dr. Verma is skilled in advanced GI interventions.",
    image: "assets/img/health/staff-1.webp",
    phone: "+1 (555) 234-0567",
    email: "rohit.verma@hospital.com",
    availability: "Mon, Wed, Fri 9:00 AM - 5:00 PM"
  },
  "DR.Priya Singh": {
    name: "DR.Priya Singh",
    specialty: "Gastroenterologist",
    experience: "12+ Years",
    qualification: "MD (Gastroenterology), DM",
    description: "Expert in IBD management and endoscopic therapy. Dr. Singh provides comprehensive digestive health care.",
    image: "assets/img/health/staff-2.webp",
    phone: "+1 (555) 345-0678",
    email: "priya.singh@hospital.com",
    availability: "Tue, Thu, Sat 10:00 AM - 6:00 PM"
  },
  "DR.Aditya Sengupta": {
    name: "DR.Aditya Sengupta",
    specialty: "Gastroenterologist, Hepatologist",
    experience: "13+ Years",
    qualification: "MD (Gastroenterology), DM (Hepatology)",
    description: "Specialized in liver diseases and hepatology. Dr. Sengupta is known for his expertise in complex GI cases.",
    image: "assets/img/health/staff-3.webp",
    phone: "+1 (555) 456-0789",
    email: "aditya.sengupta@hospital.com",
    availability: "Tue, Thu, Sat 11:00 AM - 7:00 PM"
  },
  "DR.Ramesh Kumar": {
    name: "DR.Ramesh Kumar",
    specialty: "General Medicine",
    experience: "20+ Years",
    qualification: "MD (General Medicine)",
    description: "Senior consultant with extensive experience in internal medicine and preventive care.",
    image: "assets/img/health/staff-1.webp",
    phone: "+1 (555) 567-0890",
    email: "ramesh.kumar@hospital.com",
    availability: "Mon-Fri 9:00 AM - 5:00 PM"
  },
  "DR.Pooja Menon": {
    name: "DR.Pooja Menon",
    specialty: "General Medicine",
    experience: "11+ Years",
    qualification: "MD (General Medicine)",
    description: "Compassionate physician dedicated to comprehensive patient care and wellness.",
    image: "assets/img/health/staff-2.webp",
    phone: "+1 (555) 678-0901",
    email: "pooja.menon@hospital.com",
    availability: "Tue, Thu, Sat 10:00 AM - 6:00 PM"
  }
};
