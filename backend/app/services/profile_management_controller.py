"""
app/services/profile_management_controller.py — Control Layer
=================================================================
Sprint 2 — User Admin Profile Management

Separate controller class per use case:
- CreateProfileController  (UA-01)
- ViewProfileController    (UA-02)
- UpdateProfileController  (UA-03)
- SuspendProfileController (UA-04)
- ActivateProfileController (UA-04)
- SearchProfileController  (UA-05)
"""
from app.models.user_profile import UserProfile


class CreateProfileController:
    """Control — CreateProfileController (UA-01)"""

    @staticmethod
    def createProfile(data: dict):
        result = UserProfile.create({
            'profile_name': data['profile_name'],
            'description':  data.get('description', None),
        })
        if not result:
            return False, {'status': 'fail', 'error': f"Profile '{data['profile_name']}' already exists."}
        return True, {
            'status':  'success',
            'message': f"Profile '{data['profile_name']}' created successfully.",
        }


class ViewProfileController:
    """Control — ViewProfileController (UA-02)"""

    @staticmethod
    def getAllProfiles():
        profiles = UserProfile.getAll()
        return True, {
            'status':   'success',
            'message':  f'{len(profiles)} profile(s) found.',
            'profiles': profiles
        }

    @staticmethod
    def viewProfile(profile_id: int):
        profile = UserProfile.findById(profile_id)
        if not profile:
            return False, {'status': 'fail', 'error': f'Profile with ID {profile_id} not found.'}
        return True, {'status': 'success', 'profile': profile}


class UpdateProfileController:
    """Control — UpdateProfileController (UA-03)"""

    @staticmethod
    def updateProfile(profile_id: int, data: dict):
        result = UserProfile.update(profile_id, data)
        if result == 'not_found':
            return False, {'status': 'fail', 'error': f'Profile with ID {profile_id} not found.'}
        if result == 'name_taken':
            return False, {'status': 'fail', 'error': f"Profile name '{data.get('profile_name')}' already exists."}
        return True, {'status': 'success', 'message': 'Profile updated successfully.'}


class SuspendProfileController:
    """Control — SuspendProfileController (UA-04)"""

    @staticmethod
    def suspendProfile(profile_id: int):
        result = UserProfile.suspend(profile_id)
        if result == 'not_found':
            return False, {'status': 'fail', 'error': f'Profile with ID {profile_id} not found.'}
        if result == 'already_suspended':
            return False, {'status': 'fail', 'error': 'Profile is already suspended.'}
        if result == 'protected':
            return False, {'status': 'fail', 'error': 'Cannot suspend the admin profile.'}
        return True, {'status': 'success', 'message': 'Profile suspended. All associated accounts have been suspended.'}


class ActivateProfileController:
    """Control — ActivateProfileController (UA-04)"""

    @staticmethod
    def activateProfile(profile_id: int):
        result = UserProfile.activate(profile_id)
        if result == 'not_found':
            return False, {'status': 'fail', 'error': f'Profile with ID {profile_id} not found.'}
        if result == 'already_active':
            return False, {'status': 'fail', 'error': 'Profile is already active.'}
        return True, {'status': 'success', 'message': 'Profile reactivated. All associated accounts have been reactivated.'}


class SearchProfileController:
    """Control — SearchProfileController (UA-05)"""

    @staticmethod
    def searchProfile(query: str):
        profiles = UserProfile.search(query.strip())
        if not profiles:
            return False, {'status': 'fail', 'error': f"No profiles found matching '{query}'."}
        return True, {
            'status':   'success',
            'message':  f'{len(profiles)} profile(s) found.',
            'profiles': profiles
        }


# Keep old name as alias for backward compatibility
class ProfileManagementController:
    createProfile  = CreateProfileController.createProfile
    getAllProfiles  = ViewProfileController.getAllProfiles
    viewProfile    = ViewProfileController.viewProfile
    updateProfile  = UpdateProfileController.updateProfile
    suspendProfile = SuspendProfileController.suspendProfile
    activateProfile= ActivateProfileController.activateProfile
    searchProfile  = SearchProfileController.searchProfile