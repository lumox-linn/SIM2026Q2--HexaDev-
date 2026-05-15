"""
app/services/donee_controller.py — Control Layer
==================================================
Sprint 5 — DN-01 to DN-05: Donee Browse & Favourites

Separate controller class per use case:
- BrowseActivityController  (DN-01, DN-02)
- SaveFavouriteController   (DN-03)
- SearchFavouriteController (DN-04)
- ViewFavouriteController   (DN-05)
"""
from app.models.activity import Activity
from app.models.favourite import Favourite


class BrowseActivityController:
    """Control — BrowseActivityController (DN-01, DN-02)"""

    @staticmethod
    def getAllActivities():
        """DN-02 — Get all active activities (all fund raisers)."""
        activities = Activity.getAll()
        active = [a for a in activities if a['status'] == 'active']
        return True, {
            'status':     'success',
            'message':    f'{len(active)} activity(s) found.',
            'activities': active
        }

    @staticmethod
    def searchActivities(query: str):
        """DN-01 — Search all active activities by title."""
        activities = Activity.search(query.strip())
        active = [a for a in activities if a['status'] == 'active']
        if not active:
            return False, {
                'status': 'fail',
                'error':  f"No activities found matching '{query}'."
            }
        return True, {
            'status':     'success',
            'message':    f'{len(active)} activity(s) found.',
            'activities': active
        }

    @staticmethod
    def viewActivity(activity_id: int):
        """DN-02 — View one activity details."""
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


class SaveFavouriteController:
    """Control — SaveFavouriteController (DN-03)"""

    @staticmethod
    def saveFavourite(user_id: int, activity_id: int):
        result = Favourite.save(user_id, activity_id)

        if result == 'already_saved':
            return False, {
                'status': 'fail',
                'error':  'Activity is already in your favourites.'
            }
        if result == 'not_found':
            return False, {
                'status': 'fail',
                'error':  f'Activity with ID {activity_id} not found.'
            }
        return True, {
            'status':  'success',
            'message': 'Activity saved to favourites.'
        }

    @staticmethod
    def removeFavourite(user_id: int, activity_id: int):
        result = Favourite.remove(user_id, activity_id)

        if result == 'not_found':
            return False, {
                'status': 'fail',
                'error':  'Activity is not in your favourites.'
            }
        return True, {
            'status':  'success',
            'message': 'Activity removed from favourites.'
        }


class ViewFavouriteController:
    """Control — ViewFavouriteController (DN-05)"""

    @staticmethod
    def getAllFavourites(user_id: int):
        favourites = Favourite.getAll(user_id)
        return True, {
            'status':     'success',
            'message':    f'{len(favourites)} favourite(s) found.',
            'favourites': favourites
        }


class SearchFavouriteController:
    """Control — SearchFavouriteController (DN-04)"""

    @staticmethod
    def searchFavourites(query: str, user_id: int):
        favourites = Favourite.search(query.strip(), user_id)
        if not favourites:
            return False, {
                'status': 'fail',
                'error':  f"No favourites found matching '{query}'."
            }
        return True, {
            'status':     'success',
            'message':    f'{len(favourites)} favourite(s) found.',
            'favourites': favourites
        }
