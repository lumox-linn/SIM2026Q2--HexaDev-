from flask import Blueprint, request, jsonify
from app.services.auth_login_cotroller import AuthLoginCotroller
from app.services.auth_logout_cotroller import AuthLogoutCotroller
from app.services.account_controller import AccountController
from app.utils.auth_utils import token_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    POST /api/auth/login
    BOUNDARY — validates input, calls controller.
    """
    data = request.get_json()

    # [BOUNDARY] Input validation
    if not data:
        return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400
    if not data.get('username') or not str(data['username']).strip():
        return jsonify({'status': 'fail', 'error': 'Username is required.'}), 400
    if not data.get('password') or not str(data['password']).strip():
        return jsonify({'status': 'fail', 'error': 'Password is required.'}), 400

    success, payload = AuthLoginCotroller.login(
        data['username'].strip(),
        data['password']
    )
    if success:
        return jsonify(payload), 200
    return jsonify(payload), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    POST /api/auth/logout
    BOUNDARY — JWT logout is stateless, just return success.
    Frontend clears token from localStorage.
    """
    # [BOUNDARY] No DB operation needed — JWT is stateless
    AuthLogoutCotroller.logout()
    return jsonify({'status': 'success', 'message': 'Logged out successfully.'}), 200




@auth_bp.route('/accounts', methods=['POST'])
@token_required(roles=['admin'])
def admin_create_account(current_user):
    """
    POST /api/auth/accounts
    BOUNDARY — validates input, calls controller.
    Admin only.
    """
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

    success, payload = AccountController.createUserAccount(data)
    if success:
        return jsonify(payload), 201
    return jsonify(payload), 400


@auth_bp.route('/me', methods=['GET'])
@token_required()
def me(current_user):
    """GET /api/auth/me — return current user info from JWT."""
    return jsonify({'status': 'success', **current_user}), 200