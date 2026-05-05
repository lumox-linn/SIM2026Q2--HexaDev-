"""
app/services/auth_login_cotroller.py — Control Layer
=====================================================
Sprint 1 — UA-11, FR-06, DN-06, PM-09: Login

LoginController — calls Entity only, no validation.
"""
from app.models.user_account import UserAccount
from app.utils.auth_utils import generate_token

ROLE_LABELS = {
    'admin':            'User Admin',
    'fund_raiser':      'Fund Raiser',
    'donee':            'Donee',
    'platform_manager': 'Platform Manager',
}


class LoginController:
    """
    Control — LoginController (UA-11, FR-06, DN-06, PM-09)
    Only calls Entity methods — no validation, no alt flow logic.
    """

    @staticmethod
    def login(username: str, password: str):
        from app.utils.avatar_utils import get_avatar_url

        # [CONTROL] call Entity — alt flows handled inside Entity
        account = UserAccount.login(username, password)

        if not account:
            return False, {'status': 'fail', 'error': 'Invalid credentials or account suspended.'}

        token = generate_token(account['user_id'], account['role'])

        return True, {
            'status':     'success',
            'token':      token,
            'role':       account['role'],
            'role_label': ROLE_LABELS.get(account['role'], account['role']),
            'user_id':    account['user_id'],
            'username':   account['username'],
            'email':      account.get('email', None),
            'dob':        account.get('dob', None),
            'redirectTo': '/home',
            'avatar_url': get_avatar_url(account['role']),
        }


# Keep old name as alias for backward compatibility
AuthLoginCotroller = LoginController