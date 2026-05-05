"""
app/routes/account_management_routes.py — Boundary Layer
==========================================================
Sprint 2 — User Admin Account Management

Separate boundary class per use case:
- ViewAccountBoundary    (UA-07)
- UpdateAccountBoundary  (UA-08)
- SuspendAccountBoundary (UA-09)
- ActivateAccountBoundary (UA-09)
- SearchAccountBoundary  (UA-10)
- DeleteAccountBoundary
"""
from flask import Blueprint, request, jsonify
from app.services.account_management_controller import (
    ViewAccountController,
    UpdateAccountController,
    SuspendAccountController,
    ActivateAccountController,
    SearchAccountController,
    DeleteAccountController,
)
from app.utils.auth_utils import token_required

account_management_bp = Blueprint('account_management', __name__)

VALID_ROLES = ['admin', 'fund_raiser', 'donee', 'platform_manager']


class ViewAccountBoundary:
    """Boundary — ViewAccountBoundary (UA-07)"""

    @staticmethod
    @account_management_bp.route('/', methods=['GET'])
    @token_required(roles=['admin'])
    def get_all_accounts(current_user):
        username = request.args.get('username', '').strip()
        role     = request.args.get('role', '').strip()

        # If search params provided — delegate to search
        if username or role:
            query = {}
            if username: query['username'] = username
            if role:     query['role'] = role
            ok, payload = SearchAccountController.searchAccount(query)
            if ok:
                return jsonify(payload), 200
            return jsonify(payload), 404

        ok, payload = ViewAccountController.getAllAccounts()
        return jsonify(payload), 200

    @staticmethod
    @account_management_bp.route('/<int:user_id>', methods=['GET'])
    @token_required(roles=['admin'])
    def view_account(current_user, user_id):
        ok, payload = ViewAccountController.viewAccount(user_id)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404


class UpdateAccountBoundary:
    """Boundary — UpdateAccountBoundary (UA-08)"""

    @staticmethod
    @account_management_bp.route('/<int:user_id>', methods=['PUT'])
    @token_required(roles=['admin'])
    def update_account(current_user, user_id):
        data = request.get_json()

        # [BOUNDARY] Input validation
        if not data:
            return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400
        if data.get('email') and '@' not in str(data['email']):
            return jsonify({'status': 'fail', 'error': 'Invalid email format.'}), 400
        if data.get('role') and data['role'] not in VALID_ROLES:
            return jsonify({'status': 'fail', 'error': f'Invalid role. Must be one of: {", ".join(VALID_ROLES)}.'}), 400
        if data.get('password') and len(str(data['password'])) < 6:
            return jsonify({'status': 'fail', 'error': 'Password must be at least 6 characters.'}), 400

        ok, payload = UpdateAccountController.updateAccount(user_id, data)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400


class SuspendAccountBoundary:
    """Boundary — SuspendAccountBoundary (UA-09)"""

    @staticmethod
    @account_management_bp.route('/<int:user_id>/suspend', methods=['PUT'])
    @token_required(roles=['admin'])
    def suspend_account(current_user, user_id):
        ok, payload = SuspendAccountController.suspendAccount(user_id)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400


class ActivateAccountBoundary:
    """Boundary — ActivateAccountBoundary (UA-09)"""

    @staticmethod
    @account_management_bp.route('/<int:user_id>/activate', methods=['PUT'])
    @token_required(roles=['admin'])
    def activate_account(current_user, user_id):
        ok, payload = ActivateAccountController.activateAccount(user_id)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400


class SearchAccountBoundary:
    """Boundary — SearchAccountBoundary (UA-10)"""

    @staticmethod
    @account_management_bp.route('/search', methods=['GET'])
    @token_required(roles=['admin'])
    def search_accounts(current_user):
        username = request.args.get('username', '').strip()
        role     = request.args.get('role', '').strip()

        query = {}
        if username: query['username'] = username
        if role:     query['role'] = role

        ok, payload = SearchAccountController.searchAccount(query)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404


class DeleteAccountBoundary:
    """Boundary — DeleteAccountBoundary"""

    @staticmethod
    @account_management_bp.route('/<int:user_id>', methods=['DELETE'])
    @token_required(roles=['admin'])
    def delete_account(current_user, user_id):
        ok, payload = DeleteAccountController.deleteAccount(user_id)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400