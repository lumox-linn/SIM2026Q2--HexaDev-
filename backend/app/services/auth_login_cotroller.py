from app.models.user_account import UserAccount
from app.models.user_session import UserSession

ROLE_ROUTES = {
    'admin':            '/admin/dashboard',
    'fund_raiser':      '/fr/dashboard',
    'donee':            '/donee/dashboard',
    'platform_manager': '/pm/dashboard',
}

ROLE_LABELS = {
    'admin':            'User Admin',
    'fund_raiser':      'Fund Raiser',
    'donee':            'Donee',
    'platform_manager': 'Platform Manager',
}


class AuthLoginCotroller:
    """
    Control — AuthLoginCotroller <controller> from BCE diagram.
    Method: login(username: String, password: String)
    Implements 4-alt flow from sequence diagram.
    Returns avatar_url so frontend can display profile picture immediately.
    """

    @staticmethod
    def login(username: str, password: str):
        """
        Returns (success: bool, payload: dict)
        Success: { token, role, role_label, user_id, redirectTo, avatar_url }
        Failure: { error }
        """
        # Import here to avoid circular import
        from app.utils.avatar_utils import get_avatar_url

        # Input validation
        if not username or not username.strip():
            return False, {'error': 'Username is required.'}
        if not password or not password.strip():
            return False, {'error': 'Password is required.'}

        # alt 1: Account not found
        account = UserAccount.findByUsername(username.strip())
        if not account:
            return False, {'error': 'Invalid credentials entered.'}

        # alt 2: Password incorrect
        if not UserAccount.verifyPassword(password, account['password_hash']):
            return False, {'error': 'Invalid credentials entered.'}

        # alt 3: Account not active (isActive = 0)
        if not UserAccount.isActive(account):
            return False, {'error': 'Account is suspended or inactive. Contact the administrator.'}

        # alt 4: Wrong role
        valid_roles = list(ROLE_ROUTES.keys())
        if not UserAccount.hasRole(account, account['role']) or account['role'] not in valid_roles:
            return False, {'error': 'Access denied.'}

        # All checks passed — create session
        token = UserSession.create(account['user_id'])

        return True, {
            'token':      token,
            'role':       account['role'],
            'role_label': ROLE_LABELS.get(account['role'], account['role']),
            'user_id':    account['user_id'],
            'redirectTo': ROLE_ROUTES.get(account['role'], '/login'),
            'avatar_url': get_avatar_url(account['role']),
        }
