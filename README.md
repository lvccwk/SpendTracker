## Introduction

SpendTrackeris a system designed to record and categorize daily expenses. This guide provides detailed instructions for setting up and running the project locally.

---

## Installation Guide

### **1. Clone the Repository**

First, clone this project to your local environment:

```bash
git clone https://github.com/<your-username>/SpendTracker.git

cd SpendTracker


### 2. Create and Activate a Virtual Environment
Windows:
.\env\Scripts\activate

Mac/Linux:
source env/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt
pip install flask psycopg2
pip install python-dotenv
pip install flask psycopg2 bcrypt flask-jwt-extended


### 4. Configure Environment Variable
DB_NAME=expense_pocket
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

### 5. Initialize the Database
psql -U postgres -f /yourpath/init_database.sql

### 6. Run the Application
python -m venv env
python app.py

```
