# TECHSPIRE Learning - Production-Ready Django LMS Platform
> **Tagline:** *Learn Today, Lead Tomorrow.*

TECHSPIRE Learning is a full-featured, production-ready Learning Management System (LMS) built with Django, PostgreSQL/SQLite, Bootstrap 5, and custom UI design. It provides structured course modules, interactive quizzes, automated lesson progression, student dashboards, and downloadable PDF course completion certificates with online verification and QR code lookup.

---

## 🏢 Business & Legal Information
- **Brand Name:** TECHSPIRE Learning
- **Business Entity:** TECHSPIRE (Proprietorship / Micro Enterprise)
- **Proprietor / Legal Name:** Vivek Jat
- **Headquarters / Location:** Indore, Madhya Pradesh, India
- **Address:** 53/43 Radhaswami Nagar, Nowlakha, Indore, Madhya Pradesh 452001
- **Email:** vivekjat301@gmail.com
- **Phone:** +91 9713931301
- **Udyam Registration:** UDYAM-MP-23-0283495
- **GSTIN:** 23BEZPJ5728J1ZW

---

## 🚀 Key Features

1. **Course & Curriculum Management**
   - 7 Pre-configured learning tracks: *Web Development, Python Programming, Data Analytics, AI Tools, Digital Marketing, Basic Computer Skills, MS Office Skills*.
   - Multi-module courses with video lessons, rich tutorial reading panes, and downloadable resources.
   - Course catalog with faceted category filters, keyword search, difficulty level filters, and sorting.

2. **LMS Classroom Learning Interface**
   - Sticky syllabus sidebar with active lesson highlighting and real-time progress checklist.
   - One-click "Mark Complete & Next" navigation.
   - Dynamic progress tracking calculating percentage of completed course material.

3. **Assessment & Quiz Engine**
   - MCQ assessment engine with configurable passing thresholds (e.g. 70%) and time limits.
   - Instant automated scoring, attempt tracking, and detailed question-by-question review with explanations.

4. **Tamper-Proof Certificates & Public Verification**
   - Automatically generated upon 100% course completion and passing score.
   - Unique Certificate ID (`TS-2026-XXXXXXXX`) and high-resolution QR code.
   - Downloadable landscape PDF certificate generated dynamically via ReportLab with Vivek Jat's signature, golden seal, and Indore registration details.
   - Public Certificate Verification Portal (`/verify-certificate/`) for instant live authenticity check.

5. **Student & Admin Portals**
   - Student Dashboard with real-time statistics, active course progress bars, recent assessment scores, and certificate vault.
   - Extended Django admin portal for managing categories, courses, lessons, questions, enrollments, certificates, and inquiries.

---

## 💻 Quick Start Guide (Local Setup)

### 1. Clone & Setup Virtual Environment
```bash
# Navigate to project folder
cd Techspire

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
.\venv\Scripts\activate
# Activate virtual environment (Linux/macOS)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `.env.example` to `.env` (optional, defaults are configured out-of-the-box):
```bash
copy .env.example .env
```

### 3. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Seed Comprehensive Production & Demo Data
Run our custom seeding command to pre-populate all 7 categories, 4 comprehensive courses with modules, lessons, quizzes, FAQs, testimonials, and demo credentials:
```bash
python manage.py seed_techspire_data
```

### 5. Start Development Server
```bash
python manage.py runserver
```
Visit: **`http://127.0.0.1:8000/`**

---

## 🔑 Pre-Seeded Demo Credentials

| Role | Email | Password | Access Area |
| :--- | :--- | :--- | :--- |
| **Super Admin** | `admin@techspire.in` | `Admin@12345` | `/admin/` & Student Dashboard |
| **Demo Student** | `student@techspire.in` | `Student@12345` | Student LMS Dashboard |

---

## 🐳 Docker & Docker Compose Deployment

Run the complete stack with PostgreSQL and Gunicorn in one command:
```bash
docker-compose up --build
```
The application will automatically run migrations, seed data, and start serving on `http://localhost:8000`.

---

## 🛠️ Production Deployment (Ubuntu + Gunicorn + Nginx)

1. **Install System Dependencies:**
   ```bash
   sudo apt update && sudo apt install python3-pip python3-venv postgresql nginx git
   ```
2. **Setup PostgreSQL Database:**
   ```sql
   CREATE DATABASE techspire_db;
   CREATE USER techspire_user WITH PASSWORD 'strong_password';
   GRANT ALL PRIVILEGES ON DATABASE techspire_db TO techspire_user;
   ```
3. **Configure Gunicorn Service (`/etc/systemd/system/techspire.service`):**
   ```ini
   [Unit]
   Description=Gunicorn daemon for TECHSPIRE Learning
   After=network.target

   [Service]
   User=www-data
   Group=www-data
   WorkingDirectory=/home/ubuntu/Techspire
   ExecStart=/home/ubuntu/Techspire/venv/bin/gunicorn --workers 3 --bind unix:/run/techspire.sock techspire_project.wsgi:application

   [Install]
   WantedBy=multi-user.target
   ```
4. **Configure Nginx Site (`/etc/nginx/sites-available/techspire`):**
   ```nginx
   server {
       listen 80;
       server_name techspire.in www.techspire.in;

       location /static/ {
           root /home/ubuntu/Techspire;
       }

       location /media/ {
           root /home/ubuntu/Techspire;
       }

       location / {
           include proxy_params;
           proxy_pass http://unix:/run/techspire.sock;
       }
   }
   ```
5. **SSL Certificate Setup:**
   ```bash
   sudo certbot --nginx -d techspire.in -d www.techspire.in
   ```
