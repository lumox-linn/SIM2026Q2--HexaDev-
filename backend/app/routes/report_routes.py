"""
app/routes/report_routes.py — Boundary Layer
==============================================
Sprint 6 — PM-06, PM-07, PM-08: Platform Manager Reports

Separate boundary class per use case:
- DailyReportBoundary   (PM-06)
- WeeklyReportBoundary  (PM-07)
- MonthlyReportBoundary (PM-08)
"""
from flask import Blueprint, jsonify
from app.services.report_controller import (
    DailyReportController,
    WeeklyReportController,
    MonthlyReportController,
)
from app.utils.auth_utils import token_required

report_bp = Blueprint('report', __name__)


class DailyReportBoundary:
    """Boundary — DailyReportBoundary (PM-06)"""

    @staticmethod
    @report_bp.route('/daily', methods=['GET'])
    @token_required(roles=['platform_manager'])
    def get_daily_report(current_user):
        ok, payload = DailyReportController.generateDailyReport()
        return jsonify(payload), 200


class WeeklyReportBoundary:
    """Boundary — WeeklyReportBoundary (PM-07)"""

    @staticmethod
    @report_bp.route('/weekly', methods=['GET'])
    @token_required(roles=['platform_manager'])
    def get_weekly_report(current_user):
        ok, payload = WeeklyReportController.generateWeeklyReport()
        return jsonify(payload), 200


class MonthlyReportBoundary:
    """Boundary — MonthlyReportBoundary (PM-08)"""

    @staticmethod
    @report_bp.route('/monthly', methods=['GET'])
    @token_required(roles=['platform_manager'])
    def get_monthly_report(current_user):
        ok, payload = MonthlyReportController.generateMonthlyReport()
        return jsonify(payload), 200
