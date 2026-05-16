"""
app/services/report_controller.py — Control Layer
===================================================
Sprint 6 — PM-06, PM-07, PM-08: Platform Manager Reports

Separate controller class per use case:
- DailyReportController   (PM-06)
- WeeklyReportController  (PM-07)
- MonthlyReportController (PM-08)
"""
from app.models.report import Report


class DailyReportController:
    """Control — DailyReportController (PM-06)"""

    @staticmethod
    def generateDailyReport():
        report = Report.getDaily()
        return True, {
            'status': 'success',
            'report': report
        }


class WeeklyReportController:
    """Control — WeeklyReportController (PM-07)"""

    @staticmethod
    def generateWeeklyReport():
        report = Report.getWeekly()
        return True, {
            'status': 'success',
            'report': report
        }


class MonthlyReportController:
    """Control — MonthlyReportController (PM-08)"""

    @staticmethod
    def generateMonthlyReport():
        report = Report.getMonthly()
        return True, {
            'status': 'success',
            'report': report
        }
