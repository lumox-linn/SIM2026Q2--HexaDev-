"""
conftest.py — runs before all tests.
Mocks flask_mysqldb so tests can import app modules
without needing a real MySQL connection.
"""
import sys
import os
from unittest.mock import MagicMock, patch

# ── 1. Add backend/ to Python path ───────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

# ── 2. Mock flask_mysqldb before any app module is imported ──
# This prevents "No module named 'flask_mysqldb'" errors in CI
# and stops the app from trying to connect to MySQL during tests.
mock_mysql = MagicMock()
sys.modules['flask_mysqldb'] = mock_mysql
sys.modules['MySQLdb']       = MagicMock()

# ── 3. Create a minimal Flask app for testing ─────────────────
from flask import Flask

def create_test_app():
    app = Flask(__name__)
    app.config['TESTING']   = True
    app.config['SECRET_KEY'] = 'test-secret'
    return app

# Patch the mysql object in the app module before tests run
import importlib
import app as app_module
app_module.mysql = MagicMock()
