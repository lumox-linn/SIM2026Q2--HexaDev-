"""
app/services/history_controller.py — Control Layer
====================================================
Sprint 6 — FR-HS-01, FR-HS-02, DN-HS-01, DN-HS-02

Separate controller class per use case:
- SearchFRHistoryController    (FR-HS-01) — search/filter FR history
- ViewFRHistoryController      (FR-HS-02) — view all FR completed history
- SearchDoneeHistoryController (DN-HS-01) — search/filter donee history
- ViewDoneeHistoryController   (DN-HS-02) — view all donee donation history
"""
from app.models.activity import Activity
from app.models.donation import Donation


class SearchFRHistoryController:
    """Control — SearchFRHistoryController (FR-HS-01)
    Search completed activities filtered by category and date period.
    """

    @staticmethod
    def searchHistory(user_id: int, category_id: int = None,
                      start_date: str = None, end_date: str = None):
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


class ViewFRHistoryController:
    """Control — ViewFRHistoryController (FR-HS-02)
    View all completed/ended activities for a Fund Raiser.
    """

    @staticmethod
    def getHistory(user_id: int):
        activities = Activity.getHistory(user_id=user_id)
        if not activities:
            return False, {
                'status': 'fail',
                'error':  'No completed activities found.'
            }
        return True, {
            'status':     'success',
            'message':    f'{len(activities)} completed activity(s) found.',
            'activities': activities
        }


class SearchDoneeHistoryController:
    """Control — SearchDoneeHistoryController (DN-HS-01)
    Search donation history filtered by category and date period.
    """

    @staticmethod
    def searchHistory(user_id: int, category_id: int = None,
                      start_date: str = None, end_date: str = None):
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


class ViewDoneeHistoryController:
    """Control — ViewDoneeHistoryController (DN-HS-02)
    View all donation history for a Donee.
    """

    @staticmethod
    def getDoneeHistory(user_id: int):
        history = Donation.getHistory(user_id=user_id)
        if not history:
            return False, {
                'status': 'fail',
                'error':  'No donation history found.'
            }
        return True, {
            'status':  'success',
            'message': f'{len(history)} donation(s) found.',
            'history': history
        }