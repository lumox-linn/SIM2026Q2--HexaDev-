"""
app/services/interest_controller.py — Control Layer
=====================================================
Sprint 6 — FR-IT-01, FR-IT-02: Fund Raiser Interest Tracking

Separate controller class per use case:
- ViewInterestController  (FR-IT-01) — view count
- ViewShortlistController (FR-IT-02) — shortlist count
"""
from app.models.activity import Activity


class ViewInterestController:
    """Control — ViewInterestController (FR-IT-01)
    View number of views for all FR's activities.
    """

    @staticmethod
    def getAllInterest(user_id: int):
        """Get view count for all activities owned by this FR."""
        activities = Activity.getAll(user_id=user_id)
        return True, {
            'status':     'success',
            'activities': [
                {
                    'activity_id': a['activity_id'],
                    'title':       a['title'],
                    'view_count':  a.get('view_count', 0),
                    'status':      a['status'],
                }
                for a in activities
            ]
        }


class ViewShortlistController:
    """Control — ViewShortlistController (FR-IT-02)
    View number of times an activity has been shortlisted/saved.
    """

    @staticmethod
    def getActivityInterest(activity_id: int, user_id: int):
        """Get view count and shortlist count for one activity."""
        activity = Activity.findById(activity_id)

        if not activity:
            return False, {
                'status': 'fail',
                'error':  f'Activity with ID {activity_id} not found.'
            }
        if activity['created_by'] != user_id:
            return False, {
                'status': 'fail',
                'error':  'You can only view interest for your own activities.'
            }

        return True, {
            'status':          'success',
            'activity_id':     activity_id,
            'title':           activity['title'],
            'view_count':      activity.get('view_count', 0),
            'shortlist_count': activity.get('shortlist_count', 0),
        }