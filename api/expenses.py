from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import psycopg2
import os

expenses_bp = Blueprint('expenses', __name__)

def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@expenses_bp.route('/expenses', methods=['POST'])
@jwt_required()
def add_expense():
    try:
        current_user = get_jwt_identity()
        data = request.json
        amount = data['amount']
        category = data['category']
        date = data['date']
        description = data.get('description', '')

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

@expenses_bp.route('/expenses', methods=['GET'])
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
