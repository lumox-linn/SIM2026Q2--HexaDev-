from app.models.user_account import UserAccount


class RegisterController:
    """
    Control — RegisterController <controller> from BCE diagram (GU-03).
    Public registration — anyone can register.
    Role defaults to 'donee' automatically.
    User can upgrade to Fund Raiser from dashboard later.
    """

    @staticmethod
    def validateInput(data: dict):
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        email    = data.get('email', '').strip()

        if not username:
            return False, 'Username is required.'
        if len(username) < 3:
            return False, 'Username must be at least 3 characters.'
        if not password:
            return False, 'Password is required.'
        if len(password) < 6:
            return False, 'Password must be at least 6 characters.'
        if not email:
            return False, 'Email is required.'
        if '@' not in email:
            return False, 'Please enter a valid email address.'

        return True, None

    @staticmethod
    def registerUser(data: dict):
        """
        Register a new user.
        Role is always 'donee' by default — no role selection needed.
        User can switch to fund_raiser later from dashboard.
        """
        valid, error = RegisterController.validateInput(data)
        if not valid:
            return False, {'status': 'fail', 'error': error}

        # Check duplicate username
        if UserAccount.exists(data['username'].strip()):
            return False, {'status': 'fail', 'error': 'Username already exists. Please choose another.'}

        # Create account — role is always donee, not chosen by user
        UserAccount.createAccount({
            'username': data['username'].strip(),
            'password': data['password'],
            'email':    data.get('email', '').strip(),
            'role':     'donee',
            'isActive': 1,
        })

        return True, {
            'status':  'success',
            'message': 'Account created successfully. You may now log in.',
            'username': data['username'].strip(),
        }