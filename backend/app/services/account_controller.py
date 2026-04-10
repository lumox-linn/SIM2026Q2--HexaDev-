from app.models.user_account import UserAccount

# Roles that only admin can create
ADMIN_ONLY_ROLES = ['admin', 'platform_manager']

# All valid roles
VALID_ROLES = ['admin', 'fund_raiser', 'donee', 'platform_manager']


class AccountController:
    """
    Control — AccountController <controller> from BCE diagram (UA-03).
    Method: createUserAccount(data)
    Called only by authenticated User Admin.
    Can create accounts for ALL roles including admin and platform_manager.
    """

    @staticmethod
    def validateInput(data: dict):
        """
        Validate required fields are present and non-empty.
        Returns (True, None) or (False, error_message)
        """
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
        """
        Main flow from sequence diagram:
          1. validateInput()
          2. [invalid] → return error
          3. [valid]   → exists(username)
          4. [exists]  → return error
          5. [unique]  → createAccount(data) → showSuccessMessage

        Returns (success: bool, payload: dict)
        """
        # Step 1: validate input
        valid, error = AccountController.validateInput(data)
        if not valid:
            return False, {'error': error}

        # Step 2: check username exists
        if UserAccount.exists(data['username'].strip()):
            return False, {'error': 'Username already exists. Please choose another.'}

        # Step 3: create account
        UserAccount.createAccount({
            'username': data['username'].strip(),
            'password': data['password'],
            'role':     data['role'].strip(),
            'isActive': 1,
        })

        return True, {
            'message':  f"Account created successfully for {data['username'].strip()}.",
            'username': data['username'].strip(),
            'role':     data['role'].strip(),
        }
