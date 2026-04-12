from app.models.user_account import UserAccount

ADMIN_ONLY_ROLES = ['admin', 'platform_manager']
VALID_ROLES = ['admin', 'fund_raiser', 'donee', 'platform_manager']


class AccountController:
    """
    Control — AccountController <controller> from BCE diagram (UA-03).
    Admin creates accounts for any role.
    """

    @staticmethod
    def validateInput(data: dict):
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        role     = data.get('role', '').strip()

        if not username:
            return False, 'Username is required.'
        if len(username) < 3:
            return False, 'Username must be at least 3 characters.'
        if not password:
            return False, 'Password is required.'
        if len(password) < 6:
            return False, 'Password must be at least 6 characters.'
        if not role:
            return False, 'Role is required.'
        if role not in VALID_ROLES:
            return False, f'Invalid role. Must be one of: {", ".join(VALID_ROLES)}.'

        return True, None

    @staticmethod
    def createUserAccount(data: dict):
        valid, error = AccountController.validateInput(data)
        if not valid:
            return False, {'status': 'fail', 'error': error}

        if UserAccount.exists(data['username'].strip()):
            return False, {'status': 'fail', 'error': 'Username already exists. Please choose another.'}

        UserAccount.createAccount({
            'username': data['username'].strip(),
            'password': data['password'],
            'email':    data.get('email', None),
            'role':     data['role'].strip(),
            'isActive': 1,
        })

        return True, {
            'status':   'success',
            'message':  f"Account created successfully for {data['username'].strip()}.",
            'username': data['username'].strip(),
            'role':     data['role'].strip(),
        }