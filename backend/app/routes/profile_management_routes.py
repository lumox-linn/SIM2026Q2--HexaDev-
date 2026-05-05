"""
app/routes/profile_management_routes.py — Boundary Layer
==========================================================
Sprint 2 — User Admin Profile Management

Separate boundary class per use case:
- CreateProfileBoundary  (UA-01)
- ViewProfileBoundary    (UA-02)
- UpdateProfileBoundary  (UA-03)
- SuspendProfileBoundary (UA-04)
- ActivateProfileBoundary (UA-04)
- SearchProfileBoundary  (UA-05)
"""
from flask import Blueprint, request, jsonify
from app.services.profile_management_controller import (
    CreateProfileController,
    ViewProfileController,
    UpdateProfileController,
    SuspendProfileController,
    ActivateProfileController,
    SearchProfileController,
)
from app.utils.auth_utils import token_required

profile_management_bp = Blueprint('profile_management', __name__)


class CreateProfileBoundary:
    """Boundary — CreateProfileBoundary (UA-01)"""

    @staticmethod
    @profile_management_bp.route('/', methods=['POST'])
    @token_required(roles=['admin'])
    def create_profile(current_user):
        data = request.get_json()

        # [BOUNDARY] Input validation
        if not data:
            return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400
        if not data.get('profile_name') or not str(data['profile_name']).strip():
            return jsonify({'status': 'fail', 'error': 'Profile name is required.'}), 400
        if len(str(data['profile_name']).strip()) < 2:
            return jsonify({'status': 'fail', 'error': 'Profile name must be at least 2 characters.'}), 400

        ok, payload = CreateProfileController.createProfile(data)
        if ok:
            return jsonify(payload), 201
        return jsonify(payload), 400


class ViewProfileBoundary:
    """Boundary — ViewProfileBoundary (UA-02)"""

    @staticmethod
    @profile_management_bp.route('/', methods=['GET'])
    @token_required(roles=['admin'])
    def get_all_profiles(current_user):
        query = request.args.get('query', '').strip()

        # [BOUNDARY] Validate empty query
        if 'query' in request.args and query == '':
            return jsonify({'status': 'fail', 'error': 'Search query cannot be empty.'}), 400

        if query:
            return SearchProfileBoundary._search(query)

        ok, payload = ViewProfileController.getAllProfiles()
        return jsonify(payload), 200

    @staticmethod
    @profile_management_bp.route('/<int:profile_id>', methods=['GET'])
    @token_required(roles=['admin'])
    def view_profile(current_user, profile_id):
        ok, payload = ViewProfileController.viewProfile(profile_id)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404


class UpdateProfileBoundary:
    """Boundary — UpdateProfileBoundary (UA-03)"""

    @staticmethod
    @profile_management_bp.route('/<int:profile_id>', methods=['PUT'])
    @token_required(roles=['admin'])
    def update_profile(current_user, profile_id):
        data = request.get_json()

        # [BOUNDARY] Input validation
        if not data:
            return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400

        ok, payload = UpdateProfileController.updateProfile(profile_id, data)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400


class SuspendProfileBoundary:
    """Boundary — SuspendProfileBoundary (UA-04)"""

    @staticmethod
    @profile_management_bp.route('/<int:profile_id>/suspend', methods=['PUT'])
    @token_required(roles=['admin'])
    def suspend_profile(current_user, profile_id):
        ok, payload = SuspendProfileController.suspendProfile(profile_id)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400


class ActivateProfileBoundary:
    """Boundary — ActivateProfileBoundary (UA-04)"""

    @staticmethod
    @profile_management_bp.route('/<int:profile_id>/activate', methods=['PUT'])
    @token_required(roles=['admin'])
    def activate_profile(current_user, profile_id):
        ok, payload = ActivateProfileController.activateProfile(profile_id)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400


class SearchProfileBoundary:
    """Boundary — SearchProfileBoundary (UA-05)"""

    @staticmethod
    def _search(query: str):
        ok, payload = SearchProfileController.searchProfile(query)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404