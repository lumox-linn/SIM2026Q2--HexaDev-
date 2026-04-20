"""
app/services/profile_management_controller.py — Controller Layer
=================================================================
Sprint 2 — User Admin Profile Management

Handles business logic for:
  UA-01 — Create user profile
  UA-02 — View user profile
  UA-03 — Update user profile
  UA-04 — Suspend user profile
  UA-05 — Search user profile
"""
from app.models.user_profile import UserProfile

PROTECTED_PROFILES = ['admin']  # Cannot suspend admin profile


class ProfileManagementController:

    # ── UA-01: Create profile ─────────────────────────────────

    @staticmethod
    def createProfile(data: dict):
        """
        Create a new user profile (role type).

        Alt 1: Missing profile name → fail
        Alt 2: Profile name already exists → fail
        Main:  Create profile → success
        """
        profile_name = data.get('profile_name', '').strip()

        # Alt 1: Missing name
        if not profile_name:
            return False, {'status': 'fail', 'error': 'Profile name is required.'}

        if len(profile_name) < 3:
            return False, {'status': 'fail', 'error': 'Profile name must be at least 3 characters.'}

        # Alt 2: Already exists
        if UserProfile.exists(profile_name):
            return False, {'status': 'fail', 'error': f"Profile '{profile_name}' already exists."}

        # Main flow: create
        UserProfile.createProfile({
            'profile_name': profile_name,
            'description':  data.get('description', None),
        })

        return True, {
            'status':  'success',
            'message': f"Profile '{profile_name}' created successfully.",
        }

    # ── UA-02: View all profiles ──────────────────────────────

    @staticmethod
    def getAllProfiles():
        """Get all profiles."""
        profiles = UserProfile.getAll()
        return True, {
            'status':   'success',
            'message':  f'{len(profiles)} profile(s) found.',
            'profiles': profiles
        }

    # ── UA-02: View one profile ───────────────────────────────

    @staticmethod
    def viewProfile(profile_id: int):
        """
        View a single profile by ID.

        Alt 1: Profile not found → fail
        Main:  Return profile → success
        """
        profile = UserProfile.findById(profile_id)
        if not profile:
            return False, {
                'status': 'fail',
                'error':  f'Profile with ID {profile_id} not found.'
            }

        return True, {
            'status':  'success',
            'profile': profile
        }

    # ── UA-03: Update profile ─────────────────────────────────

    @staticmethod
    def updateProfile(profile_id: int, data: dict):
        """
        Update a profile's details.

        Alt 1: Profile not found → fail
        Alt 2: New name already taken → fail
        Main:  Update → success
        """
        # Alt 1: Not found
        profile = UserProfile.findById(profile_id)
        if not profile:
            return False, {
                'status': 'fail',
                'error':  f'Profile with ID {profile_id} not found.'
            }

        # Alt 2: Name already taken
        if 'profile_name' in data and data['profile_name']:
            if data['profile_name'] != profile['profile_name']:
                if UserProfile.exists(data['profile_name']):
                    return False, {
                        'status': 'fail',
                        'error':  f"Profile name '{data['profile_name']}' already exists."
                    }

        # Main flow: update
        UserProfile.updateProfile(profile_id, data)

        return True, {
            'status':  'success',
            'message': f"Profile '{profile['profile_name']}' updated successfully.",
        }

    # ── UA-04: Suspend profile ────────────────────────────────

    @staticmethod
    def suspendProfile(profile_id: int):
        """
        Suspend a profile — also suspends all accounts with this profile.

        Alt 1: Profile not found → fail
        Alt 2: Already suspended → fail
        Alt 3: Cannot suspend protected profile (admin) → fail
        Main:  Suspend profile + all accounts → success
        """
        # Alt 1: Not found
        profile = UserProfile.findById(profile_id)
        if not profile:
            return False, {
                'status': 'fail',
                'error':  f'Profile with ID {profile_id} not found.'
            }

        # Alt 2: Already suspended
        if profile['status'] == 'suspended':
            return False, {
                'status': 'fail',
                'error':  f"Profile '{profile['profile_name']}' is already suspended."
            }

        # Alt 3: Cannot suspend protected profiles
        if profile['profile_name'] in PROTECTED_PROFILES:
            return False, {
                'status': 'fail',
                'error':  f"Cannot suspend the '{profile['profile_name']}' profile."
            }

        # Main flow: suspend profile + all accounts
        UserProfile.suspendProfile(profile_id)

        return True, {
            'status':  'success',
            'message': f"Profile '{profile['profile_name']}' suspended. All associated accounts have been suspended.",
        }

    # ── UA-04: Activate profile ───────────────────────────────

    @staticmethod
    def activateProfile(profile_id: int):
        """
        Reactivate a suspended profile.

        Alt 1: Profile not found → fail
        Alt 2: Already active → fail
        Main:  Activate profile + all accounts → success
        """
        # Alt 1: Not found
        profile = UserProfile.findById(profile_id)
        if not profile:
            return False, {
                'status': 'fail',
                'error':  f'Profile with ID {profile_id} not found.'
            }

        # Alt 2: Already active
        if profile['status'] == 'active':
            return False, {
                'status': 'fail',
                'error':  f"Profile '{profile['profile_name']}' is already active."
            }

        # Main flow: activate profile + all accounts
        UserProfile.activateProfile(profile_id)

        return True, {
            'status':  'success',
            'message': f"Profile '{profile['profile_name']}' reactivated. All associated accounts have been reactivated.",
        }

    # ── UA-05: Search profiles ────────────────────────────────

    @staticmethod
    def searchProfile(query: str):
        """
        Search profiles by name.

        Alt 1: No results → fail
        Main:  Return matching profiles → success
        """
        if not query or not query.strip():
            return False, {'status': 'fail', 'error': 'Search query is required.'}

        profiles = UserProfile.searchProfiles(query.strip())

        if not profiles:
            return False, {
                'status': 'fail',
                'error':  f"No profiles found matching '{query}'."
            }

        return True, {
            'status':   'success',
            'message':  f'{len(profiles)} profile(s) found.',
            'profiles': profiles
        }
