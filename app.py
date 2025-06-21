from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
jwt = JWTManager(app)
CORS(app)  # 允許所有來源

# 导入API路由
from api.users import users_bp
from api.expenses import expenses_bp

app.register_blueprint(users_bp, url_prefix='/api')
app.register_blueprint(expenses_bp, url_prefix='/api')

@app.route('/')
def home():
    return "Welcome to SpendTracker API!"

if __name__ == '__main__':
    app.run(debug=True)
