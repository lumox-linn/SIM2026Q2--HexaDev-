import jwt
import os
from functools import wraps
from flask import request, jsonify
from app.models.user_account import UserAccount

SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'hexadev-secret-key-2026')

ROLE_LABELS = {
    'admin':            'User Admin',
    'fund_raiser':      'Fund Raiser',
    'donee':            'Donee',
    'platform_manager': 'Platform Manager',
}


def generate_token(user_id: int, role: str) -> str:
    """Generate a JWT token containing user_id and role."""
    payload = {
        'user_id': user_id,
        'role':    role,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')


def decode_token(token: str):
    """
    Decode a JWT token.
    Returns payload dict if valid.
    Returns None if invalid or expired.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
    except jwt.InvalidTokenError:
        return None


def token_required(roles=None):
    """
    Decorator — protects routes with JWT authentication.
    Validates token from Authorization header.
    Optionally checks role.
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # [BOUNDARY] — validate token exists in header
            auth_header = request.headers.get('Authorization', '')
            if not auth_header.startswith('Bearer '):
                return jsonify({'status': 'fail', 'error': 'No token provided.'}), 401

            token = auth_header.split(' ')[1]
            payload = decode_token(token)

            if not payload:
                return jsonify({'status': 'fail', 'error': 'Invalid or expired token. Please log in again.'}), 401

            # Check role access
            if roles and payload.get('role') not in roles:
                return jsonify({'status': 'fail', 'error': 'Access denied.'}), 403

            # Get full user info from DB
            account = UserAccount.findById(payload['user_id'])
            if not account:
                return jsonify({'status': 'fail', 'error': 'Account not found.'}), 401

            # Check account is still active
            if not account['isActive']:
                return jsonify({'status': 'fail', 'error': 'Account is suspended.'}), 401

            from app.utils.avatar_utils import get_avatar_url
            profile_picture = UserAccount.getProfilePicture(account['user_id'])

            current_user = {
                'user_id':          account['user_id'],
                'username':         account['username'],
                'role':             account['role'],
                'role_label':       ROLE_LABELS.get(account['role'], account['role']),
                'email':            account.get('email', None),
                'dob':              account.get('dob', None),
                'avatar_url':       get_avatar_url(account['role'], profile_picture),
                'has_custom_avatar': profile_picture is not None,
            }

            return f(current_user=current_user, *args, **kwargs)
        return decorated
    return decorator