"""
Sprint 2 Unit Tests — Account & Profile Management
Assigned to: Jiecheng
Run: pytest tests/test_account_management.py -v
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.account_management_controller import (
    ViewAccountController,
    UpdateAccountController,
    SuspendAccountController,
    ActivateAccountController,
    SearchAccountController,
)
from app.services.profile_management_controller import (
    CreateProfileController,
    ViewProfileController,
    UpdateProfileController,
    SuspendProfileController,
    SearchProfileController,
)


def make_account(user_id=1, username='testuser', role='donee', is_active=1,
                 email='test@test.com', phone='12345678', dob='2000-01-01'):
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
        'profile_id':      1,
        'profile_name':    role,
        'profile_status':  'active',
        'created_at':    '2026-01-01 00:00:00',
    }

def make_profile(profile_id=1, profile_name='donee', status='active'):
    return {
        'profile_id':   profile_id,
        'profile_name': profile_name,
        'status':       status,
        'description':  f'{profile_name} role',
        'created_at':   '2026-01-01 00:00:00',
    }


# ══════════════════════════════════════════════════════════════
# UA-07 — VIEW USER ACCOUNT — ViewAccountController
# ══════════════════════════════════════════════════════════════

class TestViewAccount:

    @patch('app.models.user_account.UserAccount.findById', return_value=None)
    def test_view_account_not_found(self, _):
        ok, d = ViewAccountController.viewAccount(999)
        assert ok is False and 'error' in d

    @patch('app.models.user_account.UserAccount.findById')
    def test_view_account_success(self, mock_find):
        mock_find.return_value = make_account()
        ok, d = ViewAccountController.viewAccount(1)
        assert ok is True and d['account']['username'] == 'testuser'

    @patch('app.models.user_account.UserAccount.findById')
    def test_view_account_returns_correct_fields(self, mock_find):
        mock_find.return_value = make_account(role='admin', email='admin@test.com')
        ok, d = ViewAccountController.viewAccount(1)
        assert ok is True
        account = d['account']
        for field in ['username', 'role', 'isActive', 'email', 'phone', 'dob']:
            assert field in account
        assert 'password_hash' not in account


# ══════════════════════════════════════════════════════════════
# UA-08 — UPDATE USER ACCOUNT — UpdateAccountController
# ══════════════════════════════════════════════════════════════

class TestUpdateAccount:

    def _data(self, **kwargs):
        base = {'email': 'new@test.com', 'phone': '99999999', 'dob': '2000-01-01'}
        base.update(kwargs)
        return base

    @patch('app.models.user_account.UserAccount.findById', return_value=None)
    def test_update_account_not_found(self, _):
        ok, d = UpdateAccountController.updateAccount(999, self._data())
        assert ok is False and 'error' in d

    @patch('app.models.user_account.UserAccount.findById')
    def test_update_account_success(self, mock_find):
        mock_find.return_value = make_account()
        ok, d = UpdateAccountController.updateAccount(1, self._data())
        assert ok is True and d['status'] == 'success'

    @patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None)
    @patch('app.utils.auth_utils.UserAccount.findById')
    def test_update_invalid_email(self, mock_find, _, client, admin_token):
        mock_find.return_value = make_account(role='admin')
        res = client.put('/api/accounts/1',
            json={'email': 'notanemail'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert res.status_code == 400
        assert 'email' in res.get_json()['error'].lower()

    @patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None)
    @patch('app.utils.auth_utils.UserAccount.findById')
    def test_update_invalid_role(self, mock_find, _, client, admin_token):
        mock_find.return_value = make_account(role='admin')
        res = client.put('/api/accounts/1',
            json={'role': 'superuser'},
            headers={'Authorization': f'Bearer {admin_token}'})
        assert res.status_code == 400
        assert 'role' in res.get_json()['error'].lower()

    @patch('app.models.user_account.UserAccount.findById')
    def test_update_valid_role(self, mock_find):
        mock_find.return_value = make_account(role='donee')
        ok, d = UpdateAccountController.updateAccount(1, self._data(role='fund_raiser'))
        assert ok is True


# ══════════════════════════════════════════════════════════════
# UA-09 — SUSPEND USER ACCOUNT — SuspendAccountController
# ══════════════════════════════════════════════════════════════

class TestSuspendAccount:

    @patch('app.models.user_account.UserAccount.findById', return_value=None)
    def test_suspend_account_not_found(self, _):
        ok, d = SuspendAccountController.suspendAccount(999)
        assert ok is False and 'error' in d

    @patch('app.models.user_account.UserAccount.findById')
    def test_suspend_already_suspended(self, mock_find):
        mock_find.return_value = make_account(is_active=0)
        ok, d = SuspendAccountController.suspendAccount(1)
        assert ok is False and 'already' in d['error'].lower()

    @patch('app.models.user_account.UserAccount.findById')
    def test_suspend_account_success(self, mock_find):
        mock_find.return_value = make_account(is_active=1)
        ok, d = SuspendAccountController.suspendAccount(1)
        assert ok is True and d['status'] == 'success'

    @patch('app.models.user_account.UserAccount.findById')
    def test_cannot_suspend_admin(self, mock_find):
        mock_find.return_value = make_account(role='admin')
        ok, d = SuspendAccountController.suspendAccount(1)
        assert ok is False and 'admin' in d['error'].lower()


# ══════════════════════════════════════════════════════════════
# UA-09 — ACTIVATE USER ACCOUNT — ActivateAccountController
# ══════════════════════════════════════════════════════════════

class TestActivateAccount:

    @patch('app.models.user_account.UserAccount.findById', return_value=None)
    def test_activate_account_not_found(self, _):
        ok, d = ActivateAccountController.activateAccount(999)
        assert ok is False

    @patch('app.models.user_account.UserAccount.findById')
    def test_activate_already_active(self, mock_find):
        mock_find.return_value = make_account(is_active=1)
        ok, d = ActivateAccountController.activateAccount(1)
        assert ok is False and 'already' in d['error'].lower()

    @patch('app.models.user_account.UserAccount.findById')
    def test_activate_account_success(self, mock_find):
        mock_find.return_value = make_account(is_active=0)
        ok, d = ActivateAccountController.activateAccount(1)
        assert ok is True and d['status'] == 'success'


# ══════════════════════════════════════════════════════════════
# UA-10 — SEARCH USER ACCOUNT — SearchAccountController
# ══════════════════════════════════════════════════════════════

class TestSearchAccount:

    @patch('app.models.user_account.UserAccount.search', return_value=[])
    def test_search_no_results(self, _):
        ok, d = SearchAccountController.searchAccount({'username': 'nobody'})
        assert ok is False and 'error' in d

    @patch('app.models.user_account.UserAccount.search')
    def test_search_by_username(self, mock_search):
        mock_search.return_value = [make_account(username='admin01')]
        ok, d = SearchAccountController.searchAccount({'username': 'admin01'})
        assert ok is True and len(d['accounts']) == 1

    @patch('app.models.user_account.UserAccount.search')
    def test_search_by_role(self, mock_search):
        mock_search.return_value = [
            make_account(username='donee01', role='donee'),
            make_account(username='donee02', role='donee', user_id=2),
        ]
        ok, d = SearchAccountController.searchAccount({'role': 'donee'})
        assert ok is True and len(d['accounts']) == 2

    @patch('app.models.user_account.UserAccount.search')
    def test_search_returns_no_passwords(self, mock_search):
        mock_search.return_value = [make_account()]
        ok, d = SearchAccountController.searchAccount({'username': 'test'})
        assert ok is True
        for account in d['accounts']:
            assert 'password_hash' not in account


# ══════════════════════════════════════════════════════════════
# GET ALL ACCOUNTS — ViewAccountController
# ══════════════════════════════════════════════════════════════

class TestGetAllAccounts:

    @patch('app.models.user_account.UserAccount.getAll', return_value=[])
    def test_get_all_empty(self, _):
        ok, d = ViewAccountController.getAllAccounts()
        assert ok is True and d['accounts'] == []

    @patch('app.models.user_account.UserAccount.getAll')
    def test_get_all_returns_accounts(self, mock_get):
        mock_get.return_value = [
            make_account(user_id=1, username='admin01', role='admin'),
            make_account(user_id=2, username='fr01', role='fund_raiser'),
        ]
        ok, d = ViewAccountController.getAllAccounts()
        assert ok is True and len(d['accounts']) == 2

    @patch('app.models.user_account.UserAccount.getAll')
    def test_get_all_no_passwords(self, mock_get):
        mock_get.return_value = [make_account()]
        ok, d = ViewAccountController.getAllAccounts()
        for account in d['accounts']:
            assert 'password_hash' not in account

    @patch('app.models.user_account.UserAccount.getAll')
    def test_get_all_filter_by_role(self, mock_get):
        mock_get.return_value = [make_account(user_id=1, role='admin')]
        ok, d = ViewAccountController.getAllAccounts(role='admin')
        assert ok is True
        mock_get.assert_called_once_with(role='admin')
        for account in d['accounts']:
            assert account['role'] == 'admin'


# ══════════════════════════════════════════════════════════════
# UA-01 — CREATE PROFILE — CreateProfileController
# ══════════════════════════════════════════════════════════════

class TestCreateProfile:

    def test_empty_name_fails(self):
        ok, d = CreateProfileController.createProfile({'profile_name': ''})
        assert ok is False and 'error' in d

    def test_short_name_fails(self):
        ok, d = CreateProfileController.createProfile({'profile_name': 'ab'})
        assert ok is False

    @patch('app.models.user_profile.UserProfile.exists', return_value=True)
    def test_duplicate_name_fails(self, _):
        ok, d = CreateProfileController.createProfile({'profile_name': 'donee'})
        assert ok is False and 'exists' in d['error'].lower()

    @patch('app.models.user_profile.UserProfile.exists', return_value=False)
    def test_create_success(self, _):
        ok, d = CreateProfileController.createProfile({
            'profile_name': 'moderator',
            'description':  'Moderates content'
        })
        assert ok is True and d['status'] == 'success'


# ══════════════════════════════════════════════════════════════
# UA-02 — VIEW PROFILE — ViewProfileController
# ══════════════════════════════════════════════════════════════

class TestViewProfile:

    @patch('app.models.user_profile.UserProfile.findById', return_value=None)
    def test_view_not_found(self, _):
        ok, d = ViewProfileController.viewProfile(999)
        assert ok is False

    @patch('app.models.user_profile.UserProfile.findById')
    def test_view_success(self, mock_find):
        mock_find.return_value = make_profile()
        ok, d = ViewProfileController.viewProfile(1)
        assert ok is True and d['profile']['profile_name'] == 'donee'


# ══════════════════════════════════════════════════════════════
# UA-03 — UPDATE PROFILE — UpdateProfileController
# ══════════════════════════════════════════════════════════════

class TestUpdateProfile:

    @patch('app.models.user_profile.UserProfile.findById', return_value=None)
    def test_update_not_found(self, _):
        ok, d = UpdateProfileController.updateProfile(999, {'description': 'test'})
        assert ok is False

    @patch('app.models.user_profile.UserProfile.findById')
    def test_update_success(self, mock_find):
        mock_find.return_value = make_profile()
        ok, d = UpdateProfileController.updateProfile(1, {'description': 'updated'})
        assert ok is True and d['status'] == 'success'


# ══════════════════════════════════════════════════════════════
# UA-04 — SUSPEND PROFILE — SuspendProfileController
# ══════════════════════════════════════════════════════════════

class TestSuspendProfile:

    @patch('app.models.user_profile.UserProfile.findById', return_value=None)
    def test_suspend_not_found(self, _):
        ok, d = SuspendProfileController.suspendProfile(999)
        assert ok is False

    @patch('app.models.user_profile.UserProfile.findById')
    def test_suspend_already_suspended(self, mock_find):
        mock_find.return_value = make_profile(status='suspended')
        ok, d = SuspendProfileController.suspendProfile(1)
        assert ok is False and 'already' in d['error'].lower()

    @patch('app.models.user_profile.UserProfile.findById')
    def test_cannot_suspend_admin(self, mock_find):
        mock_find.return_value = make_profile(profile_name='admin')
        ok, d = SuspendProfileController.suspendProfile(1)
        assert ok is False and 'cannot' in d['error'].lower()

    @patch('app.models.user_profile.UserProfile.findById')
    def test_suspend_success(self, mock_find):
        mock_find.return_value = make_profile(profile_name='donee')
        ok, d = SuspendProfileController.suspendProfile(1)
        assert ok is True and d['status'] == 'success'


# ══════════════════════════════════════════════════════════════
# UA-05 — SEARCH PROFILE — SearchProfileController
# ══════════════════════════════════════════════════════════════

class TestSearchProfile:

    @patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None)
    @patch('app.utils.auth_utils.UserAccount.findById')
    def test_empty_query_fails(self, mock_find, _, client, admin_token):
        mock_find.return_value = make_account(role='admin')
        res = client.get('/api/profiles/?query=',
            headers={'Authorization': f'Bearer {admin_token}'})
        assert res.status_code == 400

    @patch('app.models.user_profile.UserProfile.search', return_value=[])
    def test_no_results(self, _):
        ok, d = SearchProfileController.searchProfile('nobody')
        assert ok is False

    @patch('app.models.user_profile.UserProfile.search')
    def test_search_success(self, mock_search):
        mock_search.return_value = [make_profile(profile_name='donee')]
        ok, d = SearchProfileController.searchProfile('donee')
        assert ok is True and len(d['profiles']) == 1