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
        'role': role, 'email': None, 'dob': None,
    }


# ══════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════

class TestLoginValidation:
    def test_empty_username(self):
        ok, d = AuthLoginCotroller.login('', 'pass')
        assert ok is False

    def test_whitespace_username(self):
        ok, d = AuthLoginCotroller.login('   ', 'pass')
        assert ok is False

    def test_empty_password(self):
        ok, d = AuthLoginCotroller.login('admin01', '')
        assert ok is False

    def test_both_empty(self):
        ok, d = AuthLoginCotroller.login('', '')
        assert ok is False


class TestLoginAltFlows:

    @patch('app.services.auth_login_cotroller.UserAccount.findByUsername', return_value=None)
    def test_alt1_account_not_found(self, _):
        ok, d = AuthLoginCotroller.login('nobody', 'pass')
        assert ok is False and 'error' in d

    @patch('app.services.auth_login_cotroller.UserAccount.verifyPassword', return_value=False)
    @patch('app.services.auth_login_cotroller.UserAccount.findByUsername')
    def test_alt2_wrong_password(self, mock_find, _):
        mock_find.return_value = make_account()
        ok, d = AuthLoginCotroller.login('admin01', 'wrong')
        assert ok is False

    @patch('app.services.auth_login_cotroller.UserAccount.verifyPassword', return_value=True)
    @patch('app.services.auth_login_cotroller.UserAccount.findByUsername')
    def test_alt3_suspended_account(self, mock_find, _):
        mock_find.return_value = make_account(is_active=0)
        ok, d = AuthLoginCotroller.login('admin01', 'pass')
        assert ok is False


class TestLoginRoleRedirects:

    @patch('app.services.auth_login_cotroller.UserSession.create', return_value='tok')
    @patch('app.services.auth_login_cotroller.UserAccount.verifyPassword', return_value=True)
    @patch('app.services.auth_login_cotroller.UserAccount.findByUsername')
    def test_admin_redirect(self, mock_find, _, __):
        mock_find.return_value = make_account(role='admin')
        ok, d = AuthLoginCotroller.login('admin01', 'pass')
        assert ok is True and d['redirectTo'] == '/home'
        assert d['role_label'] == 'User Admin'

    @patch('app.services.auth_login_cotroller.UserSession.create', return_value='tok')
    @patch('app.services.auth_login_cotroller.UserAccount.verifyPassword', return_value=True)
    @patch('app.services.auth_login_cotroller.UserAccount.findByUsername')
    def test_fund_raiser_redirect(self, mock_find, _, __):
        mock_find.return_value = make_account(role='fund_raiser')
        ok, d = AuthLoginCotroller.login('fr01', 'pass')
        assert ok is True and d['redirectTo'] == '/home'

    @patch('app.services.auth_login_cotroller.UserSession.create', return_value='tok')
    @patch('app.services.auth_login_cotroller.UserAccount.verifyPassword', return_value=True)
    @patch('app.services.auth_login_cotroller.UserAccount.findByUsername')
    def test_donee_redirect(self, mock_find, _, __):
        mock_find.return_value = make_account(role='donee')
        ok, d = AuthLoginCotroller.login('donee01', 'pass')
        assert ok is True and d['redirectTo'] == '/home'

    @patch('app.services.auth_login_cotroller.UserSession.create', return_value='tok')
    @patch('app.services.auth_login_cotroller.UserAccount.verifyPassword', return_value=True)
    @patch('app.services.auth_login_cotroller.UserAccount.findByUsername')
    def test_platform_manager_redirect(self, mock_find, _, __):
        mock_find.return_value = make_account(role='platform_manager')
        ok, d = AuthLoginCotroller.login('pm01', 'pass')
        assert ok is True and d['redirectTo'] == '/home'

    @patch('app.services.auth_login_cotroller.UserSession.create', return_value='tok')
    @patch('app.services.auth_login_cotroller.UserAccount.verifyPassword', return_value=True)
    @patch('app.services.auth_login_cotroller.UserAccount.findByUsername')
    def test_session_created_on_login(self, mock_find, _, mock_session):
        mock_find.return_value = make_account()
        AuthLoginCotroller.login('admin01', 'pass')
        mock_session.assert_called_once_with(1)


# ══════════════════════════════════════════════════════════════
# LOGOUT
# ══════════════════════════════════════════════════════════════

class TestLogout:

    @patch('app.services.auth_logout_cotroller.UserAccount.logout')
    def test_logout_calls_useraccount(self, mock_logout):
        AuthLogoutCotroller.logout('1')
        mock_logout.assert_called_once_with('1')

    @patch('app.services.auth_logout_cotroller.UserAccount.logout')
    def test_logout_none_safe(self, mock_logout):
        AuthLogoutCotroller.logout(None)
        mock_logout.assert_not_called()

    @patch('app.services.auth_logout_cotroller.UserSession.expire')
    def test_logout_by_token(self, mock_expire):
        AuthLogoutCotroller.logoutByToken('tok')
        mock_expire.assert_called_once_with('tok')

    @patch('app.services.auth_logout_cotroller.UserSession.expire')
    def test_logout_expired_token_safe(self, mock_expire):
        AuthLogoutCotroller.logoutByToken('expired-tok')
        mock_expire.assert_called_once()


# ══════════════════════════════════════════════════════════════
# ADMIN CREATE ACCOUNT
# ══════════════════════════════════════════════════════════════

class TestAdminCreateAccount:

    def _data(self, username='newuser', password='pass123', role='donee'):
        return {'username': username, 'password': password, 'role': role}

    def test_empty_username_fails(self):
        ok, d = AccountController.createUserAccount(self._data(username=''))
        assert ok is False

    def test_short_username_fails(self):
        ok, d = AccountController.createUserAccount(self._data(username='ab'))
        assert ok is False

    def test_empty_password_fails(self):
        ok, d = AccountController.createUserAccount(self._data(password=''))
        assert ok is False

    def test_short_password_fails(self):
        ok, d = AccountController.createUserAccount(self._data(password='abc'))
        assert ok is False

    def test_invalid_role_fails(self):
        ok, d = AccountController.createUserAccount(self._data(role='superuser'))
        assert ok is False

    @patch('app.services.account_controller.UserAccount.exists', return_value=True)
    def test_duplicate_username_fails(self, _):
        ok, d = AccountController.createUserAccount(self._data())
        assert ok is False and 'exists' in d['error'].lower()

    @patch('app.services.account_controller.UserAccount.createAccount')
    @patch('app.services.account_controller.UserAccount.exists', return_value=False)
    def test_admin_can_create_admin_role(self, _, mock_create):
        ok, d = AccountController.createUserAccount(self._data(role='admin'))
        assert ok is True
        mock_create.assert_called_once()

    @patch('app.services.account_controller.UserAccount.createAccount')
    @patch('app.services.account_controller.UserAccount.exists', return_value=False)
    def test_admin_can_create_platform_manager(self, _, mock_create):
        ok, d = AccountController.createUserAccount(self._data(role='platform_manager'))
        assert ok is True

    @patch('app.services.account_controller.UserAccount.createAccount')
    @patch('app.services.account_controller.UserAccount.exists', return_value=False)
    def test_create_success_returns_message(self, _, mock_create):
        ok, d = AccountController.createUserAccount(self._data())
        assert ok is True and 'message' in d


# ══════════════════════════════════════════════════════════════
# SELF REGISTER — updated: email required, role auto = donee
# ══════════════════════════════════════════════════════════════

class TestSelfRegister:

    def _data(self, username='newuser', password='pass123', email='test@test.com'):
        return {'username': username, 'password': password, 'email': email}

    def test_empty_username_fails(self):
        ok, d = RegisterController.registerUser(self._data(username=''))
        assert ok is False

    def test_short_password_fails(self):
        ok, d = RegisterController.registerUser(self._data(password='abc'))
        assert ok is False

    def test_empty_email_fails(self):
        ok, d = RegisterController.registerUser(self._data(email=''))
        assert ok is False

    def test_invalid_email_fails(self):
        ok, d = RegisterController.registerUser(self._data(email='notanemail'))
        assert ok is False

    @patch('app.services.register_controller.UserAccount.exists', return_value=True)
    def test_duplicate_username_fails(self, _):
        ok, d = RegisterController.registerUser(self._data())
        assert ok is False and 'exists' in d['error'].lower()

    @patch('app.services.register_controller.UserAccount.createAccount')
    @patch('app.services.register_controller.UserAccount.exists', return_value=False)
    def test_register_success(self, _, mock_create):
        ok, d = RegisterController.registerUser(self._data())
        assert ok is True and 'message' in d
        mock_create.assert_called_once()

    @patch('app.services.register_controller.UserAccount.createAccount')
    @patch('app.services.register_controller.UserAccount.exists', return_value=False)
    def test_role_is_always_donee(self, _, mock_create):
        """Role must always be donee regardless of what is sent."""
        ok, d = RegisterController.registerUser(self._data())
        assert ok is True
        call_args = mock_create.call_args[0][0]
        assert call_args['role'] == 'donee'

    @patch('app.services.register_controller.UserAccount.createAccount')
    @patch('app.services.register_controller.UserAccount.exists', return_value=False)
    def test_register_saves_email(self, _, mock_create):
        """Email must be saved during registration."""
        ok, d = RegisterController.registerUser(self._data(email='user@test.com'))
        assert ok is True
        call_args = mock_create.call_args[0][0]
        assert call_args['email'] == 'user@test.com'
