"""
app/services/history_controller.py — Control Layer
====================================================
Sprint 6 — FR-HS-01, FR-HS-02, DN-HS-01, DN-HS-02

Separate controller class per use case:
- ViewFRHistoryController    (FR-HS-01, FR-HS-02)
- ViewDoneeHistoryController (DN-HS-01, DN-HS-02)
"""
from app.models.activity import Activity
from app.models.donation import Donation


class ViewFRHistoryController:
    """Control — ViewFRHistoryController (FR-HS-01, FR-HS-02)"""

    @staticmethod
    def getHistory(user_id: int, category_id: int = None,
                   start_date: str = None, end_date: str = None):
        """Get completed/ended activity history for a Fund Raiser."""
        activities = Activity.getHistory(
            user_id=user_id,
            category_id=category_id,
            start_date=start_date,
            end_date=end_date
        )
        if not activities:
            return False, {
                'status': 'fail',
                'error':  'No completed activities found for the given filters.'
            }
        return True, {
            'status':     'success',
            'message':    f'{len(activities)} completed activity(s) found.',
            'activities': activities
        }


class ViewDoneeHistoryController:
    """Control — ViewDoneeHistoryController (DN-HS-01, DN-HS-02)"""

    @staticmethod
    def getDoneeHistory(user_id: int, category_id: int = None,
                        start_date: str = None, end_date: str = None):
        """Get donation history for a Donee."""
        history = Donation.getHistory(
            user_id=user_id,
            category_id=category_id,
            start_date=start_date,
            end_date=end_date
        )
        if not history:
            return False, {
                'status': 'fail',
                'error':  'No donation history found for the given filters.'
            }
        return True, {
            'status':  'success',
            'message': f'{len(history)} donation(s) found.',
            'history': history
        }