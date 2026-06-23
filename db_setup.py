import os
import sys
import bcrypt
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "varma1508",
    "database": "hospital_contact",
}

DEPARTMENT_DATA = [
    {"slug": "cardiology", "name": "Cardiology", "specialization": "Heart & Vascular"},
    {"slug": "neurology", "name": "Neurology", "specialization": "Brain & Nerves"},
    {"slug": "pediatrics", "name": "Pediatrics", "specialization": "Children's Health"},
    {"slug": "orthopedics", "name": "Orthopedics", "specialization": "Bone & Joint"},
    {"slug": "dermatology", "name": "Dermatology", "specialization": "Skin Care"},
    {"slug": "oncology", "name": "Oncology", "specialization": "Cancer Care"},
    {"slug": "general_medicine", "name": "General Medicine", "specialization": "Primary Care"},
    {"slug": "ent", "name": "ENT", "specialization": "Ear, Nose & Throat"},
    {"slug": "gastroenterology", "name": "Gastroenterology", "specialization": "Digestive Health"},
    {"slug": "nephrology", "name": "Nephrology", "specialization": "Kidney Care"},
    {"slug": "urology", "name": "Urology", "specialization": "Urinary & Reproductive"},
    {"slug": "pulmonology", "name": "Pulmonology", "specialization": "Lung Care"},
    {"slug": "endocrinology", "name": "Endocrinology", "specialization": "Hormone Health"},
    {"slug": "gynecology", "name": "Gynecology", "specialization": "Women's Health"},
    {"slug": "psychiatry", "name": "Psychiatry", "specialization": "Mental Health"},
]

DOCTOR_SEED = {
    "cardiology": ["DR.S.Arjun Reddy", "DR.Rajesh Kumar", "DR.Vikram Singh"],
    "neurology": ["DR.S.SaiPriya", "DR.T.Anu", "DR.Neha Sharma"],
    "pediatrics": ["DR.N.MadhuLatha", "DR.Priya Verma", "DR.Arun Nair"],
    "orthopedics": ["DR.M.Sameer", "DR.Ravi Patel", "DR.Suresh Gupta"],
    "dermatology": ["DR.N.lohith", "DR.Anjali Singh", "DR.Meera Joshi"],
    "oncology": ["DR.T.Anu", "DR.Ashok Kumar", "DR.Sneha Desai"],
    "general_medicine": ["DR.Ramesh Kumar", "DR.Pooja Menon", "DR.S.Arjun Reddy"],
    "ent": ["DR.Vikram Sharma", "DR.Anand Gupta", "DR.Shruti Patel"],
    "gastroenterology": ["DR.Rohit Verma", "DR.Priya Singh", "DR.Aditya Sengupta"],
    "nephrology": ["DR.Sanjay Kumar", "DR.Meera Nair", "DR.Rajiv Desai"],
    "urology": ["DR.Harsh Patel", "DR.Vikas Sharma", "DR.Amit Singh"],
    "pulmonology": ["DR.Deepak Verma", "DR.Sneha Kumar", "DR.Arjun Sharma"],
    "endocrinology": ["DR.Divya Singh", "DR.Ashok Nair", "DR.Priya Gupta"],
    "gynecology": ["DR.Ragini Sharma", "DR.Neha Verma", "DR.Anjali Patel"],
    "psychiatry": ["DR.Ramesh Singh", "DR.Anjali Kumar", "DR.Vikram Desai"],
}


def get_db_connection(use_database: bool = True):
    config = DB_CONFIG.copy()
    if not use_database:
        config.pop("database", None)
    return mysql.connector.connect(**config)


def create_database():
    conn = get_db_connection(use_database=False)
    cursor = conn.cursor()
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Database `{DB_CONFIG['database']}` ensured.")


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Admin (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(150) NOT NULL UNIQUE,
            passwordHash VARCHAR(255) NOT NULL,
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Department (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(150) NOT NULL,
            slug VARCHAR(150) NOT NULL UNIQUE,
            description TEXT NULL,
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Doctor (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            specialization VARCHAR(150) NULL,
            photoUrl VARCHAR(255) NULL,
            departmentId INT NOT NULL,
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (departmentId) REFERENCES Department(id) ON DELETE CASCADE,
            UNIQUE KEY unique_doctor_department (name, departmentId)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Appointment (
            id INT AUTO_INCREMENT PRIMARY KEY,
            doctorId INT NOT NULL,
            departmentId INT NOT NULL,
            patientName VARCHAR(200) NOT NULL,
            email VARCHAR(255) NOT NULL,
            phone VARCHAR(50) NOT NULL,
            appointment_date DATE NOT NULL,
            appointment_time TIME NOT NULL,
            notes TEXT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'Pending',
            createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (doctorId) REFERENCES Doctor(id) ON DELETE CASCADE,
            FOREIGN KEY (departmentId) REFERENCES Department(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
        """
    )

    cursor.close()
    conn.close()
    print("Required tables ensured.")


def deduplicate_doctors():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT name, departmentId, GROUP_CONCAT(id ORDER BY id ASC) AS ids, COUNT(*) AS cnt "
        "FROM Doctor "
        "GROUP BY name, departmentId "
        "HAVING COUNT(*) > 1"
    )
    duplicates = cursor.fetchall()
    if not duplicates:
        cursor.close()
        conn.close()
        return

    for row in duplicates:
        ids = [int(doct_id) for doct_id in row["ids"].split(",") if doct_id]
        keep_id, remove_ids = ids[0], ids[1:]
        if not remove_ids:
            continue

        format_strings = ",".join(["%s"] * len(remove_ids))
        cursor.execute(
            f"UPDATE Appointment SET doctorId = %s WHERE doctorId IN ({format_strings})",
            (keep_id, *remove_ids),
        )
        cursor.execute(
            f"DELETE FROM Doctor WHERE id IN ({format_strings})",
            tuple(remove_ids),
        )

    conn.commit()
    cursor.close()
    conn.close()
    print("Duplicate doctor records cleaned.")


def ensure_doctor_unique_index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SHOW INDEX FROM Doctor WHERE Key_name = 'unique_doctor_department'")
    if cursor.fetchone() is None:
        try:
            cursor.execute(
                "ALTER TABLE Doctor ADD UNIQUE INDEX unique_doctor_department (name, departmentId)"
            )
            conn.commit()
            print("Created unique doctor index.")
        except mysql.connector.Error as err:
            print(f"Could not create unique doctor index: {err}")
    cursor.close()
    conn.close()


def seed_departments_and_doctors():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    for department in DEPARTMENT_DATA:
        cursor.execute(
            "INSERT INTO Department (name, slug, description) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE name = VALUES(name), description = VALUES(description)",
            (department["name"], department["slug"], department["specialization"])
        )
    conn.commit()

    for slug, doctor_names in DOCTOR_SEED.items():
        cursor.execute("SELECT id FROM Department WHERE slug = %s", (slug,))
        row = cursor.fetchone()
        if not row:
            continue
        department_id = row["id"]
        for doctor_name in doctor_names:
            cursor.execute(
                "INSERT INTO Doctor (name, specialization, photoUrl, departmentId) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE specialization = VALUES(specialization), photoUrl = VALUES(photoUrl), departmentId = VALUES(departmentId)",
                (doctor_name, slug.replace("_", " ").title(), None, department_id)
            )
    conn.commit()
    cursor.close()
    conn.close()
    print("Departments and doctors seeded.")


def add_admin_user(username: str, password: str):
    if not username or not password:
        raise ValueError("Username and password cannot be empty.")

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Admin (username, passwordHash) VALUES (%s, %s) ON DUPLICATE KEY UPDATE passwordHash = VALUES(passwordHash)",
        (username, password_hash),
    )
    conn.commit()
    cursor.close()
    conn.close()
    print(f"Admin user '{username}' has been created or updated successfully.")


def print_usage():
    print("Usage: python db_setup.py <admin_username> <admin_password>")
    print("Example: python db_setup.py admin SuperSecret123")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage()
        sys.exit(1)

    admin_username = sys.argv[1].strip()
    admin_password = sys.argv[2].strip()
    if not admin_username or not admin_password:
        print_usage()
        sys.exit(1)

    create_database()
    create_tables()
    deduplicate_doctors()
    ensure_doctor_unique_index()
    seed_departments_and_doctors()
    add_admin_user(admin_username, admin_password)
    print("Database setup complete.")
