from flask import Blueprint, request, jsonify
import bcrypt
import psycopg2
import os

users_bp = Blueprint('users', __name__)

def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)",
            (username, password_hash.decode('utf-8')))
        connection.commit()
        connection.close()
        return jsonify({"message": "User registered successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@users_bp.route('/login', methods=['POST'])
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
            from flask_jwt_extended import create_access_token
            access_token = create_access_token(identity=user[0])
            return jsonify({"access_token": access_token}), 200
        else:
            return jsonify({"error": "Invalid credentials!"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 400
