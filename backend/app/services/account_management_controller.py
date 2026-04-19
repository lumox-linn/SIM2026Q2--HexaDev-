"""
app/services/account_management_controller.py — Controller Layer
=================================================================
Sprint 2 — User Admin Account Management

Handles business logic for:
  UA-07 — View user account
  UA-08 — Update user account
  UA-09 — Suspend user account (+ reactivate)
  UA-10 — Search user account
  UA-04 — View all accounts (get all)

RULES:
  - Only admin can call these (enforced by @token_required in routes)
  - Never return password_hash in any response
  - Admin cannot suspend another admin account
  - Cannot suspend already suspended account
  - Cannot activate already active account
"""
from app.models.user_account import UserAccount

VALID_ROLES = ['admin', 'fund_raiser', 'donee', 'platform_manager']


def _safe_account(account: dict) -> dict:
    """
    Remove password_hash from account dict before returning to frontend.
    NEVER expose password hash in API responses.
    """
    return {k: v for k, v in account.items() if k != 'password_hash'}


class AccountManagementController:

    # ── UA-07: View one account ───────────────────────────────

    @staticmethod
    def viewAccount(user_id: int):
        """
        View a single user account by user_id.

        Alt 1: Account not found → fail
        Main:  Return account data → success
        """
        # Alt 1: Account not found
        account = UserAccount.findById(user_id)
        if not account:
            return False, {
                'status': 'fail',
                'error':  f'Account with ID {user_id} not found.'
            }

        # Main flow: return account data
        return True, {
            'status':  'success',
            'account': _safe_account(account)
        }

    # ── UA-07: View all accounts ──────────────────────────────

    @staticmethod
    def getAllAccounts(role: str = None):
        """
        Get all user accounts.
        Optionally filter by role.

        Returns empty list if no accounts found — not an error.
        """
        accounts = UserAccount.getAll(role=role)

        # Filter by role if specified (extra safety in Python)
        if role:
            accounts = [a for a in accounts if a['role'] == role]

        return True, {
            'status':   'success',
            'message':  f'{len(accounts)} account(s) found.',
            'accounts': [_safe_account(a) for a in accounts]
        }

    # ── UA-08: Update account ─────────────────────────────────

    @staticmethod
    def validateUpdateInput(data: dict):
        """
        Validate update data.
        Returns (True, None) if valid.
        Returns (False, error_message) if invalid.
        """
        if 'email' in data and data['email']:
            if '@' not in data['email']:
                return False, 'Invalid email format.'

        if 'role' in data and data['role']:
            if data['role'] not in VALID_ROLES:
                return False, f'Invalid role. Must be one of: {", ".join(VALID_ROLES)}.'

        if 'password' in data and data['password']:
            if len(data['password']) < 6:
                return False, 'Password must be at least 6 characters.'

        if 'phone' in data and data['phone']:
            if not str(data['phone']).replace('+', '').replace('-', '').isdigit():
                return False, 'Invalid phone number format.'

        return True, None

    @staticmethod
    def updateAccount(user_id: int, data: dict):
        """
        Update a user account's details.

        Alt 1: Account not found → fail
        Alt 2: Invalid input → fail
        Main:  Update and return success
        """
        # Alt 1: Account not found
        account = UserAccount.findById(user_id)
        if not account:
            return False, {
                'status': 'fail',
                'error':  f'Account with ID {user_id} not found.'
            }

        # Alt 2: Validate input
        valid, error = AccountManagementController.validateUpdateInput(data)
        if not valid:
            return False, {'status': 'fail', 'error': error}

        # Main flow: update account
        UserAccount.updateAccount(user_id, data)

        return True, {
            'status':  'success',
            'message': f"Account '{account['username']}' updated successfully.",
            'user_id': user_id
        }

    # ── UA-09: Suspend account ────────────────────────────────

    @staticmethod
    def suspendAccount(user_id: int):
        """
        Suspend a user account (set isActive = 0).

        Alt 1: Account not found → fail
        Alt 2: Already suspended → fail
        Alt 3: Cannot suspend admin → fail
        Main:  Suspend and return success
        """
        # Alt 1: Account not found
        account = UserAccount.findById(user_id)
        if not account:
            return False, {
                'status': 'fail',
                'error':  f'Account with ID {user_id} not found.'
            }

        # Alt 2: Already suspended
        if account['isActive'] == 0:
            return False, {
                'status': 'fail',
                'error':  f"Account '{account['username']}' is already suspended."
            }

        # Alt 3: Cannot suspend admin
        if account['role'] == 'admin':
            return False, {
                'status': 'fail',
                'error':  'Cannot suspend an admin account.'
            }

        # Main flow: suspend
        UserAccount.suspendAccount(user_id)

        return True, {
            'status':  'success',
            'message': f"Account '{account['username']}' has been suspended.",
            'user_id': user_id
        }

    # ── UA-09: Activate account (reactivate) ──────────────────

    @staticmethod
    def activateAccount(user_id: int):
        """
        Reactivate a suspended account (set isActive = 1).

        Alt 1: Account not found → fail
        Alt 2: Already active → fail
        Main:  Activate and return success
        """
        # Alt 1: Account not found
        account = UserAccount.findById(user_id)
        if not account:
            return False, {
                'status': 'fail',
                'error':  f'Account with ID {user_id} not found.'
            }

        # Alt 2: Already active
        if account['isActive'] == 1:
            return False, {
                'status': 'fail',
                'error':  f"Account '{account['username']}' is already active."
            }

        # Main flow: activate
        UserAccount.activateAccount(user_id)

        return True, {
            'status':  'success',
            'message': f"Account '{account['username']}' has been reactivated.",
            'user_id': user_id
        }

    # ── UA-10: Search accounts ────────────────────────────────

    @staticmethod
    def searchAccount(query: dict):
        """
        Search accounts by username and/or role.

        Alt 1: No results found → fail
        Main:  Return matching accounts
        """
        # Main flow: search
        accounts = UserAccount.searchAccounts(query)

        # Alt 1: No results
        if not accounts:
            return False, {
                'status': 'fail',
                'error':  'No matching accounts found.'
            }

        return True, {
            'status':   'success',
            'message':  f'{len(accounts)} account(s) found.',
            'accounts': [_safe_account(a) for a in accounts]
        }
