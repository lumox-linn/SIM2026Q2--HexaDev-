"""
app/services/account_management_controller.py — Controller Layer
=================================================================
Sprint 2 — User Admin Account Management

REFACTORED:
- Validation moved to Boundary (account_management_routes.py)
- Alt flows moved to Entity (user_account.py)
- Controller ONLY calls Entity methods and returns results
"""
from app.models.user_account import UserAccount


def _safe_account(account: dict) -> dict:
    """Remove password_hash before returning to frontend."""
    return {k: v for k, v in account.items() if k != 'password_hash'}


class AccountManagementController:

    @staticmethod
    def viewAccount(user_id: int):
        """UA-07 — Call Entity, return result."""
        account = UserAccount.findById(user_id)
        if not account:
            return False, {'status': 'fail', 'error': f'Account with ID {user_id} not found.'}
        return True, {'status': 'success', 'account': _safe_account(account)}

    @staticmethod
    def getAllAccounts(role: str = None):
        """UA-07 — Get all accounts."""
        accounts = UserAccount.getAll(role=role)
        return True, {
            'status':   'success',
            'message':  f'{len(accounts)} account(s) found.',
            'accounts': [_safe_account(a) for a in accounts]
        }

    @staticmethod
    def updateAccount(user_id: int, data: dict):
        """UA-08 — Call Entity to update, return result."""
        result = UserAccount.updateIfExists(user_id, data)
        if not result:
            return False, {'status': 'fail', 'error': f'Account with ID {user_id} not found.'}
        return True, {
            'status':  'success',
            'message': f"Account updated successfully.",
            'user_id': user_id
        }

    @staticmethod
    def suspendAccount(user_id: int):
        """UA-09 — Call Entity to suspend, return result."""
        result = UserAccount.suspendIfAllowed(user_id)
        if result == 'not_found':
            return False, {'status': 'fail', 'error': f'Account with ID {user_id} not found.'}
        if result == 'already_suspended':
            return False, {'status': 'fail', 'error': 'Account is already suspended.'}
        if result == 'is_admin':
            return False, {'status': 'fail', 'error': 'Cannot suspend an admin account.'}
        return True, {
            'status':  'success',
            'message': 'Account has been suspended.',
            'user_id': user_id
        }

    @staticmethod
    def activateAccount(user_id: int):
        """UA-09 — Call Entity to activate, return result."""
        result = UserAccount.activateIfAllowed(user_id)
        if result == 'not_found':
            return False, {'status': 'fail', 'error': f'Account with ID {user_id} not found.'}
        if result == 'already_active':
            return False, {'status': 'fail', 'error': 'Account is already active.'}
        return True, {
            'status':  'success',
            'message': 'Account has been reactivated.',
            'user_id': user_id
        }

    @staticmethod
    def searchAccount(query: dict):
        """UA-10 — Call Entity to search, return result."""
        accounts = UserAccount.searchAccounts(query)
        if not accounts:
            return False, {'status': 'fail', 'error': 'No matching accounts found.'}
        return True, {
            'status':   'success',
            'message':  f'{len(accounts)} account(s) found.',
            'accounts': [_safe_account(a) for a in accounts]
        }

    @staticmethod
    def deleteAccount(user_id: int):
        """Delete account — call Entity."""
        result = UserAccount.deleteIfAllowed(user_id)
        if result == 'not_found':
            return False, {'status': 'fail', 'error': f'Account with ID {user_id} not found.'}
        if result == 'is_admin':
            return False, {'status': 'fail', 'error': 'Cannot delete an admin account.'}
        return True, {
            'status':  'success',
            'message': 'Account has been deleted.',
            'user_id': user_id
        }