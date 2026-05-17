"""
app/routes/history_routes.py — Boundary Layer
===============================================
Sprint 6 — FR-HS-01, FR-HS-02, DN-HS-01, DN-HS-02

Separate boundary class per use case:
- SearchFRHistoryBoundary    (FR-HS-01) — search/filter FR history
- ViewFRHistoryBoundary      (FR-HS-02) — view all FR completed history
- SearchDoneeHistoryBoundary (DN-HS-01) — search/filter donee history
- ViewDoneeHistoryBoundary   (DN-HS-02) — view all donee donation history
"""
from flask import Blueprint, request, jsonify
from app.services.history_controller import (
    SearchFRHistoryController,
    ViewFRHistoryController,
    SearchDoneeHistoryController,
    ViewDoneeHistoryController,
)
from app.utils.auth_utils import token_required

history_bp = Blueprint('history', __name__)


class SearchFRHistoryBoundary:
    """Boundary — SearchFRHistoryBoundary (FR-HS-01)
    Search/filter history of completed FSA by category and date period.
    """

    @staticmethod
    @history_bp.route('/fr/search', methods=['GET'])
    @token_required(roles=['fund_raiser'])
    def search_fr_history(current_user):
        category_id = request.args.get('category_id')
        start_date  = request.args.get('start_date')
        end_date    = request.args.get('end_date')

        # [BOUNDARY] Validate at least one filter provided
        if not category_id and not start_date and not end_date:
            return jsonify({'status': 'fail', 'error': 'At least one filter is required.'}), 400

        # [BOUNDARY] Validate date range
        if start_date and end_date and start_date > end_date:
            return jsonify({'status': 'fail', 'error': 'start_date cannot be after end_date.'}), 400

        ok, payload = SearchFRHistoryController.searchHistory(
            user_id=current_user['user_id'],
            category_id=int(category_id) if category_id else None,
            start_date=start_date,
            end_date=end_date
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404


class ViewFRHistoryBoundary:
    """Boundary — ViewFRHistoryBoundary (FR-HS-02)
    View all completed/ended fundraising activity history.
    """

    @staticmethod
    @history_bp.route('/fr', methods=['GET'])
    @token_required(roles=['fund_raiser'])
    def get_fr_history(current_user):
        ok, payload = ViewFRHistoryController.getHistory(
            user_id=current_user['user_id']
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404


class SearchDoneeHistoryBoundary:
    """Boundary — SearchDoneeHistoryBoundary (DN-HS-01)
    Search/filter donation history by category and date period.
    """

    @staticmethod
    @history_bp.route('/donee/search', methods=['GET'])
    @token_required(roles=['donee'])
    def search_donee_history(current_user):
        category_id = request.args.get('category_id')
        start_date  = request.args.get('start_date')
        end_date    = request.args.get('end_date')

        # [BOUNDARY] Validate at least one filter provided
        if not category_id and not start_date and not end_date:
            return jsonify({'status': 'fail', 'error': 'At least one filter is required.'}), 400

        # [BOUNDARY] Validate date range
        if start_date and end_date and start_date > end_date:
            return jsonify({'status': 'fail', 'error': 'start_date cannot be after end_date.'}), 400

        ok, payload = SearchDoneeHistoryController.searchHistory(
            user_id=current_user['user_id'],
            category_id=int(category_id) if category_id else None,
            start_date=start_date,
            end_date=end_date
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404


class ViewDoneeHistoryBoundary:
    """Boundary — ViewDoneeHistoryBoundary (DN-HS-02)
    View all donation history and monitor FSA progress.
    """

    @staticmethod
    @history_bp.route('/donee', methods=['GET'])
    @token_required(roles=['donee'])
    def get_donee_history(current_user):
        ok, payload = ViewDoneeHistoryController.getDoneeHistory(
            user_id=current_user['user_id']
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404