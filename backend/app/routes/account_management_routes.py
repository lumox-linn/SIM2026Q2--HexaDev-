"""
app/routes/account_management_routes.py — Boundary Layer
==========================================================
Sprint 2 — User Admin Account Management API endpoints

All endpoints are protected with @token_required(roles=['admin'])
Only logged-in admins can call these routes.

Endpoints:
  GET    /api/accounts              → get all accounts (UA-07)
  GET    /api/accounts?username=xx  → search by username (UA-10)
  GET    /api/accounts?role=admin   → filter by role (UA-05)
  GET    /api/accounts/<user_id>    → view one account (UA-07)
  PUT    /api/accounts/<user_id>    → update account (UA-08)
  PUT    /api/accounts/<user_id>/suspend  → suspend account (UA-09)
  PUT    /api/accounts/<user_id>/activate → activate account (UA-09)
"""
from flask import Blueprint, request, jsonify
from app.services.account_management_controller import AccountManagementController
from app.utils.auth_utils import token_required

account_management_bp = Blueprint('account_management', __name__)


@account_management_bp.route('/', methods=['GET'])
@token_required(roles=['admin'])
def get_all_accounts(current_user):
    """
    GET /api/accounts/
    GET /api/accounts/?username=admin01   ← search by username
    GET /api/accounts/?role=donee         ← filter by role
    GET /api/accounts/?username=xx&role=donee ← search + filter

    Returns all accounts or search results.
    Admin only.
    """
    username = request.args.get('username', '').strip()
    role     = request.args.get('role', '').strip()

    # If search query provided — search
    if username or role:
        query = {}
        if username:
            query['username'] = username
        if role:
            query['role'] = role
        ok, payload = AccountManagementController.searchAccount(query)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404

    # No query — return all accounts
    role_filter = role if role else None
    ok, payload = AccountManagementController.getAllAccounts(role=role_filter)
    return jsonify(payload), 200


@account_management_bp.route('/<int:user_id>', methods=['GET'])
@token_required(roles=['admin'])
def view_account(current_user, user_id):
    """
    GET /api/accounts/<user_id>

    View a single user account by ID.
    Admin only.

    Returns: { status, account: { user_id, username, role, isActive, email, phone, dob } }
    """
    ok, payload = AccountManagementController.viewAccount(user_id)
    if ok:
        return jsonify(payload), 200
    return jsonify(payload), 404


@account_management_bp.route('/<int:user_id>', methods=['PUT'])
@token_required(roles=['admin'])
def update_account(current_user, user_id):
    """
    PUT /api/accounts/<user_id>

    Update a user account's details.
    Admin only.

    Body (all fields optional):
    {
      "email":    "new@email.com",
      "phone":    "12345678",
      "dob":      "2000-01-01",
      "role":     "fund_raiser",
      "password": "newpass123"
    }

    Returns: { status, message, user_id }
    """
    data = request.get_json()
    if not data:
        return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400

    # [BOUNDARY] Input validation
    valid_roles = ['admin', 'fund_raiser', 'donee', 'platform_manager']
    if data.get('email') and '@' not in str(data['email']):
        return jsonify({'status': 'fail', 'error': 'Invalid email format.'}), 400
    if data.get('role') and data['role'] not in valid_roles:
        return jsonify({'status': 'fail', 'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}.'}), 400
    if data.get('password') and len(str(data['password'])) < 6:
        return jsonify({'status': 'fail', 'error': 'Password must be at least 6 characters.'}), 400

    ok, payload = AccountManagementController.updateAccount(user_id, data)
    if ok:
        return jsonify(payload), 200
    return jsonify(payload), 400


@account_management_bp.route('/<int:user_id>/suspend', methods=['PUT'])
@token_required(roles=['admin'])
def suspend_account(current_user, user_id):
    """
    PUT /api/accounts/<user_id>/suspend

    Suspend a user account (set isActive = 0).
    Admin only.
    Cannot suspend another admin.
    Cannot suspend already suspended account.

    Returns: { status, message, user_id }
    """
    ok, payload = AccountManagementController.suspendAccount(user_id)
    if ok:
        return jsonify(payload), 200
    return jsonify(payload), 400


@account_management_bp.route('/<int:user_id>/activate', methods=['PUT'])
@token_required(roles=['admin'])
def activate_account(current_user, user_id):
    """
    PUT /api/accounts/<user_id>/activate

    Reactivate a suspended account (set isActive = 1).
    Admin only.

    Returns: { status, message, user_id }
    """
    ok, payload = AccountManagementController.activateAccount(user_id)
    if ok:
        return jsonify(payload), 200
    return jsonify(payload), 400


@account_management_bp.route('/<int:user_id>', methods=['DELETE'])
@token_required(roles=['admin'])
def delete_account(current_user, user_id):
    """
    DELETE /api/accounts/<user_id>
    Permanently delete a user account.
    Cannot delete admin accounts.
    Admin only.
    """
    ok, payload = AccountManagementController.deleteAccount(user_id)
    if ok:
        return jsonify(payload), 200
    return jsonify(payload), 400