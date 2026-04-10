"""
Sprint 1 Unit Tests
Assigned to: Jiecheng
Run: pytest tests/test_auth.py -v
Screenshot output as TDD evidence for the report.
"""
import pytest
from unittest.mock import patch
from app.services.auth_login_controller  import AuthLoginController
from app.services.auth_logout_controller import AuthLogoutController
from app.services.account_controller   import AccountController
from app.services.register_controller  import RegisterController


# ── Helpers ───────────────────────────────────────────────────

def make_account(role='admin', is_active=1):
    return {
        'user_id': 1, 'username': 'testuser',
        'password_hash': 'hashed', 'isActive': is_active, 'role': role,
    }


# ══════════════════════════════════════════════════════════════
# LOGIN — AuthLoginController
# ══════════════════════════════════════════════════════════════

class TestLoginValidation:
    def test_empty_username(self):
        ok, d = AuthLoginController.login('', 'pass'); assert ok is False
    def test_whitespace_username(self):
        ok, d = AuthLoginController.login('   ', 'pass'); assert ok is False
    def test_empty_password(self):
        ok, d = AuthLoginController.login('admin01', ''); assert ok is False
    def test_both_empty(self):
        ok, d = AuthLoginController.login('', ''); assert ok is False


class TestLoginAltFlows:

    @patch('app.services.auth_login_controller.UserAccount.findByUsername', return_value=None)
    def test_alt1_account_not_found(self, _):
        ok, d = AuthLoginController.login('nobody', 'pass')
        assert ok is False and 'error' in d

    @patch('app.services.auth_login_controller.UserAccount.verifyPassword', return_value=False)
    @patch('app.services.auth_login_controller.UserAccount.findByUsername')
    def test_alt2_wrong_password(self, mock_find, _):
        mock_find.return_value = make_account()
        ok, d = AuthLoginController.login('admin01', 'wrong')
        assert ok is False

    @patch('app.services.auth_login_controller.UserAccount.verifyPassword', return_value=True)
    @patch('app.services.auth_login_controller.UserAccount.findByUsername')
    def test_alt3_suspended_account(self, mock_find, _):
        mock_find.return_value = make_account(is_active=0)
        ok, d = AuthLoginController.login('admin01', 'pass')
        assert ok is False


class TestLoginRoleRedirects:
    """Each role must redirect to the correct dashboard."""

    def _login(self, role, mock_find, mock_session):
        mock_find.return_value = make_account(role=role)
        mock_session.return_value = 'tok'
        return AuthLoginController.login('user', 'pass')

    @patch('app.services.auth_login_controller.UserSession.create', return_value='tok')
    @patch('app.services.auth_login_controller.UserAccount.verifyPassword', return_value=True)
    @patch('app.services.auth_login_controller.UserAccount.findByUsername')
    def test_admin_redirect(self, mock_find, _, mock_session):
        mock_find.return_value = make_account(role='admin')
        ok, d = AuthLoginController.login('admin01', 'pass')
        assert ok and d['redirectTo'] == '/admin/dashboard'
        assert d['role_label'] == 'User Admin'

    @patch('app.services.auth_login_controller.UserSession.create', return_value='tok')
    @patch('app.services.auth_login_controller.UserAccount.verifyPassword', return_value=True)
    @patch('app.services.auth_login_controller.UserAccount.findByUsername')
    def test_fund_raiser_redirect(self, mock_find, _, mock_session):
        mock_find.return_value = make_account(role='fund_raiser')
        ok, d = AuthLoginController.login('fr01', 'pass')
        assert ok and d['redirectTo'] == '/fr/dashboard'
        assert d['role_label'] == 'Fund Raiser'

    @patch('app.services.auth_login_controller.UserSession.create', return_value='tok')
    @patch('app.services.auth_login_controller.UserAccount.verifyPassword', return_value=True)
    @patch('app.services.auth_login_controller.UserAccount.findByUsername')
    def test_donee_redirect(self, mock_find, _, mock_session):
        mock_find.return_value = make_account(role='donee')
        ok, d = AuthLoginController.login('donee01', 'pass')
        assert ok and d['redirectTo'] == '/donee/dashboard'
        assert d['role_label'] == 'Donee'

    @patch('app.services.auth_login_controller.UserSession.create', return_value='tok')
    @patch('app.services.auth_login_controller.UserAccount.verifyPassword', return_value=True)
    @patch('app.services.auth_login_controller.UserAccount.findByUsername')
    def test_platform_manager_redirect(self, mock_find, _, mock_session):
        mock_find.return_value = make_account(role='platform_manager')
        ok, d = AuthLoginController.login('pm01', 'pass')
        assert ok and d['redirectTo'] == '/pm/dashboard'
        assert d['role_label'] == 'Platform Manager'

    @patch('app.services.auth_login_controller.UserSession.create', return_value='tok')
    @patch('app.services.auth_login_controller.UserAccount.verifyPassword', return_value=True)
    @patch('app.services.auth_login_controller.UserAccount.findByUsername')
    def test_session_created_on_login(self, mock_find, _, mock_session):
        mock_find.return_value = make_account()
        AuthLoginController.login('admin01', 'pass')
        mock_session.assert_called_once_with(1)


# ══════════════════════════════════════════════════════════════
# LOGOUT — AuthLogoutController
# ══════════════════════════════════════════════════════════════

class TestLogout:

    @patch('app.services.auth_logout_controller.UserAccount.logout')
    def test_logout_calls_useraccount(self, mock_logout):
        AuthLogoutController.logout('1')
        mock_logout.assert_called_once_with('1')

    @patch('app.services.auth_logout_controller.UserAccount.logout')
    def test_logout_none_safe(self, mock_logout):
        AuthLogoutController.logout(None)
        mock_logout.assert_not_called()

    @patch('app.services.auth_logout_controller.UserSession.expire')
    def test_logout_by_token(self, mock_expire):
        AuthLogoutController.logoutByToken('tok')
        mock_expire.assert_called_once_with('tok')

    @patch('app.services.auth_logout_controller.UserSession.expire')
    def test_logout_expired_token_safe(self, mock_expire):
        AuthLogoutController.logoutByToken('expired-tok')
        mock_expire.assert_called_once()


# ══════════════════════════════════════════════════════════════
# ADMIN CREATE ACCOUNT — AccountController (UA-03)
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
# SELF-REGISTER — RegisterController (GU-03)
# ══════════════════════════════════════════════════════════════

class TestSelfRegister:

    def _data(self, username='newuser', password='pass123', role='fund_raiser'):
        return {'username': username, 'password': password, 'role': role}

    def test_empty_username_fails(self):
        ok, d = RegisterController.registerUser(self._data(username=''))
        assert ok is False

    def test_short_password_fails(self):
        ok, d = RegisterController.registerUser(self._data(password='abc'))
        assert ok is False

    def test_admin_role_blocked(self):
        """Security: self-register must not allow admin role."""
        ok, d = RegisterController.registerUser(self._data(role='admin'))
        assert ok is False and 'role' in d['error'].lower()

    def test_platform_manager_role_blocked(self):
        """Security: self-register must not allow platform_manager role."""
        ok, d = RegisterController.registerUser(self._data(role='platform_manager'))
        assert ok is False and 'role' in d['error'].lower()

    def test_fund_raiser_role_allowed(self):
        """fund_raiser is a valid self-register role."""
        ok, _ = RegisterController.validateRole('fund_raiser')
        assert ok is True

    def test_donee_role_allowed(self):
        """donee is a valid self-register role."""
        ok, _ = RegisterController.validateRole('donee')
        assert ok is True

    @patch('app.services.register_controller.UserAccount.exists', return_value=True)
    def test_duplicate_username_fails(self, _):
        ok, d = RegisterController.registerUser(self._data())
        assert ok is False and 'exists' in d['error'].lower()

    @patch('app.services.register_controller.UserAccount.createAccount')
    @patch('app.services.register_controller.UserAccount.exists', return_value=False)
    def test_fund_raiser_register_success(self, _, mock_create):
        ok, d = RegisterController.registerUser(self._data(role='fund_raiser'))
        assert ok is True and 'message' in d
        mock_create.assert_called_once()

    @patch('app.services.register_controller.UserAccount.createAccount')
    @patch('app.services.register_controller.UserAccount.exists', return_value=False)
    def test_donee_register_success(self, _, mock_create):
        ok, d = RegisterController.registerUser(self._data(role='donee'))
        assert ok is True
