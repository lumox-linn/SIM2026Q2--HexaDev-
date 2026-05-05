"""
app/services/account_management_controller.py — Control Layer
=================================================================
Sprint 2 — User Admin Account Management

Separate controller class per use case:
- ViewAccountController    (UA-07)
- UpdateAccountController  (UA-08)
- SuspendAccountController (UA-09)
- ActivateAccountController (UA-09)
- SearchAccountController  (UA-10)
- DeleteAccountController
"""
from app.models.user_account import UserAccount


def _safe(account: dict) -> dict:
    """Remove password_hash before returning to frontend."""
    return {k: v for k, v in account.items() if k != 'password_hash'}


class ViewAccountController:
    """Control — ViewAccountController (UA-07)"""

    @staticmethod
    def getAllAccounts():
        accounts = UserAccount.getAll()
        return True, {
            'status':   'success',
            'message':  f'{len(accounts)} account(s) found.',
            'accounts': [_safe(a) for a in accounts]
        }

    @staticmethod
    def viewAccount(user_id: int):
        account = UserAccount.findById(user_id)
        if not account:
            return False, {'status': 'fail', 'error': f'Account with ID {user_id} not found.'}
        return True, {'status': 'success', 'account': _safe(account)}


class UpdateAccountController:
    """Control — UpdateAccountController (UA-08)"""

    @staticmethod
    def updateAccount(user_id: int, data: dict):
        result = UserAccount.update(user_id, data)
        if not result:
            return False, {'status': 'fail', 'error': f'Account with ID {user_id} not found.'}
        return True, {
            'status':  'success',
            'message': 'Account updated successfully.',
            'user_id': user_id
        }


class SuspendAccountController:
    """Control — SuspendAccountController (UA-09)"""

    @staticmethod
    def suspendAccount(user_id: int):
        result = UserAccount.suspend(user_id)
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


class ActivateAccountController:
    """Control — ActivateAccountController (UA-09)"""

    @staticmethod
    def activateAccount(user_id: int):
        result = UserAccount.activate(user_id)
        if result == 'not_found':
            return False, {'status': 'fail', 'error': f'Account with ID {user_id} not found.'}
        if result == 'already_active':
            return False, {'status': 'fail', 'error': 'Account is already active.'}
        return True, {
            'status':  'success',
            'message': 'Account has been reactivated.',
            'user_id': user_id
        }


class SearchAccountController:
    """Control — SearchAccountController (UA-10)"""

    @staticmethod
    def searchAccount(query: dict):
        accounts = UserAccount.search(query)
        if not accounts:
            return False, {'status': 'fail', 'error': 'No matching accounts found.'}
        return True, {
            'status':   'success',
            'message':  f'{len(accounts)} account(s) found.',
            'accounts': [_safe(a) for a in accounts]
        }


class DeleteAccountController:
    """Control — DeleteAccountController"""

    @staticmethod
    def deleteAccount(user_id: int):
        result = UserAccount.delete(user_id)
        if result == 'not_found':
            return False, {'status': 'fail', 'error': f'Account with ID {user_id} not found.'}
        if result == 'is_admin':
            return False, {'status': 'fail', 'error': 'Cannot delete an admin account.'}
        return True, {
            'status':  'success',
            'message': 'Account has been deleted.',
            'user_id': user_id
        }


# Keep old name as alias for backward compatibility
class AccountManagementController:
    viewAccount    = ViewAccountController.viewAccount
    getAllAccounts  = ViewAccountController.getAllAccounts
    updateAccount  = UpdateAccountController.updateAccount
    suspendAccount = SuspendAccountController.suspendAccount
    activateAccount= ActivateAccountController.activateAccount
    searchAccount  = SearchAccountController.searchAccount
    deleteAccount  = DeleteAccountController.deleteAccount