"""
app/services/activity_controller.py — Control Layer
=====================================================
Sprint 4 — FR-01 to FR-05: Fundraising Activity Management

Separate controller class per use case:
- CreateActivityController (FR-01)
- ViewActivityController   (FR-02)
- UpdateActivityController (FR-03)
- DeleteActivityController (FR-04)
- SearchActivityController (FR-05)
"""
from app.models.activity import Activity


class CreateActivityController:
    """Control — CreateActivityController (FR-01)"""

    @staticmethod
    def createActivity(data: dict, user_id: int):
        result = Activity.create({
            'title':         data['title'],
            'description':   data.get('description', None),
            'category_id':   data.get('category_id', None),
            'created_by':    user_id,
            'target_amount': data.get('target_amount', 0.00),
            'start_date':    data.get('start_date', None),
            'end_date':      data.get('end_date', None),
        })

        if not result:
            return False, {
                'status': 'fail',
                'error':  f"You already have an activity titled '{data['title']}'."
            }
        return True, {
            'status':  'success',
            'message': f"Activity '{data['title']}' created successfully."
        }


class ViewActivityController:
    """Control — ViewActivityController (FR-02)"""

    @staticmethod
    def getAllActivities(user_id: int = None):
        activities = Activity.getAll(user_id=user_id)
        return True, {
            'status':     'success',
            'message':    f'{len(activities)} activity(s) found.',
            'activities': activities
        }

    @staticmethod
    def viewActivity(activity_id: int):
        activity = Activity.findById(activity_id)
        if not activity:
            return False, {
                'status': 'fail',
                'error':  f'Activity with ID {activity_id} not found.'
            }
        return True, {
            'status':   'success',
            'activity': activity
        }


class UpdateActivityController:
    """Control — UpdateActivityController (FR-03)"""

    @staticmethod
    def updateActivity(activity_id: int, user_id: int, data: dict):
        result = Activity.update(activity_id, user_id, data)

        if result == 'not_found':
            return False, {
                'status': 'fail',
                'error':  f'Activity with ID {activity_id} not found.'
            }
        if result == 'unauthorized':
            return False, {
                'status': 'fail',
                'error':  'You can only update your own activities.'
            }
        return True, {
            'status':      'success',
            'message':     'Activity updated successfully.',
            'activity_id': activity_id
        }


class SuspendActivityController:
    """Control — SuspendActivityController (FR-04)"""

    @staticmethod
    def suspendActivity(activity_id: int, user_id: int):
        result = Activity.suspend(activity_id, user_id)

        if result == 'not_found':
            return False, {
                'status': 'fail',
                'error':  f'Activity with ID {activity_id} not found.'
            }
        if result == 'unauthorized':
            return False, {
                'status': 'fail',
                'error':  'You can only suspend your own activities.'
            }
        return True, {
            'status':      'success',
            'message':     'Activity suspended successfully.',
            'activity_id': activity_id
        }


class SearchActivityController:
    """Control — SearchActivityController (FR-05)"""

    @staticmethod
    def searchActivity(query: str, user_id: int = None):
        activities = Activity.search(query.strip(), user_id=user_id)
        if not activities:
            return False, {
                'status': 'fail',
                'error':  f"No activities found matching '{query}'."
            }
        return True, {
            'status':     'success',
            'message':    f'{len(activities)} activity(s) found.',
            'activities': activities
        }


# Backward compatibility alias
class ActivityController:
    createActivity  = CreateActivityController.createActivity
    getAllActivities = ViewActivityController.getAllActivities
    viewActivity    = ViewActivityController.viewActivity
    updateActivity  = UpdateActivityController.updateActivity
    suspendActivity = SuspendActivityController.suspendActivity
    searchActivity  = SearchActivityController.searchActivity