"""
Sprint 2 Unit Tests — Account Management
Assigned to: Jiecheng
Run: pytest tests/test_account_management.py -v

TDD approach:
  - Tests written BEFORE implementation code
  - All database calls are mocked (no real DB needed)
  - Tests cover UA-07 to UA-10 (account management)
  - Tests cover UA-01 to UA-05 (profile management)
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.account_management_controller import AccountManagementController


def make_account(
    user_id=1,
    username='testuser',
    role='donee',
    is_active=1,
    email='test@test.com',
    phone='12345678',
    dob='2000-01-01'
):
    """Helper — creates a fake account dict like a real DB row."""
    return {
        'user_id':       user_id,
        'username':      username,
        'password_hash': 'hashed',
        'isActive':      is_active,
        'role':          role,
        'email':         email,
        'phone':         phone,
        'dob':           dob,
        'profile_picture': None,
        'created_at':    '2026-01-01 00:00:00',
    }


# ══════════════════════════════════════════════════════════════
# UA-07 — VIEW USER ACCOUNT
# ══════════════════════════════════════════════════════════════

class TestViewAccount:

    @patch('app.services.account_management_controller.UserAccount.findById',
           return_value=None)
    def test_view_account_not_found(self, mock_find):
        """Returns fail if account does not exist."""
        ok, d = AccountManagementController.viewAccount(999)
        assert ok is False
        assert 'error' in d

    @patch('app.services.account_management_controller.UserAccount.findById')
    def test_view_account_success(self, mock_find):
        """Returns account data if found."""
        mock_find.return_value = make_account()
        ok, d = AccountManagementController.viewAccount(1)
        assert ok is True
        assert d['status'] == 'success'
        assert d['account']['username'] == 'testuser'

    @patch('app.services.account_management_controller.UserAccount.findById')
    def test_view_account_returns_correct_fields(self, mock_find):
        """Response must include all required fields."""
        mock_find.return_value = make_account(role='admin', email='admin@test.com')
        ok, d = AccountManagementController.viewAccount(1)
        assert ok is True
        account = d['account']
        assert 'username'   in account
        assert 'role'       in account
        assert 'isActive'   in account
        assert 'email'      in account
        assert 'phone'      in account
        assert 'dob'        in account
        assert 'password_hash' not in account  # never return password


# ══════════════════════════════════════════════════════════════
# UA-08 — UPDATE USER ACCOUNT
# ══════════════════════════════════════════════════════════════

class TestUpdateAccount:

    def _data(self, **kwargs):
        base = {'email': 'new@test.com', 'phone': '99999999', 'dob': '2000-01-01'}
        base.update(kwargs)
        return base

    @patch('app.services.account_management_controller.UserAccount.findById',
           return_value=None)
    def test_update_account_not_found(self, mock_find):
        """Returns fail if account does not exist."""
        ok, d = AccountManagementController.updateAccount(999, self._data())
        assert ok is False
        assert 'error' in d

    @patch('app.services.account_management_controller.UserAccount.updateAccount')
    @patch('app.services.account_management_controller.UserAccount.findById')
    def test_update_account_success(self, mock_find, mock_update):
        """Updates account and returns success."""
        mock_find.return_value = make_account()
        ok, d = AccountManagementController.updateAccount(1, self._data())
        assert ok is True
        assert d['status'] == 'success'
        mock_update.assert_called_once()

    @patch('app.services.account_management_controller.UserAccount.findById')
    def test_update_invalid_email(self, mock_find):
        """Invalid email format should fail."""
        mock_find.return_value = make_account()
        ok, d = AccountManagementController.updateAccount(1, self._data(email='notanemail'))
        assert ok is False
        assert 'email' in d['error'].lower()

    @patch('app.services.account_management_controller.UserAccount.findById')
    def test_update_invalid_role(self, mock_find):
        """Invalid role should fail."""
        mock_find.return_value = make_account()
        ok, d = AccountManagementController.updateAccount(1, self._data(role='superuser'))
        assert ok is False
        assert 'role' in d['error'].lower()

    @patch('app.services.account_management_controller.UserAccount.updateAccount')
    @patch('app.services.account_management_controller.UserAccount.findById')
    def test_update_valid_role(self, mock_find, mock_update):
        """Valid role change should succeed."""
        mock_find.return_value = make_account(role='donee')
        ok, d = AccountManagementController.updateAccount(1, self._data(role='fund_raiser'))
        assert ok is True


# ══════════════════════════════════════════════════════════════
# UA-09 — SUSPEND USER ACCOUNT
# ══════════════════════════════════════════════════════════════

class TestSuspendAccount:

    @patch('app.services.account_management_controller.UserAccount.findById',
           return_value=None)
    def test_suspend_account_not_found(self, mock_find):
        """Returns fail if account does not exist."""
        ok, d = AccountManagementController.suspendAccount(999)
        assert ok is False
        assert 'error' in d

    @patch('app.services.account_management_controller.UserAccount.findById')
    def test_suspend_already_suspended(self, mock_find):
        """Returns fail if account already suspended."""
        mock_find.return_value = make_account(is_active=0)
        ok, d = AccountManagementController.suspendAccount(1)
        assert ok is False
        assert 'already' in d['error'].lower()

    @patch('app.services.account_management_controller.UserAccount.suspendAccount')
    @patch('app.services.account_management_controller.UserAccount.findById')
    def test_suspend_account_success(self, mock_find, mock_suspend):
        """Suspends account successfully."""
        mock_find.return_value = make_account(is_active=1)
        ok, d = AccountManagementController.suspendAccount(1)
        assert ok is True
        assert d['status'] == 'success'
        mock_suspend.assert_called_once_with(1)

    @patch('app.services.account_management_controller.UserAccount.suspendAccount')
    @patch('app.services.account_management_controller.UserAccount.findById')
    def test_cannot_suspend_admin(self, mock_find, mock_suspend):
        """Admin account cannot be suspended."""
        mock_find.return_value = make_account(role='admin')
        ok, d = AccountManagementController.suspendAccount(1)
        assert ok is False
        assert 'admin' in d['error'].lower()


# ══════════════════════════════════════════════════════════════
# UA-09 — ACTIVATE USER ACCOUNT (reactivate suspended)
# ══════════════════════════════════════════════════════════════

class TestActivateAccount:

    @patch('app.services.account_management_controller.UserAccount.findById',
           return_value=None)
    def test_activate_account_not_found(self, mock_find):
        """Returns fail if account does not exist."""
        ok, d = AccountManagementController.activateAccount(999)
        assert ok is False

    @patch('app.services.account_management_controller.UserAccount.findById')
    def test_activate_already_active(self, mock_find):
        """Returns fail if account already active."""
        mock_find.return_value = make_account(is_active=1)
        ok, d = AccountManagementController.activateAccount(1)
        assert ok is False
        assert 'already' in d['error'].lower()

    @patch('app.services.account_management_controller.UserAccount.activateAccount')
    @patch('app.services.account_management_controller.UserAccount.findById')
    def test_activate_account_success(self, mock_find, mock_activate):
        """Activates suspended account successfully."""
        mock_find.return_value = make_account(is_active=0)
        ok, d = AccountManagementController.activateAccount(1)
        assert ok is True
        assert d['status'] == 'success'
        mock_activate.assert_called_once_with(1)


# ══════════════════════════════════════════════════════════════
# UA-10 — SEARCH USER ACCOUNT
# ══════════════════════════════════════════════════════════════

class TestSearchAccount:

    @patch('app.services.account_management_controller.UserAccount.searchAccounts',
           return_value=[])
    def test_search_no_results(self, mock_search):
        """Returns fail when no accounts match."""
        ok, d = AccountManagementController.searchAccount({'username': 'nobody'})
        assert ok is False
        assert 'error' in d

    @patch('app.services.account_management_controller.UserAccount.searchAccounts')
    def test_search_by_username(self, mock_search):
        """Search by username returns matching accounts."""
        mock_search.return_value = [make_account(username='admin01')]
        ok, d = AccountManagementController.searchAccount({'username': 'admin01'})
        assert ok is True
        assert d['status'] == 'success'
        assert len(d['accounts']) == 1
        assert d['accounts'][0]['username'] == 'admin01'

    @patch('app.services.account_management_controller.UserAccount.searchAccounts')
    def test_search_by_role(self, mock_search):
        """Search by role returns matching accounts."""
        mock_search.return_value = [
            make_account(username='donee01', role='donee'),
            make_account(username='donee02', role='donee', user_id=2),
        ]
        ok, d = AccountManagementController.searchAccount({'role': 'donee'})
        assert ok is True
        assert len(d['accounts']) == 2

    @patch('app.services.account_management_controller.UserAccount.searchAccounts')
    def test_search_returns_no_passwords(self, mock_search):
        """Search results must never include password_hash."""
        mock_search.return_value = [make_account()]
        ok, d = AccountManagementController.searchAccount({'username': 'test'})
        assert ok is True
        for account in d['accounts']:
            assert 'password_hash' not in account


# ══════════════════════════════════════════════════════════════
# UA-04 — VIEW ALL ACCOUNTS
# ══════════════════════════════════════════════════════════════

class TestGetAllAccounts:

    @patch('app.services.account_management_controller.UserAccount.getAll',
           return_value=[])
    def test_get_all_empty(self, mock_get):
        """Returns success with empty list if no accounts."""
        ok, d = AccountManagementController.getAllAccounts()
        assert ok is True
        assert d['accounts'] == []

    @patch('app.services.account_management_controller.UserAccount.getAll')
    def test_get_all_returns_accounts(self, mock_get):
        """Returns all accounts successfully."""
        mock_get.return_value = [
            make_account(user_id=1, username='admin01', role='admin'),
            make_account(user_id=2, username='fr01', role='fund_raiser'),
            make_account(user_id=3, username='donee01', role='donee'),
        ]
        ok, d = AccountManagementController.getAllAccounts()
        assert ok is True
        assert d['status'] == 'success'
        assert len(d['accounts']) == 3

    @patch('app.services.account_management_controller.UserAccount.getAll')
    def test_get_all_no_passwords(self, mock_get):
        """Results must never include password_hash."""
        mock_get.return_value = [make_account()]
        ok, d = AccountManagementController.getAllAccounts()
        assert ok is True
        for account in d['accounts']:
            assert 'password_hash' not in account

    @patch('app.services.account_management_controller.UserAccount.getAll')
    def test_get_all_filter_by_role(self, mock_get):
        """Can filter accounts by role."""
        mock_get.return_value = [
            make_account(user_id=1, role='admin'),
            make_account(user_id=2, role='donee'),
        ]
        ok, d = AccountManagementController.getAllAccounts(role='admin')
        assert ok is True
        for account in d['accounts']:
            assert account['role'] == 'admin'
