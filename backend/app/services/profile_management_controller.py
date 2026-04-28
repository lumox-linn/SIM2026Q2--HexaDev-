"""
app/services/profile_management_controller.py — Controller Layer
=================================================================
Sprint 2 — User Admin Profile Management

REFACTORED:
- Validation moved to Boundary (profile_management_routes.py)
- Alt flows moved to Entity (user_profile.py)
- Controller ONLY calls Entity methods and returns results
"""
from app.models.user_profile import UserProfile


class ProfileManagementController:

    @staticmethod
    def createProfile(data: dict):
        """UA-01 — Call Entity to create profile."""
        result = UserProfile.createIfNotExists({
            'profile_name': data['profile_name'],
            'description':  data.get('description', None),
        })
        if not result:
            return False, {'status': 'fail', 'error': f"Profile '{data['profile_name']}' already exists."}
        return True, {
            'status':  'success',
            'message': f"Profile '{data['profile_name']}' created successfully.",
        }

    @staticmethod
    def getAllProfiles():
        """UA-02 — Get all profiles."""
        profiles = UserProfile.getAll()
        return True, {
            'status':   'success',
            'message':  f'{len(profiles)} profile(s) found.',
            'profiles': profiles
        }

    @staticmethod
    def viewProfile(profile_id: int):
        """UA-02 — View one profile."""
        profile = UserProfile.findById(profile_id)
        if not profile:
            return False, {'status': 'fail', 'error': f'Profile with ID {profile_id} not found.'}
        return True, {'status': 'success', 'profile': profile}

    @staticmethod
    def updateProfile(profile_id: int, data: dict):
        """UA-03 — Call Entity to update profile."""
        result = UserProfile.updateIfExists(profile_id, data)
        if result == 'not_found':
            return False, {'status': 'fail', 'error': f'Profile with ID {profile_id} not found.'}
        if result == 'name_taken':
            return False, {'status': 'fail', 'error': f"Profile name '{data.get('profile_name')}' already exists."}
        return True, {'status': 'success', 'message': 'Profile updated successfully.'}

    @staticmethod
    def suspendProfile(profile_id: int):
        """UA-04 — Call Entity to suspend profile."""
        result = UserProfile.suspendIfAllowed(profile_id)
        if result == 'not_found':
            return False, {'status': 'fail', 'error': f'Profile with ID {profile_id} not found.'}
        if result == 'already_suspended':
            return False, {'status': 'fail', 'error': 'Profile is already suspended.'}
        if result == 'protected':
            return False, {'status': 'fail', 'error': 'Cannot suspend the admin profile.'}
        return True, {'status': 'success', 'message': 'Profile suspended. All associated accounts have been suspended.'}

    @staticmethod
    def activateProfile(profile_id: int):
        """UA-04 — Call Entity to activate profile."""
        result = UserProfile.activateIfAllowed(profile_id)
        if result == 'not_found':
            return False, {'status': 'fail', 'error': f'Profile with ID {profile_id} not found.'}
        if result == 'already_active':
            return False, {'status': 'fail', 'error': 'Profile is already active.'}
        return True, {'status': 'success', 'message': 'Profile reactivated. All associated accounts have been reactivated.'}

    @staticmethod
    def searchProfile(query: str):
        """UA-05 — Call Entity to search profiles."""
        profiles = UserProfile.searchProfiles(query.strip())
        if not profiles:
            return False, {'status': 'fail', 'error': f"No profiles found matching '{query}'."}
        return True, {
            'status':   'success',
            'message':  f'{len(profiles)} profile(s) found.',
            'profiles': profiles
        }