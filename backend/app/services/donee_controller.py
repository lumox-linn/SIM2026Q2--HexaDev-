"""
app/services/donee_controller.py — Control Layer
==================================================
Sprint 5 — DN-01 to DN-05: Donee Browse & Favourites

Separate controller class per use case:
- SearchActivityController  (DN-01) — search activities
- BrowseActivityController  (DN-02) — browse + view activities
- SaveFavouriteController   (DN-03) — save to favourites
- RemoveFavouriteController (DN-03) — remove from favourites
- SearchFavouriteController (DN-04) — search favourites
- ViewFavouriteController   (DN-05) — view all favourites
"""
from app.models.activity import Activity
from app.models.favourite import Favourite


class SearchActivityController:
    """Control — SearchActivityController (DN-01)
    Search all active activities by title.
    """

    @staticmethod
    def searchActivities(query: str):
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


class BrowseActivityController:
    """Control — BrowseActivityController (DN-02)
    Browse all active activities or view one activity.
    """

    @staticmethod
    def getAllActivities():
        activities = Activity.getAll()
        active = [a for a in activities if a['status'] == 'active']
        return True, {
            'status':     'success',
            'message':    f'{len(active)} activity(s) found.',
            'activities': active
        }

    @staticmethod
    def viewActivity(activity_id: int):
        activity = Activity.findById(activity_id)
        if not activity:
            return False, {
                'status': 'fail',
                'error':  f'Activity with ID {activity_id} not found.'
            }
            
        Activity.incrementViewCount(activity_id)
        
        return True, {
            'status':   'success',
            'activity': activity
        }


class SaveFavouriteController:
    """Control — SaveFavouriteController (DN-03)
    Save an activity to favourites.
    """

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


class RemoveFavouriteController:
    """Control — RemoveFavouriteController (DN-03)
    Remove an activity from favourites.
    """

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


class SearchFavouriteController:
    """Control — SearchFavouriteController (DN-04)
    Search saved favourites by activity title.
    """

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


class ViewFavouriteController:
    """Control — ViewFavouriteController (DN-05)
    View all saved favourites.
    """

    @staticmethod
    def getAllFavourites(user_id: int):
        favourites = Favourite.getAll(user_id)
        return True, {
            'status':     'success',
            'message':    f'{len(favourites)} favourite(s) found.',
            'favourites': favourites
        }