from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import psycopg2
import bcrypt
from datetime import datetime
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'  # 替換為你的密鑰

jwt = JWTManager(app)

# 資料庫連接設定
def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
        
    )

# 用戶註冊
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
        connection.commit()
        connection.close()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 用戶登入
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT id, password_hash FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        connection.close()

        if user and bcrypt.checkpw(password.encode('utf-8'), user[1].encode('utf-8')):
            access_token = create_access_token(identity=user[0])
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"error": "Invalid credentials!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 新增支出記錄
@app.route('/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    current_user = get_jwt_identity()
    data = request.json
    amount = data['amount']
    category = data['category']
    date = data['date']
    description = data.get('description', '')

    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO expenses (user_id, amount, category, date, description) VALUES (%s, %s, %s, %s, %s)",
            (current_user, amount, category, date, description)
        )
        connection.commit()
        connection.close()
        return jsonify({"message": "Expense added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# 查詢所有支出記錄
@app.route('/expenses', methods=['GET'])
@jwt_required()
def get_expenses():
    current_user = get_jwt_identity()

    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT amount, category, date, description FROM expenses WHERE user_id = %s", (current_user,))
        expenses = cursor.fetchall()
        connection.close()
        return jsonify(expenses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
