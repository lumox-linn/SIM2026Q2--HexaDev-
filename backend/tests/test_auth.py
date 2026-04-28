"""
Sprint 1 Unit Tests
Assigned to: Jiecheng
Run: pytest tests/test_auth.py -v
Screenshot output as TDD evidence for the report.
"""
import pytest
from unittest.mock import patch
from app.services.auth_login_cotroller  import AuthLoginCotroller
from app.services.auth_logout_cotroller import AuthLogoutCotroller
from app.services.account_controller   import AccountController
from app.services.register_controller  import RegisterController


def make_account(role='admin', is_active=1):
    return {
        'user_id': 1, 'username': 'testuser',
        'password_hash': 'hashed', 'isActive': is_active,
        'role': role, 'email': None, 'dob': None, 'profile_name': role, 'profile_status': 'active', 'profile_id': 1,
    }


# ══════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════

class TestLoginValidation:
    """Validation is now in Boundary (auth_routes.py) — test via route."""

    def test_empty_username(self, client):
        res = client.post('/api/auth/login', json={'username': '', 'password': 'pass'})
        assert res.status_code == 400

    def test_whitespace_username(self, client):
        res = client.post('/api/auth/login', json={'username': '   ', 'password': 'pass'})
        assert res.status_code == 400

    def test_empty_password(self, client):
        res = client.post('/api/auth/login', json={'username': 'admin01', 'password': ''})
        assert res.status_code == 400

    def test_both_empty(self, client):
        res = client.post('/api/auth/login', json={'username': '', 'password': ''})
        assert res.status_code == 400


class TestLoginAltFlows:

    @patch('app.services.auth_login_cotroller.UserAccount.login', return_value=None)
    def test_alt1_account_not_found(self, _):
        ok, d = AuthLoginCotroller.login('nobody', 'pass')
        assert ok is False and 'error' in d

    @patch('app.services.auth_login_cotroller.UserAccount.login', return_value=None)
    def test_alt2_wrong_password(self, _):
        ok, d = AuthLoginCotroller.login('admin01', 'wrong')
        assert ok is False

    @patch('app.services.auth_login_cotroller.UserAccount.login', return_value=None)
    def test_alt3_suspended_account(self, _):
        ok, d = AuthLoginCotroller.login('admin01', 'pass')
        assert ok is False


class TestLoginRoleRedirects:

    @patch('app.services.auth_login_cotroller.generate_token', return_value='jwt-tok')
    @patch('app.services.auth_login_cotroller.UserAccount.login')
    def test_admin_redirect(self, mock_login, mock_token):
        mock_login.return_value = make_account(role='admin')
        ok, d = AuthLoginCotroller.login('admin01', 'pass')
        assert ok is True and d['redirectTo'] == '/home'
        assert d['role_label'] == 'User Admin'

    @patch('app.services.auth_login_cotroller.generate_token', return_value='jwt-tok')
    @patch('app.services.auth_login_cotroller.UserAccount.login')
    def test_fund_raiser_redirect(self, mock_login, _):
        mock_login.return_value = make_account(role='fund_raiser')
        ok, d = AuthLoginCotroller.login('fr01', 'pass')
        assert ok is True and d['redirectTo'] == '/home'

    @patch('app.services.auth_login_cotroller.generate_token', return_value='jwt-tok')
    @patch('app.services.auth_login_cotroller.UserAccount.login')
    def test_donee_redirect(self, mock_login, _):
        mock_login.return_value = make_account(role='donee')
        ok, d = AuthLoginCotroller.login('donee01', 'pass')
        assert ok is True and d['redirectTo'] == '/home'

    @patch('app.services.auth_login_cotroller.generate_token', return_value='jwt-tok')
    @patch('app.services.auth_login_cotroller.UserAccount.login')
    def test_platform_manager_redirect(self, mock_login, _):
        mock_login.return_value = make_account(role='platform_manager')
        ok, d = AuthLoginCotroller.login('pm01', 'pass')
        assert ok is True and d['redirectTo'] == '/home'

    @patch('app.services.auth_login_cotroller.generate_token', return_value='jwt-tok')
    @patch('app.services.auth_login_cotroller.UserAccount.login')
    def test_token_returned_on_login(self, mock_login, mock_token):
        """JWT token is returned on successful login."""
        mock_login.return_value = make_account()
        ok, d = AuthLoginCotroller.login('admin01', 'pass')
        assert ok is True
        assert 'token' in d
        mock_token.assert_called_once_with(1, 'admin')


# ══════════════════════════════════════════════════════════════
# LOGOUT
# ══════════════════════════════════════════════════════════════

class TestLogout:

    def test_logout_returns_true(self):
        """JWT logout is stateless — always returns True."""
        result = AuthLogoutCotroller.logout()
        assert result is True

    def test_logout_no_db_needed(self):
        """JWT logout requires no DB operation — just returns success."""
        result = AuthLogoutCotroller.logout()
        assert result is True

    def test_logout_idempotent(self):
        """Calling logout multiple times is safe."""
        assert AuthLogoutCotroller.logout() is True
        assert AuthLogoutCotroller.logout() is True

    def test_logout_frontend_clears_token(self):
        """Backend logout is a no-op — frontend clears JWT from localStorage."""
        result = AuthLogoutCotroller.logout()
        assert result is True


# ══════════════════════════════════════════════════════════════
# ADMIN CREATE ACCOUNT
# ══════════════════════════════════════════════════════════════

class TestAdminCreateAccount:
    """Validation is now in Boundary (auth_routes.py) — test via route."""

    def test_empty_username_fails(self, client, admin_token):
        res = client.post('/api/auth/accounts',
            json={'username': '', 'password': 'pass123', 'role': 'donee'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert res.status_code == 400

    def test_short_username_fails(self, client, admin_token):
        res = client.post('/api/auth/accounts',
            json={'username': 'ab', 'password': 'pass123', 'role': 'donee'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert res.status_code == 400

    def test_empty_password_fails(self, client, admin_token):
        res = client.post('/api/auth/accounts',
            json={'username': 'newuser', 'password': '', 'role': 'donee'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert res.status_code == 400

    def test_short_password_fails(self, client, admin_token):
        res = client.post('/api/auth/accounts',
            json={'username': 'newuser', 'password': 'abc', 'role': 'donee'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert res.status_code == 400

    def test_invalid_role_fails(self, client, admin_token):
        res = client.post('/api/auth/accounts',
            json={'username': 'newuser', 'password': 'pass123', 'role': 'superuser'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert res.status_code == 400

    @patch('app.services.account_controller.UserAccount.createIfNotExists', return_value=None)
    def test_duplicate_username_fails(self, _, client, admin_token):
        res = client.post('/api/auth/accounts',
            json={'username': 'newuser', 'password': 'pass123', 'role': 'donee'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert res.status_code == 400
        assert 'exists' in res.get_json()['error'].lower()

    @patch('app.services.account_controller.UserAccount.createIfNotExists', return_value=True)
    def test_admin_can_create_admin_role(self, mock_create, client, admin_token):
        res = client.post('/api/auth/accounts',
            json={'username': 'newadmin', 'password': 'pass123', 'role': 'admin'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert res.status_code == 201

    @patch('app.services.account_controller.UserAccount.createIfNotExists', return_value=True)
    def test_admin_can_create_platform_manager(self, _, client, admin_token):
        res = client.post('/api/auth/accounts',
            json={'username': 'newpm', 'password': 'pass123', 'role': 'platform_manager'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert res.status_code == 201

    @patch('app.services.account_controller.UserAccount.createIfNotExists', return_value=True)
    def test_create_success_returns_message(self, _, client, admin_token):
        res = client.post('/api/auth/accounts',
            json={'username': 'newuser', 'password': 'pass123', 'role': 'donee'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert res.status_code == 201
        assert 'message' in res.get_json()


# ══════════════════════════════════════════════════════════════
# SELF REGISTER — updated: email required, role auto = donee
# ══════════════════════════════════════════════════════════════

class TestSelfRegister:

    def test_empty_username_fails(self, client):
        res = client.post('/api/auth/register',
            json={'username': '', 'password': 'pass123', 'email': 'test@test.com'})
        assert res.status_code == 400

    def test_short_password_fails(self, client):
        res = client.post('/api/auth/register',
            json={'username': 'newuser', 'password': 'abc', 'email': 'test@test.com'})
        assert res.status_code == 400

    def test_empty_email_fails(self, client):
        res = client.post('/api/auth/register',
            json={'username': 'newuser', 'password': 'pass123', 'email': ''})
        assert res.status_code == 400

    def test_invalid_email_fails(self, client):
        res = client.post('/api/auth/register',
            json={'username': 'newuser', 'password': 'pass123', 'email': 'notanemail'})
        assert res.status_code == 400

    @patch('app.services.register_controller.UserAccount.register', return_value=None)
    def test_duplicate_username_fails(self, _, client):
        res = client.post('/api/auth/register',
            json={'username': 'newuser', 'password': 'pass123', 'email': 'test@test.com'})
        assert res.status_code == 400
        assert 'exists' in res.get_json()['error'].lower()

    @patch('app.services.register_controller.UserAccount.register', return_value=True)
    def test_register_success(self, _, client):
        res = client.post('/api/auth/register',
            json={'username': 'newuser', 'password': 'pass123', 'email': 'test@test.com'})
        assert res.status_code == 201
        assert 'message' in res.get_json()

    @patch('app.services.register_controller.UserAccount.register', return_value=True)
    def test_role_is_always_donee(self, mock_register, client):
        """Role must always be donee regardless of what is sent."""
        client.post('/api/auth/register',
            json={'username': 'newuser', 'password': 'pass123', 'email': 'test@test.com'})
        call_args = mock_register.call_args[0][0]
        assert call_args['role'] == 'donee'

    @patch('app.services.register_controller.UserAccount.register', return_value=True)
    def test_register_saves_email(self, mock_register, client):
        """Email must be saved during registration."""
        client.post('/api/auth/register',
            json={'username': 'newuser', 'password': 'pass123', 'email': 'user@test.com'})
        call_args = mock_register.call_args[0][0]
        assert call_args['email'] == 'user@test.com'