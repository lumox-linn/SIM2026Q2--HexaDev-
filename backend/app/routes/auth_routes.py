from flask import Blueprint, request, jsonify
from app.services.auth_login_cotroller import AuthLoginCotroller
from app.services.auth_logout_cotroller import AuthLogoutCotroller
from app.services.account_controller import AccountController
from app.services.register_controller import RegisterController
from app.models.user_session import UserSession
from app.utils.auth_utils import token_required

auth_bp = Blueprint('auth', __name__)


# ══════════════════════════════════════════════════════════════
# LOGIN  —  POST /api/auth/login
# All roles: admin, fund_raiser, donee, platform_manager
# ══════════════════════════════════════════════════════════════

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    POST /api/auth/login
    Body: { "username": "...", "password": "..." }

    On success returns:
    {
      "token":      "<64-char hex>",
      "role":       "admin" | "fund_raiser" | "donee" | "platform_manager",
      "role_label": "User Admin" | "Fund Raiser" | "Donee" | "Platform Manager",
      "user_id":    1,
      "redirectTo": "/admin/dashboard" | "/fr/dashboard" | "/donee/dashboard" | "/pm/dashboard"
    }

    The frontend uses `redirectTo` to navigate to the correct dashboard per role.
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    success, payload = AuthLoginCotroller.login(
        data.get('username', ''),
        data.get('password', '')
    )

    if success:
        return jsonify(payload), 200
    return jsonify(payload), 401


# ══════════════════════════════════════════════════════════════
# LOGOUT  —  POST /api/auth/logout
# ══════════════════════════════════════════════════════════════

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    POST /api/auth/logout
    Header: Authorization: Bearer <token>
    Expires the session in usersession table.
    Safe to call even if session is already expired.
    """
    auth_header = request.headers.get('Authorization', '')
    token = auth_header.split(' ')[1] if auth_header.startswith('Bearer ') else None

    session = UserSession.findByToken(token) if token else None
    if session:
        # Active session — call UserAccount.logout(accountId)
        AuthLogoutCotroller.logout(str(session['user_id']))
    else:
        # Already expired — expire by token just in case
        AuthLogoutCotroller.logoutByToken(token)

    return jsonify({'message': 'Logged out successfully.'}), 200


# ══════════════════════════════════════════════════════════════
# SELF-REGISTER  —  POST /api/auth/register  (GU-03)
# Public — no auth required
# Allowed roles: fund_raiser, donee ONLY
# ══════════════════════════════════════════════════════════════

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    POST /api/auth/register
    Body: { "username": "...", "password": "...", "role": "fund_raiser" | "donee" }

    Public endpoint — anyone can call this.
    Security: RegisterController.validateRole() blocks admin/platform_manager.
    On success: returns { message, username, role }
    On failure: returns { error }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    success, payload = RegisterController.registerUser(data)

    if success:
        return jsonify(payload), 201
    return jsonify(payload), 400


# ══════════════════════════════════════════════════════════════
# ADMIN CREATE ACCOUNT  —  POST /api/auth/accounts  (UA-03)
# Protected — requires Bearer token + admin role
# Can create any role including admin, platform_manager
# ══════════════════════════════════════════════════════════════

@auth_bp.route('/accounts', methods=['POST'])
@token_required(roles=['admin'])
def admin_create_account(current_user):
    """
    POST /api/auth/accounts
    Header: Authorization: Bearer <admin token>
    Body: { "username": "...", "password": "...", "role": "admin"|"fund_raiser"|"donee"|"platform_manager" }

    Protected — only admin role can call this.
    Can create accounts for any role.
    On success: returns { message, username, role }
    On failure: returns { error }
    """
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Request body must be JSON.'}), 400

    success, payload = AccountController.createUserAccount(data)

    if success:
        return jsonify(payload), 201
    return jsonify(payload), 400


# ══════════════════════════════════════════════════════════════
# GET CURRENT USER  —  GET /api/auth/me
# ══════════════════════════════════════════════════════════════

@auth_bp.route('/me', methods=['GET'])
@token_required()
def me(current_user):
    """
    GET /api/auth/me
    Header: Authorization: Bearer <token>
    Returns current user info: { user_id, username, role, role_label }
    """
    return jsonify(current_user), 200
