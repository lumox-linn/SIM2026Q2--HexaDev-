"""
app/routes/interest_routes.py — Boundary Layer
================================================
Sprint 6 — FR-IT-01, FR-IT-02: Fund Raiser Interest Tracking

Separate boundary class per use case:
- ViewInterestBoundary   (FR-IT-01) — view count
- ViewShortlistBoundary  (FR-IT-02) — shortlist count
"""
from flask import Blueprint, jsonify
from app.services.interest_controller import (
    ViewInterestController,
    ViewShortlistController,
)
from app.utils.auth_utils import token_required

interest_bp = Blueprint('interest', __name__)


class ViewInterestBoundary:
    """Boundary — ViewInterestBoundary (FR-IT-01)
    View number of views for all FR's activities.
    """

    @staticmethod
    @interest_bp.route('/', methods=['GET'])
    @token_required(roles=['fund_raiser'])
    def get_all_interest(current_user):
        ok, payload = ViewInterestController.getAllInterest(current_user['user_id'])
        return jsonify(payload), 200


class ViewShortlistBoundary:
    """Boundary — ViewShortlistBoundary (FR-IT-02)
    View number of times an activity has been shortlisted/saved.
    """

    @staticmethod
    @interest_bp.route('/<int:activity_id>', methods=['GET'])
    @token_required(roles=['fund_raiser'])
    def get_activity_interest(current_user, activity_id):
        ok, payload = ViewShortlistController.getActivityInterest(
            activity_id, current_user['user_id']
        )
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400