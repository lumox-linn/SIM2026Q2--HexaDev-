"""
app/routes/activity_routes.py — Boundary Layer
================================================
Sprint 4 — FR-01 to FR-05: Fundraising Activity Management

Separate boundary class per use case:
- CreateActivityBoundary (FR-01)
- ViewActivityBoundary   (FR-02)
- UpdateActivityBoundary (FR-03)
- DeleteActivityBoundary (FR-04)
- SearchActivityBoundary (FR-05)
"""
from flask import Blueprint, request, jsonify
from app.services.activity_controller import (
    CreateActivityController,
    ViewActivityController,
    UpdateActivityController,
    DeleteActivityController,
    SearchActivityController,
)
from app.utils.auth_utils import token_required

activity_bp = Blueprint('activity', __name__)


class CreateActivityBoundary:
    """Boundary — CreateActivityBoundary (FR-01)"""

    @staticmethod
    @activity_bp.route('/', methods=['POST'])
    @token_required(roles=['fund_raiser'])
    def create_activity(current_user):
        data = request.get_json()

        # [BOUNDARY] Input validation
        if not data:
            return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400
        if not data.get('title') or not str(data['title']).strip():
            return jsonify({'status': 'fail', 'error': 'Title is required.'}), 400
        if len(str(data['title']).strip()) < 3:
            return jsonify({'status': 'fail', 'error': 'Title must be at least 3 characters.'}), 400

        ok, payload = CreateActivityController.createActivity(data, current_user['user_id'])
        if ok:
            return jsonify(payload), 201
        return jsonify(payload), 400


class ViewActivityBoundary:
    """Boundary — ViewActivityBoundary (FR-02)"""

    @staticmethod
    @activity_bp.route('/', methods=['GET'])
    @token_required(roles=['fund_raiser'])
    def get_all_activities(current_user):
        query = request.args.get('query', '').strip()

        # [BOUNDARY] Validate empty query
        if 'query' in request.args and query == '':
            return jsonify({'status': 'fail', 'error': 'Search query cannot be empty.'}), 400

        if query:
            ok, payload = SearchActivityController.searchActivity(
                query, user_id=current_user['user_id']
            )
            if ok:
                return jsonify(payload), 200
            return jsonify(payload), 404

        ok, payload = ViewActivityController.getAllActivities(
            user_id=current_user['user_id']
        )
        return jsonify(payload), 200

    @staticmethod
    @activity_bp.route('/<int:activity_id>', methods=['GET'])
    @token_required(roles=['fund_raiser'])
    def view_activity(current_user, activity_id):
        ok, payload = ViewActivityController.viewActivity(activity_id)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404


class UpdateActivityBoundary:
    """Boundary — UpdateActivityBoundary (FR-03)"""

    @staticmethod
    @activity_bp.route('/<int:activity_id>', methods=['PUT'])
    @token_required(roles=['fund_raiser'])
    def update_activity(current_user, activity_id):
        data = request.get_json()

        # [BOUNDARY] Input validation
        if not data:
            return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400
        if data.get('title') and len(str(data['title']).strip()) < 3:
            return jsonify({'status': 'fail', 'error': 'Title must be at least 3 characters.'}), 400

        ok, payload = UpdateActivityController.updateActivity(
            activity_id, current_user['user_id'], data
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400


class DeleteActivityBoundary:
    """Boundary — DeleteActivityBoundary (FR-04)"""

    @staticmethod
    @activity_bp.route('/<int:activity_id>', methods=['DELETE'])
    @token_required(roles=['fund_raiser'])
    def delete_activity(current_user, activity_id):
        ok, payload = DeleteActivityController.deleteActivity(
            activity_id, current_user['user_id']
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400


class SearchActivityBoundary:
    """Boundary — SearchActivityBoundary (FR-05)"""

    @staticmethod
    @activity_bp.route('/search', methods=['GET'])
    @token_required(roles=['fund_raiser'])
    def search_activities(current_user):
        query = request.args.get('query', '').strip()

        # [BOUNDARY] Validate empty query
        if not query:
            return jsonify({'status': 'fail', 'error': 'Search query cannot be empty.'}), 400

        ok, payload = SearchActivityController.searchActivity(
            query, user_id=current_user['user_id']
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404
