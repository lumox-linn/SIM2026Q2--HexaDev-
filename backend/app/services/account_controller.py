"""
app/services/account_controller.py — Control Layer
====================================================
Sprint 1 — UA-06: Admin Create Account

CreateAccountController — calls Entity only, no validation.
"""
from app.models.user_account import UserAccount


class CreateAccountController:
    """
    Control — CreateAccountController (UA-06)
    Only calls Entity methods — no validation, no alt flow logic.
    Validation is in Boundary (CreateAccountBoundary).
    Alt flows are in Entity (UserAccount.create()).
    """

    @staticmethod
    def createAccount(data: dict):
        # [CONTROL] call Entity — alt flows handled inside Entity
        result = UserAccount.create({
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


# Keep old name as alias for backward compatibility
AccountController = CreateAccountController