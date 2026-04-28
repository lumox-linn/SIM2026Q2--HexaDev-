"""
conftest.py — runs before all tests.
Mocks flask_mysqldb so tests can import app modules
without needing a real MySQL connection.
"""
import sys
import os
import pytest
from unittest.mock import MagicMock, patch

# ── 1. Add backend/ to Python path ───────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

# ── 2. Mock flask_mysqldb before any app module is imported ──
mock_mysql = MagicMock()
sys.modules['flask_mysqldb'] = mock_mysql
sys.modules['MySQLdb']       = MagicMock()

# ── 3. Patch the mysql object in the app module ───────────────
import app as app_module
app_module.mysql = MagicMock()


# ── 4. Flask test client fixture ──────────────────────────────
@pytest.fixture
def app():
    from app import create_app
    application = create_app()
    application.config['TESTING'] = True
    application.config['SECRET_KEY'] = 'test-secret'
    yield application


@pytest.fixture
def client(app):
    return app.test_client()


# ── 5. Admin JWT token fixture ────────────────────────────────
@pytest.fixture
def admin_token():
    """Generate a valid JWT token for an admin user."""
    from app.utils.auth_utils import generate_token
    return generate_token(user_id=1, role='admin')


# ── 6. Mock current_user for token_required decorator ─────────
@pytest.fixture
def mock_admin_user():
    return {
        'user_id':   1,
        'username':  'admin01',
        'role':      'admin',
        'role_label': 'User Admin',
        'email':     None,
        'dob':       None,
        'avatar_url': None,
        'has_custom_avatar': False,
    }