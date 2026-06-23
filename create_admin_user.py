import sys
import bcrypt
import mysql.connector

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "varma1508",
    "database": "hospital_contact",
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


def ensure_admin_table():
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
    conn.commit()
    cursor.close()
    conn.close()


def add_admin_user(username: str, password: str):
    if not username or not password:
        raise ValueError("Username and password cannot be empty.")

    password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Admin (username, passwordHash) VALUES (%s, %s)"
        " ON DUPLICATE KEY UPDATE passwordHash = VALUES(passwordHash)",
        (username, password_hash),
    )
    conn.commit()
    cursor.close()
    conn.close()


def print_usage():
    print("Usage: python create_admin_user.py <username> <password>")
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_usage()

    username = sys.argv[1].strip()
    password = sys.argv[2].strip()
    if not username or not password:
        print_usage()

    ensure_admin_table()
    add_admin_user(username, password)
    print(f"Admin user '{username}' has been created or updated successfully.")
