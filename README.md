# Task Manager

A simple, full‑stack task‑tracking application demonstrating:

- **Backend**: Python 3 + Flask, SQLAlchemy & Flask‑Migrate (SQLite by default)  
- **Frontend**: Vanilla HTML/CSS/JS (can be swapped for any framework)  
- **Auth**: HTTP Basic Auth (`admin:secret`)  
- **Tests**: `unittest` covering all API routes and error cases  

---

## Table of Contents

1. [Features](#features)  
2. [Prerequisites](#prerequisites)  
3. [Quick Start](#quick-start)  
4. [Run Scripts](#run-scripts)  
5. [Environment Variables](#environment-variables)  
6. [Project Structure](#project-structure)  
7. [API Endpoints](#api-endpoints)  
8. [Running Tests](#running-tests)  
9. [Interpreting Test Results](#interpreting-test-results)  
10. [Frontend Details](#frontend-details)  
11. [Database Migrations](#database-migrations)  
12. [Deployment & Production](#deployment--production)  
13. [Troubleshooting](#troubleshooting)  
14. [Extending the App](#extending-the-app)  

---

## Features

- **CRUD** on tasks: Create, Read (single/all), Update status, Delete  
- **Validation** of fields and ISO8601 due date  
- **Error handling** with JSON responses  
- **CORS** preflight support  
- **Unit tests** that reset the DB before each run  

---

## Prerequisites

- **Python** ≥ 3.9  
- **pip**  
- (Optional) **virtualenv** or **venv**  

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/your‑org/task-manager.git
cd task-manager

# 2. (Optional) Create & activate virtualenv
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy .env
cp .env.example .env

# 5. Run the helper script to migrate, test, and start
# Windows PowerShell:
.\run.ps1
# or on macOS/Linux:
./run.sh


.
├── .env
├── migrations/              
├── requirements.txt
├── run.ps1      # Windows helper
├── run.sh       # macOS/Linux helper
├── README.md
└── src
    ├── main
    │   └── python/uk/gov/hmcts/reform/dev
    │       ├── Application.py
    │       ├── controllers.py
    │       ├── errors.py
    │       ├── models.py
    │       └── schemas.py
    └── resources/static
        ├── index.html
        └── index.js
└── test.py      # root‑level unittest runner


All under /tasks, Basic Auth required.


Method	Path	Body	Response
GET	/tasks	—	200 OK + [{…},…]
POST	/tasks	{ title, status, description?, due? }	201 Created + task JSON
GET	/tasks/{id}	—	200 OK + task JSON
PATCH	/tasks/{id}/status	{ status }	200 OK + task JSON
DELETE	/tasks/{id}	—	204 No Content
OPTIONS	any /tasks*	—	204 No Content + CORS


Place a file called .env in the project root with:

ini
Copy
Edit
# .env
BASIC_AUTH_USERNAME=admin
BASIC_AUTH_PASSWORD=secret
SQLALCHEMY_DATABASE_URI=sqlite:///tasks.db
FLASK_ENV=development
BASIC_AUTH_USERNAME/PASSWORD: credentials for all API calls

SQLALCHEMY_DATABASE_URI: can point to any SQL database

FLASK_ENV: development enables debug mode



# 1. Clone the repo
git clone https://github.com/your‑org/task-manager.git
cd task-manager

# 2. Create a virtual environment (recommended)
python -m venv .venv
# Activate:
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
# Copy .env.example to .env and adjust if needed
cp .env.example .env

# 5. Initialize & apply database migrations
flask db init       # only first run
flask db migrate
flask db upgrade

# 6. Run unit tests
python -m unittest discover -v

# 7. Start the server
flask run
# → Listening on http://127.0.0.1:5000

