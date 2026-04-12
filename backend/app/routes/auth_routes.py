from flask import Blueprint, request, jsonify
from app.services.auth_login_cotroller import AuthLoginCotroller
from app.services.auth_logout_cotroller import AuthLogoutCotroller
from app.services.account_controller import AccountController
from app.services.register_controller import RegisterController
from app.models.user_session import UserSession
from app.utils.auth_utils import token_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400

    success, payload = AuthLoginCotroller.login(
        data.get('username', ''),
        data.get('password', '')
    )
    if success:
        return jsonify(payload), 200
    return jsonify(payload), 401


@auth_bp.route('/logout', methods=['POST'])
def logout():
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else None

    session = UserSession.findByToken(token) if token else None
    if session:
        AuthLogoutCotroller.logout(str(session['user_id']))
    else:
        AuthLogoutCotroller.logoutByToken(token)

    return jsonify({'status': 'success', 'message': 'Logged out successfully.'}), 200


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400

    success, payload = RegisterController.registerUser(data)
    if success:
        return jsonify(payload), 201
    return jsonify(payload), 400


@auth_bp.route('/accounts', methods=['POST'])
@token_required(roles=['admin'])
def admin_create_account(current_user):
    data = request.get_json()
    if not data:
        return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400

    success, payload = AccountController.createUserAccount(data)
    if success:
        return jsonify(payload), 201
    return jsonify(payload), 400


@auth_bp.route('/me', methods=['GET'])
@token_required()
def me(current_user):
    return jsonify({'status': 'success', **current_user}), 200