# 🏫 School Student Management System

A production-ready Django 6.0 web application designed to manage student profiles, track daily attendance, record subject grades/marks, and generate school-wide analytics. 

This repository is optimized for both **local Docker-based development (MySQL)** and **production-ready serverless hosting (Vercel + Neon PostgreSQL)**.

---

## 👥 Credits & Contributors
* **Application Development**: Developed by **Kameshwari** ([@kameshwariX](https://github.com/kameshwariX)) — designed the core Django models, custom authentication roles, data templates, management views, and interactive user interfaces.
* **DevOps, Infrastructure & Deployment**: Configured by **Suvakovan** ([@suvakovan](https://github.com/suvakovan)) — containerized local database pipelines using Docker Compose, restructured environment settings, bypassed serverless driver compatibility hurdles, and automated CI/CD pipeline deployment to Vercel with Neon PostgreSQL.

---

## 🚀 Live Demo
* **Deployment URL**: [https://school-students-next.vercel.app/](https://school-students-next.vercel.app/)
* **Default Teacher Account (Sample)**:
  * **Username**: `teacher1`
  * **Password**: `TeacherPass123!`

---

## 🛠️ Technology Stack
* **Framework**: Django 6.0 (Python 3.12)
* **Frontend**: HTML5, CSS3, JavaScript (Responsive Dashboard)
* **Production Database**: Neon Serverless PostgreSQL (Hosted on Vercel)
* **Local Development Database**: MySQL 8.0 (Containerized via Docker)
* **Hosting Platform**: Vercel Serverless Functions

---

## ✨ Features
1. **Interactive Dashboard**: Real-time metrics showing total enrolled students, today's attendance rate, and class summaries.
2. **Student Roster Management**: Add, view, edit, and delete student records with customized roll numbers and parent contacts.
3. **Attendance Tracker**: Digital attendance register allowing teachers to record daily status (Present/Absent).
4. **Grades & Marks Logger**: Add exam marks for Mathematics, Science, English, etc.
5. **Role-Based Authentication**: Custom User models separating Teachers and Administration views.
6. **Zero-Configuration Vercel Engine**: Configured to run on Vercel’s serverless architecture with pre-installed static file collections.

---

## 💻 Local Development Setup (MySQL + Docker)

Follow these steps to run the application locally on your machine:

### 1. Prerequisites
Ensure you have the following installed:
* [Python 3.12](https://www.python.org/downloads/)
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Git](https://git-scm.com/)

### 2. Clone the Repository & Install Dependencies
```bash
git clone https://github.com/suvakovan/SCHOOL-STUDENTS.git
cd SCHOOL-STUDENTS
```

Create and activate a Python virtual environment:
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Spin Up the Local Database
We use Docker Compose to run a local MySQL database and a database admin tool (Adminer):
```bash
cd database
docker-compose up -d
cd ..
```
*This hosts MySQL on `localhost:3306` and Adminer on `http://localhost:8080`.*

### 4. Create the Environment File
Create a `.env` file in the root folder of the project with the following configuration:
```env
SECRET_KEY=django-insecure-your-local-dev-key
DEBUG=True

DB_ENGINE=django.db.backends.mysql
DB_NAME=school_db
DB_USER=root
DB_PASSWORD=root
DB_HOST=127.0.0.1
DB_PORT=3306
```

### 5. Run Migrations & Populate Data
Build the SQL tables and load sample students into your database:
```bash
python manage.py migrate
python populate_sample_data.py
```

### 6. Run the Development Server
```bash
python manage.py runserver
```
Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser to view the local site!

---

## ☁️ Production Deployment on Vercel (Postgres)

This project uses Vercel's Serverless Python runtime. Follow this guide to deploy it to production:

### 1. Database Configuration
1. Create a free **PostgreSQL** database on **[Neon.tech](https://neon.tech/)**.
2. Connect Neon to your Vercel project under the **Storage** tab. Vercel will automatically generate the environment variables with the prefix `POSTGRES_` (e.g., `POSTGRES_HOST`, `POSTGRES_PASSWORD`).
3. The Django database engine (`settings.py`) automatically detects these environment variables and switches to PostgreSQL when running in production.

### 2. Run Database Migrations in the Cloud
Since serverless runtimes do not support console command execution:
1. Temporarily replace your local `.env` file values with your decrypted production Neon Postgres credentials.
2. Run the migration and data generator scripts locally to write the tables directly to the cloud instance:
   ```bash
   python manage.py migrate
   python populate_sample_data.py
   ```
3. Restore your local `.env` back to your MySQL credentials for local development.

### 3. Push and Deploy
To deploy your site, commit your changes and push them to your repository's `main` branch. Vercel will automatically detect the commit, run `collectstatic` to bundle static assets, and host the web application on the edge.

---

## 📂 Project Structure
```text
├── database/
│   ├── docker-compose.yml       # Local MySQL and Adminer containers
│   └── init.sql                 # SQL DB initialization script
├── student_project/
│   ├── settings.py              # Django main settings (Hybrid database logic)
│   ├── urls.py                  # Project-wide routing
│   └── wsgi.py                  # WSGI entrypoint for Vercel
├── students/
│   ├── models.py                # Database schemas (Student, Subject, Attendance, Marks)
│   ├── views.py                 # Views handling template rendering & dashboards
│   └── urls.py                  # App-specific routes
├── templates/                   # Frontend HTML files
├── static/                      # Styling assets (CSS and JS files)
├── requirements.txt             # Python packages
├── vercel.json                  # Vercel serverless routing configuration
└── populate_sample_data.py      # Automated database populator script
```
