from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import pymysql
pymysql.install_as_MySQLdb()

load_dotenv()

try:
    from flask_mysqldb import MySQL
    mysql = MySQL()
except Exception:
    from unittest.mock import MagicMock
    mysql = MagicMock()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY']         = os.getenv('SECRET_KEY', 'dev-secret')
    app.config['MYSQL_HOST']         = os.getenv('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER']         = os.getenv('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD']     = os.getenv('MYSQL_PASSWORD', '')
    app.config['MYSQL_DB']           = os.getenv('MYSQL_DB', 'csit314')
    app.config['MYSQL_PORT']         = int(os.getenv('MYSQL_PORT', 3306))
    app.config['MYSQL_CURSORCLASS']  = 'DictCursor'
    app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

    if os.getenv('MYSQL_SSL', 'false').lower() == 'true':
        app.config['MYSQL_SSL'] = {
            'ca': os.getenv('MYSQL_SSL_CA', 'certs/ca.pem')
        }

    CORS(app, origins='*', supports_credentials=False)
    mysql.init_app(app)

    # Sprint 1 routes
    from app.routes.auth_routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.routes.profile_routes import profile_bp
    app.register_blueprint(profile_bp, url_prefix='/api/profile')

    # Sprint 2 routes
    from app.routes.account_management_routes import account_management_bp
    app.register_blueprint(account_management_bp, url_prefix='/api/accounts')

    from app.routes.profile_management_routes import profile_management_bp
    app.register_blueprint(profile_management_bp, url_prefix='/api/profiles')

    # Sprint 3 routes
    from app.routes.category_routes import category_bp
    app.register_blueprint(category_bp, url_prefix='/api/categories')

    return app