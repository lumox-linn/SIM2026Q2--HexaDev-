"""
app/routes/donee_routes.py — Boundary Layer
=============================================
Sprint 5 — DN-01 to DN-05: Donee Browse & Favourites

Separate boundary class per use case:
- BrowseActivityBoundary  (DN-01, DN-02)
- SaveFavouriteBoundary   (DN-03)
- SearchFavouriteBoundary (DN-04)
- ViewFavouriteBoundary   (DN-05)
"""
from flask import Blueprint, request, jsonify
from app.services.donee_controller import (
    BrowseActivityController,
    SaveFavouriteController,
    ViewFavouriteController,
    SearchFavouriteController,
)
from app.utils.auth_utils import token_required

donee_bp = Blueprint('donee', __name__)


class BrowseActivityBoundary:
    """Boundary — BrowseActivityBoundary (DN-01, DN-02)"""

    @staticmethod
    @donee_bp.route('/activities', methods=['GET'])
    @token_required(roles=['donee'])
    def browse_activities(current_user):
        query = request.args.get('query', '').strip()

        # [BOUNDARY] Validate empty query
        if 'query' in request.args and query == '':
            return jsonify({'status': 'fail', 'error': 'Search query cannot be empty.'}), 400

        if query:
            ok, payload = BrowseActivityController.searchActivities(query)
            if ok:
                return jsonify(payload), 200
            return jsonify(payload), 404

        ok, payload = BrowseActivityController.getAllActivities()
        return jsonify(payload), 200

    @staticmethod
    @donee_bp.route('/activities/<int:activity_id>', methods=['GET'])
    @token_required(roles=['donee'])
    def view_activity(current_user, activity_id):
        ok, payload = BrowseActivityController.viewActivity(activity_id)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404


class SaveFavouriteBoundary:
    """Boundary — SaveFavouriteBoundary (DN-03)"""

    @staticmethod
    @donee_bp.route('/favourites', methods=['POST'])
    @token_required(roles=['donee'])
    def save_favourite(current_user):
        data = request.get_json()

        # [BOUNDARY] Input validation
        if not data:
            return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400
        if not data.get('activity_id'):
            return jsonify({'status': 'fail', 'error': 'Activity ID is required.'}), 400

        ok, payload = SaveFavouriteController.saveFavourite(
            current_user['user_id'], data['activity_id']
        )
        if ok:
            return jsonify(payload), 201
        return jsonify(payload), 400

    @staticmethod
    @donee_bp.route('/favourites/<int:activity_id>', methods=['DELETE'])
    @token_required(roles=['donee'])
    def remove_favourite(current_user, activity_id):
        ok, payload = SaveFavouriteController.removeFavourite(
            current_user['user_id'], activity_id
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400


class ViewFavouriteBoundary:
    """Boundary — ViewFavouriteBoundary (DN-05)"""

    @staticmethod
    @donee_bp.route('/favourites', methods=['GET'])
    @token_required(roles=['donee'])
    def get_favourites(current_user):
        query = request.args.get('query', '').strip()

        # [BOUNDARY] Validate empty query
        if 'query' in request.args and query == '':
            return jsonify({'status': 'fail', 'error': 'Search query cannot be empty.'}), 400

        if query:
            ok, payload = SearchFavouriteController.searchFavourites(
                query, current_user['user_id']
            )
            if ok:
                return jsonify(payload), 200
            return jsonify(payload), 404

        ok, payload = ViewFavouriteController.getAllFavourites(current_user['user_id'])
        return jsonify(payload), 200


class SearchFavouriteBoundary:
    """Boundary — SearchFavouriteBoundary (DN-04)"""

    @staticmethod
    @donee_bp.route('/favourites/search', methods=['GET'])
    @token_required(roles=['donee'])
    def search_favourites(current_user):
        query = request.args.get('query', '').strip()

        if not query:
            return jsonify({'status': 'fail', 'error': 'Search query cannot be empty.'}), 400

        ok, payload = SearchFavouriteController.searchFavourites(
            query, current_user['user_id']
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404
