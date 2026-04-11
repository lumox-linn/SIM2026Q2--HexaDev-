from functools import wraps
from flask import request, jsonify
from app.models.user_session import UserSession
from app.models.user_account import UserAccount

ROLE_LABELS = {
    'admin':            'User Admin',
    'fund_raiser':      'Fund Raiser',
    'donee':            'Donee',
    'platform_manager': 'Platform Manager',
}


def get_current_user(token: str):
    """
    Validate token and return full user info including avatar_url.
    avatar_url priority:
      1. User has uploaded a profile picture → uploaded image URL
      2. No upload → default role avatar URL
    """
    from app.utils.avatar_utils import get_avatar_url

    if not token or not UserSession.isValid(token):
        return None

    session = UserSession.findByToken(token)
    if not session:
        return None

    account = UserAccount.findById(session['user_id'])
    if not account:
        return None

    # Get uploaded picture filename from DB (may be None)
    profile_picture = UserAccount.getProfilePicture(account['user_id'])

    return {
        'user_id':         account['user_id'],
        'username':        account['username'],
        'role':            account['role'],
        'role_label':      ROLE_LABELS.get(account['role'], account['role']),
        'avatar_url':      get_avatar_url(account['role'], profile_picture),
        'has_custom_avatar': profile_picture is not None,
    }


def token_required(roles=None):
    """
    Decorator to protect API routes.
    Reads: Authorization: Bearer <token>
    Injects current_user into the route function.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return jsonify({'error': 'No token provided.'}), 401

            token = auth_header.split(' ')[1]
            user = get_current_user(token)

            if not user:
                return jsonify({'error': 'Invalid or expired session. Please log in again.'}), 401

            if roles and user['role'] not in roles:
                return jsonify({'error': 'Access denied.'}), 403

            return f(current_user=user, *args, **kwargs)
        return decorated
    return decorator
