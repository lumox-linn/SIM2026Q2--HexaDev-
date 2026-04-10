from app.models.user_account import UserAccount

# Roles allowed for self-registration (public)
PUBLIC_ROLES = ['fund_raiser', 'donee']


class RegisterController:
    """
    Control — RegisterController <controller> from BCE diagram (GU-03).
    Method: registerUser(data)
    Public endpoint — no auth required.
    Security: only fund_raiser and donee roles allowed.
    """

    @staticmethod
    def validateInput(data: dict):
        """
        Validate required fields.
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

        return True, None

    @staticmethod
    def validateRole(role: str):
        """
        Security check — block privileged role registration.
        Maps to validateRole(role) in sequence diagram.
        Returns (True, None) or (False, error_message)
        """
        if role not in PUBLIC_ROLES:
            return False, 'Invalid role for self-registration. You may only register as a Fund Raiser or Donee.'
        return True, None

    @staticmethod
    def registerUser(data: dict):
        """
        Main flow from sequence diagram:
          1. validateInput()
          2. [invalid]        → return error
          3. [valid]          → validateRole(role)   ← SECURITY CHECK
          4. [invalid role]   → return error
          5. [valid role]     → exists(username)
          6. [exists]         → return error
          7. [unique account] → createAccount(data) → showSuccessMessage

        Returns (success: bool, payload: dict)
        """
        # Step 1: validate input fields
        valid, error = RegisterController.validateInput(data)
        if not valid:
            return False, {'error': error}

        # Step 2: validate role — security check
        role_ok, role_error = RegisterController.validateRole(data.get('role', '').strip())
        if not role_ok:
            return False, {'error': role_error}

        # Step 3: check username already exists
        if UserAccount.exists(data['username'].strip()):
            return False, {'error': 'Username already exists. Please choose another.'}

        # Step 4: create account
        UserAccount.createAccount({
            'username': data['username'].strip(),
            'password': data['password'],
            'role':     data['role'].strip(),
            'isActive': 1,
        })

        return True, {
            'message':  f"Account created successfully. You may now log in.",
            'username': data['username'].strip(),
            'role':     data['role'].strip(),
        }
