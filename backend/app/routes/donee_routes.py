"""
app/routes/donee_routes.py — Boundary Layer
=============================================
Sprint 5 — DN-01 to DN-05: Donee Browse & Favourites

Separate boundary class per use case:
- SearchActivityBoundary  (DN-01) — search activities
- BrowseActivityBoundary  (DN-02) — browse + view activities
- SaveFavouriteBoundary   (DN-03) — save to favourites
- RemoveFavouriteBoundary (DN-03) — remove from favourites
- SearchFavouriteBoundary (DN-04) — search favourites
- ViewFavouriteBoundary   (DN-05) — view all favourites
"""
from flask import Blueprint, request, jsonify
from app.services.donee_controller import (
    SearchActivityController,
    BrowseActivityController,
    SaveFavouriteController,
    RemoveFavouriteController,
    SearchFavouriteController,
    ViewFavouriteController,
)
from app.utils.auth_utils import token_required

donee_bp = Blueprint('donee', __name__)


class SearchActivityBoundary:
    """Boundary — SearchActivityBoundary (DN-01)
    Search for fundraising activities by title.
    """

    @staticmethod
    @donee_bp.route('/activities/search', methods=['GET'])
    @token_required(roles=['donee'])
    def search_activities(current_user):
        query = request.args.get('query', '').strip()

        # [BOUNDARY] Validate empty query
        if not query:
            return jsonify({'status': 'fail', 'error': 'Search query cannot be empty.'}), 400

        ok, payload = SearchActivityController.searchActivities(query)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404


class BrowseActivityBoundary:
    """Boundary — BrowseActivityBoundary (DN-02)
    Browse all active activities or view one activity.
    """

    @staticmethod
    @donee_bp.route('/activities', methods=['GET'])
    @token_required(roles=['donee'])
    def browse_activities(current_user):
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
    """Boundary — SaveFavouriteBoundary (DN-03)
    Save an activity to favourites.
    """

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


class RemoveFavouriteBoundary:
    """Boundary — RemoveFavouriteBoundary (DN-03)
    Remove an activity from favourites.
    """

    @staticmethod
    @donee_bp.route('/favourites/<int:activity_id>', methods=['DELETE'])
    @token_required(roles=['donee'])
    def remove_favourite(current_user, activity_id):
        ok, payload = RemoveFavouriteController.removeFavourite(
            current_user['user_id'], activity_id
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400


class SearchFavouriteBoundary:
    """Boundary — SearchFavouriteBoundary (DN-04)
    Search saved favourites by activity title.
    """

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


class ViewFavouriteBoundary:
    """Boundary — ViewFavouriteBoundary (DN-05)
    View all saved favourites.
    """

    @staticmethod
    @donee_bp.route('/favourites', methods=['GET'])
    @token_required(roles=['donee'])
    def get_favourites(current_user):
        ok, payload = ViewFavouriteController.getAllFavourites(current_user['user_id'])
        return jsonify(payload), 200