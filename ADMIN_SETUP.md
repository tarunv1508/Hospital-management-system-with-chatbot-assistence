# Admin Module Setup Instructions

## Overview

The admin module has been fully implemented with:
- **JWT-based authentication** with bcrypt password hashing
- **MySQL Admin, Department, Doctor, and Appointment tables**
- **Protected REST APIs** for admin dashboard
- **Frontend admin page** with login and dashboard views

## Quick Setup

### 1. Create Admin User and Seed Database

Run the database setup script to create all tables and seed data:

```bash
python db_setup.py admin SuperSecret123
```

Replace `admin` with your desired username and `SuperSecret123` with your secure password.

**Or**, use the legacy script:
```bash
python create_admin_user.py admin SuperSecret123
```

### 2. Start Backend Server

```bash
python backend.py
```

Server runs on `http://localhost:5000`

### 3. Access Admin Dashboard

Open your browser and navigate to:
```
http://localhost:5000/admin
```

## Login & Features

**Credentials:**
- Username: `admin` (or whatever you set in setup)
- Password: `SuperSecret123` (or your custom password)

**Dashboard Features:**
- **Stats Overview**: Total appointments, departments, doctors
- **Department Management**: Browse all departments with doctor counts
- **Doctor Selection**: View doctors per department
- **Appointment Viewer**: See all appointments for a selected doctor

## API Endpoints

### Authentication
- `POST /api/admin/login` — Login with username/password (sets JWT cookie)
- `POST /api/admin/logout` — Clear JWT token cookie

### Admin Protected Endpoints (require valid JWT cookie)
- `GET /api/admin/summary` — Dashboard statistics
- `GET /api/departments` — List all departments with doctor counts
- `GET /api/departments/<id>/doctors` — Get doctors in a department
- `GET /api/doctors/<id>/appointments` — Get appointments for a doctor

## Database Schema

**Admin Table:**
```sql
CREATE TABLE Admin (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(150) UNIQUE,
    passwordHash VARCHAR(255),
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Department Table:**
```sql
CREATE TABLE Department (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(150),
    slug VARCHAR(150) UNIQUE,
    description TEXT,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Doctor Table:**
```sql
CREATE TABLE Doctor (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(200),
    specialization VARCHAR(150),
    photoUrl VARCHAR(255),
    departmentId INT FOREIGN KEY,
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Appointment Table:**
```sql
CREATE TABLE Appointment (
    id INT PRIMARY KEY AUTO_INCREMENT,
    doctorId INT FOREIGN KEY,
    departmentId INT FOREIGN KEY,
    patientName VARCHAR(200),
    email VARCHAR(255),
    phone VARCHAR(50),
    appointment_date DATE,
    appointment_time TIME,
    notes TEXT,
    status VARCHAR(50) DEFAULT 'Pending',
    createdAt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Troubleshooting

### "Invalid admin username or password"
- Ensure you ran the setup script and created the admin user
- Check that the password is correct
- Verify the `Admin` table exists in MySQL: `SELECT * FROM Admin;`

### "Unauthorized access"
- Admin token may have expired (1 hour default)
- Log out and log back in
- Check browser cookies for `admin_token`

### Database Connection Error
- Verify MySQL is running
- Check DB_CONFIG in `backend.py`: host, user, password, database
- Ensure `hospital_contact` database exists

### "No appointments found"
- Ensure appointments exist in the `Appointment` table
- Go to the public appointment page and book an appointment first
- Refresh the admin dashboard

## Architecture

### Frontend (admin.html + assets/js/admin.js)
- Login form (POST to `/api/admin/login`)
- Dashboard with stats cards
- Department cards with "View Doctors" button
- Modal for doctor selection
- Appointments table for selected doctor

### Backend (backend.py)
- `admin_required()` middleware checks JWT cookie
- `create_jwt_token()` creates 1-hour JWT tokens
- `/api/admin/login` authenticates and sets secure HTTP-only cookie
- Protected API routes enforce JWT validation

### Database (MySQL)
- Admin stores bcrypt-hashed passwords
- Foreign key relationships link departments → doctors → appointments
- Appointment schema supports booking flow from frontend

## Security Notes

- Passwords are hashed with bcrypt (not plaintext or SHA256)
- JWT tokens are HTTP-only cookies (not accessible to JS)
- Admin APIs require valid JWT token to access
- Admin login tokens expire after 1 hour
- All admin endpoints are protected by `admin_required()` decorator
