"""
app/routes/profile_management_routes.py — Boundary Layer
==========================================================
Sprint 2 — User Admin Profile Management API endpoints

All endpoints protected with @token_required(roles=['admin'])

Endpoints:
  GET    /api/profiles/              → get all profiles (UA-02)
  GET    /api/profiles/?query=xx     → search profiles (UA-05)
  GET    /api/profiles/<profile_id>  → view one profile (UA-02)
  POST   /api/profiles/              → create profile (UA-01)
  PUT    /api/profiles/<profile_id>  → update profile (UA-03)
  PUT    /api/profiles/<profile_id>/suspend  → suspend profile (UA-04)
  PUT    /api/profiles/<profile_id>/activate → activate profile (UA-04)
"""
from flask import Blueprint, request, jsonify
from app.services.profile_management_controller import ProfileManagementController
from app.utils.auth_utils import token_required

profile_management_bp = Blueprint('profile_management', __name__)


@profile_management_bp.route('/', methods=['GET'])
@token_required(roles=['admin'])
def get_all_profiles(current_user):
    """
    GET /api/profiles/
    GET /api/profiles/?query=donee  ← search by name

    Returns all profiles or search results.
    """
    query = request.args.get('query', '').strip()

    if query is not None and query == '' and 'query' in request.args:
        return jsonify({'status': 'fail', 'error': 'Search query cannot be empty.'}), 400

    if query:
        ok, payload = ProfileManagementController.searchProfile(query)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404

    ok, payload = ProfileManagementController.getAllProfiles()
    return jsonify(payload), 200


@profile_management_bp.route('/<int:profile_id>', methods=['GET'])
@token_required(roles=['admin'])
def view_profile(current_user, profile_id):
    """
    GET /api/profiles/<profile_id>
    View a single profile by ID.
    """
    ok, payload = ProfileManagementController.viewProfile(profile_id)
    if ok:
        return jsonify(payload), 200
    return jsonify(payload), 404


@profile_management_bp.route('/', methods=['POST'])
@token_required(roles=['admin'])
def create_profile(current_user):
    """
    POST /api/profiles/
    Create a new profile (role type).

    Body: { "profile_name": "moderator", "description": "Moderates content" }
    """
    data = request.get_json()
    if not data:
        return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400

    ok, payload = ProfileManagementController.createProfile(data)
    if ok:
        return jsonify(payload), 201
    return jsonify(payload), 400


@profile_management_bp.route('/<int:profile_id>', methods=['PUT'])
@token_required(roles=['admin'])
def update_profile(current_user, profile_id):
    """
    PUT /api/profiles/<profile_id>
    Update a profile's details.

    Body: { "profile_name": "new_name", "description": "new description" }
    """
    data = request.get_json()
    if not data:
        return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400

    ok, payload = ProfileManagementController.updateProfile(profile_id, data)
    if ok:
        return jsonify(payload), 200
    return jsonify(payload), 400


@profile_management_bp.route('/<int:profile_id>/suspend', methods=['PUT'])
@token_required(roles=['admin'])
def suspend_profile(current_user, profile_id):
    """
    PUT /api/profiles/<profile_id>/suspend
    Suspend a profile — also suspends all accounts with this profile.
    """
    ok, payload = ProfileManagementController.suspendProfile(profile_id)
    if ok:
        return jsonify(payload), 200
    return jsonify(payload), 400


@profile_management_bp.route('/<int:profile_id>/activate', methods=['PUT'])
@token_required(roles=['admin'])
def activate_profile(current_user, profile_id):
    """
    PUT /api/profiles/<profile_id>/activate
    Reactivate a suspended profile.
    """
    ok, payload = ProfileManagementController.activateProfile(profile_id)
    if ok:
        return jsonify(payload), 200
    return jsonify(payload), 400