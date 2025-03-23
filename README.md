## Introduction

ExpensePocket is a system designed to record and categorize daily expenses. This guide provides detailed instructions for setting up and running the project locally.

---

## Installation Guide

### **1. Clone the Repository**

First, clone this project to your local environment:

```bash
git clone https://github.com/<your-username>/ExpensePocket.git

cd ExpensePocket


### 2. Create and Activate a Virtual Environment
Windows:
.\env\Scripts\activate

Mac/Linux:
source env/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt
pip install flask psycopg2
pip install python-dotenv


### 4. Configure Environment Variable
DB_NAME=expense_pocket
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

### 5. Initialize the Database
CREATE DATABASE expense_pocket;

CREATE TABLE users (
id SERIAL PRIMARY KEY,
username VARCHAR(50) UNIQUE NOT NULL,
password_hash TEXT NOT NULL
);

CREATE TABLE expenses (
id SERIAL PRIMARY KEY,
user_id INT NOT NULL,
amount DECIMAL(10, 2) NOT NULL,
category VARCHAR(50) NOT NULL,
date DATE NOT NULL,
description TEXT,
FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

### 6. Run the Application
python -m venv env
python app.py

```
