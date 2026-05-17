"""
app/routes/history_routes.py — Boundary Layer
===============================================
Sprint 6 — FR-HS-01, FR-HS-02, DN-HS-01, DN-HS-02

Separate boundary class per usecase:
- ViewFRHistoryBoundary    (FR-HS-01, FR-HS-02)
- ViewDoneeHistoryBoundary (DN-HS-01, DN-HS-02)
"""
from flask import Blueprint, request, jsonify
from app.services.history_controller import (
    ViewFRHistoryController,
    ViewDoneeHistoryController,
)
from app.utils.auth_utils import token_required

history_bp = Blueprint('history', __name__)


class ViewFRHistoryBoundary:
    """Boundary — ViewFRHistoryBoundary (FR-HS-01, FR-HS-02)"""

    @staticmethod
    @history_bp.route('/fr', methods=['GET'])
    @token_required(roles=['fund_raiser'])
    def get_fr_history(current_user):
        """
        Get completed activity history for Fund Raiser.
        Optional filters: category_id, start_date, end_date
        """
        category_id = request.args.get('category_id')
        start_date  = request.args.get('start_date')
        end_date    = request.args.get('end_date')

        # [BOUNDARY] Validate date range
        if start_date and end_date and start_date > end_date:
            return jsonify({'status': 'fail', 'error': 'start_date cannot be after end_date.'}), 400

        ok, payload = ViewFRHistoryController.getHistory(
            user_id=current_user['user_id'],
            category_id=int(category_id) if category_id else None,
            start_date=start_date,
            end_date=end_date
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404


class ViewDoneeHistoryBoundary:
    """Boundary — ViewDoneeHistoryBoundary (DN-HS-01, DN-HS-02)"""

    @staticmethod
    @history_bp.route('/donee', methods=['GET'])
    @token_required(roles=['donee'])
    def get_donee_history(current_user):
        """
        Get donation history for Donee.
        Optional filters: category_id, start_date, end_date
        """
        category_id = request.args.get('category_id')
        start_date  = request.args.get('start_date')
        end_date    = request.args.get('end_date')

        # [BOUNDARY] Validate date range
        if start_date and end_date and start_date > end_date:
            return jsonify({'status': 'fail', 'error': 'start_date cannot be after end_date.'}), 400

        ok, payload = ViewDoneeHistoryController.getDoneeHistory(
            user_id=current_user['user_id'],
            category_id=int(category_id) if category_id else None,
            start_date=start_date,
            end_date=end_date
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404
