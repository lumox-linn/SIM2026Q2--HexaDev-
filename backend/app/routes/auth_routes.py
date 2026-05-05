"""
app/routes/auth_routes.py — Boundary Layer
===========================================
Sprint 1 — Authentication

Separate boundary class per use case:
- LoginBoundary     (UA-11, FR-06, DN-06, PM-09)
- LogoutBoundary    (UA-12, FR-07, DN-07, PM-10)
- CreateAccountBoundary (UA-06)
"""
from flask import Blueprint, request, jsonify
from app.services.auth_login_cotroller import LoginController
from app.services.auth_logout_cotroller import LogoutController
from app.services.account_controller import CreateAccountController
from app.utils.auth_utils import token_required

auth_bp = Blueprint('auth', __name__)


class LoginBoundary:
    """
    Boundary — LoginBoundary (UA-11, FR-06, DN-06, PM-09)
    Validates login input, calls LoginController.
    """
    @staticmethod
    def login():
        data = request.get_json()

        # [BOUNDARY] Input validation
        if not data:
            return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400
        if not data.get('username') or not str(data['username']).strip():
            return jsonify({'status': 'fail', 'error': 'Username is required.'}), 400
        if not data.get('password') or not str(data['password']).strip():
            return jsonify({'status': 'fail', 'error': 'Password is required.'}), 400

        success, payload = LoginController.login(
            data['username'].strip(),
            data['password']
        )
        if success:
            return jsonify(payload), 200
        return jsonify(payload), 401


class LogoutBoundary:
    """
    Boundary — LogoutBoundary (UA-12, FR-07, DN-07, PM-10)
    JWT logout is stateless — just calls LogoutController.
    """
    @staticmethod
    def logout():
        LogoutController.logout()
        return jsonify({'status': 'success', 'message': 'Logged out successfully.'}), 200


class CreateAccountBoundary:
    """
    Boundary — CreateAccountBoundary (UA-06)
    Validates create account input, calls CreateAccountController.
    Admin only.
    """
    @staticmethod
    def create_account(current_user):
        data = request.get_json()

        # [BOUNDARY] Input validation
        if not data:
            return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400
        if not data.get('username') or not str(data['username']).strip():
            return jsonify({'status': 'fail', 'error': 'Username is required.'}), 400
        if len(str(data['username']).strip()) < 3:
            return jsonify({'status': 'fail', 'error': 'Username must be at least 3 characters.'}), 400
        if not data.get('password') or not str(data['password']).strip():
            return jsonify({'status': 'fail', 'error': 'Password is required.'}), 400
        if len(str(data['password'])) < 6:
            return jsonify({'status': 'fail', 'error': 'Password must be at least 6 characters.'}), 400
        if not data.get('role') or not str(data['role']).strip():
            return jsonify({'status': 'fail', 'error': 'Role is required.'}), 400

        valid_roles = ['admin', 'fund_raiser', 'donee', 'platform_manager']
        if data['role'] not in valid_roles:
            return jsonify({'status': 'fail', 'error': f'Invalid role. Must be one of: {", ".join(valid_roles)}.'}), 400

        success, payload = CreateAccountController.createAccount(data)
        if success:
            return jsonify(payload), 201
        return jsonify(payload), 400


# ── Route registration ────────────────────────────────────────

@auth_bp.route('/login', methods=['POST'])
def login():
    return LoginBoundary.login()


@auth_bp.route('/logout', methods=['POST'])
def logout():
    return LogoutBoundary.logout()


@auth_bp.route('/accounts', methods=['POST'])
@token_required(roles=['admin'])
def admin_create_account(current_user):
    return CreateAccountBoundary.create_account(current_user)


@auth_bp.route('/me', methods=['GET'])
@token_required()
def me(current_user):
    return jsonify({'status': 'success', **current_user}), 200