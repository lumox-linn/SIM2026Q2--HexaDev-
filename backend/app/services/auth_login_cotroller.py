from app.models.user_account import UserAccount
from app.utils.auth_utils import generate_token

ROLE_LABELS = {
    'admin':            'User Admin',
    'fund_raiser':      'Fund Raiser',
    'donee':            'Donee',
    'platform_manager': 'Platform Manager',
}


class AuthLoginCotroller:
    """
    Control — AuthLoginCotroller.
    Only calls Entity methods — no validation, no alt flow logic.
    Validation is in Boundary (auth_routes.py).
    Alt flows are in Entity (user_account.py).
    """

    @staticmethod
    def login(username: str, password: str):
        """
        Calls UserAccount.login() which handles all alt flows.
        Returns (success, payload).
        """
        from app.utils.avatar_utils import get_avatar_url

        # [CONTROL] — call Entity, handle result
        account = UserAccount.login(username, password)

        if not account:
            return False, {'status': 'fail', 'error': 'Invalid credentials or account suspended.'}

        # Generate JWT token
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