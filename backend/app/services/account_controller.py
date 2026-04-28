from app.models.user_account import UserAccount


class AccountController:
    """
    Control — AccountController (UA-06).
    Only calls Entity methods — no validation logic.
    Validation is in Boundary (auth_routes.py).
    Alt flows are in Entity (user_account.py).
    """

    @staticmethod
    def createUserAccount(data: dict):
        """
        Admin creates a new user account.
        Calls UserAccount.createIfNotExists() which handles alt flows.
        """
        # [CONTROL] — call Entity, handle result
        result = UserAccount.createIfNotExists({
            'username': data['username'].strip(),
            'password': data['password'],
            'email':    data.get('email', None),
            'phone':    data.get('phone', None),
            'role':     data['role'].strip(),
            'dob':      data.get('dob', None),
            'isActive': 1,
        })

        if not result:
            return False, {'status': 'fail', 'error': 'Username already exists. Please choose another.'}

        return True, {
            'status':   'success',
            'message':  f"Account created successfully for {data['username'].strip()}.",
            'username': data['username'].strip(),
            'role':     data['role'].strip(),
        }