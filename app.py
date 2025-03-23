from flask import Flask
import psycopg2
from dotenv import load_dotenv
import os

# 加載 .env 文件
load_dotenv()

app = Flask(__name__)

# 配置資料庫連接
def connect_db():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )

@app.route('/')
def home():
    try:
        connection = connect_db()
        cursor = connection.cursor()
        cursor.execute("SELECT 'Connection successful!'")
        message = cursor.fetchone()[0]
        connection.close()
        return message
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
