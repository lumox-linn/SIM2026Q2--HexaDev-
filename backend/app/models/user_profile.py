"""
app/models/user_profile.py — Entity Layer
==========================================
Sprint 2 — User Profile Management

REFACTORED: Alt flows live here now.
Controller only calls these methods and reads the result.
"""
from app import mysql

PROTECTED_PROFILES = ['admin']


class UserProfile:

    # ── Alt flow methods ──────────────────────────────────────

    @staticmethod
    def createIfNotExists(data: dict):
        """
        Create a profile.
        Alt 1: Profile name already exists → return None
        Main: Create, return True
        """
        # Alt 1: Already exists
        if UserProfile.exists(data['profile_name']):
            return None

        UserProfile.createProfile(data)
        return True

    @staticmethod
    def updateIfExists(profile_id: int, data: dict):
        """
        Update a profile.
        Alt 1: Profile not found → return 'not_found'
        Alt 2: New name already taken → return 'name_taken'
        Main: Update, return True
        """
        # Alt 1: Not found
        profile = UserProfile.findById(profile_id)
        if not profile:
            return 'not_found'

        # Alt 2: Name already taken by another profile
        if data.get('profile_name') and data['profile_name'] != profile['profile_name']:
            if UserProfile.exists(data['profile_name']):
                return 'name_taken'

        UserProfile.updateProfile(profile_id, data)
        return True

    @staticmethod
    def suspendIfAllowed(profile_id: int):
        """
        Suspend a profile + all linked accounts.
        Alt 1: Profile not found → return 'not_found'
        Alt 2: Already suspended → return 'already_suspended'
        Alt 3: Protected profile → return 'protected'
        Main: Suspend, return True
        """
        profile = UserProfile.findById(profile_id)

        # Alt 1: Not found
        if not profile:
            return 'not_found'

        # Alt 2: Already suspended
        if profile['status'] == 'suspended':
            return 'already_suspended'

        # Alt 3: Cannot suspend protected profiles
        if profile['profile_name'] in PROTECTED_PROFILES:
            return 'protected'

        UserProfile.suspendProfile(profile_id)
        return True

    @staticmethod
    def activateIfAllowed(profile_id: int):
        """
        Activate a profile + all linked accounts.
        Alt 1: Profile not found → return 'not_found'
        Alt 2: Already active → return 'already_active'
        Main: Activate, return True
        """
        profile = UserProfile.findById(profile_id)

        # Alt 1: Not found
        if not profile:
            return 'not_found'

        # Alt 2: Already active
        if profile['status'] == 'active':
            return 'already_active'

        UserProfile.activateProfile(profile_id)
        return True

    # ── Pure SQL methods ──────────────────────────────────────

    @staticmethod
    def getAll():
        """SELECT all profiles."""
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM userprofile ORDER BY profile_id ASC")
        profiles = cursor.fetchall()
        cursor.close()
        return profiles

    @staticmethod
    def findById(profile_id: int):
        """SELECT profile by ID."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM userprofile WHERE profile_id = %s", (profile_id,)
        )
        profile = cursor.fetchone()
        cursor.close()
        return profile

    @staticmethod
    def findByName(profile_name: str):
        """SELECT profile by name."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM userprofile WHERE profile_name = %s", (profile_name,)
        )
        profile = cursor.fetchone()
        cursor.close()
        return profile

    @staticmethod
    def exists(profile_name: str) -> bool:
        """Check if profile name already exists."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT profile_id FROM userprofile WHERE profile_name = %s", (profile_name,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    @staticmethod
    def createProfile(data: dict) -> None:
        """INSERT new profile."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO userprofile (profile_name, status, description)
               VALUES (%s, 'active', %s)""",
            (data['profile_name'], data.get('description', None))
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def updateProfile(profile_id: int, data: dict) -> None:
        """UPDATE profile fields."""
        fields = []
        values = []

        if data.get('profile_name'):
            fields.append('profile_name = %s')
            values.append(data['profile_name'])
        if 'description' in data:
            fields.append('description = %s')
            values.append(data['description'])

        if not fields:
            return

        values.append(profile_id)
        cursor = mysql.connection.cursor()
        cursor.execute(
            f"UPDATE userprofile SET {', '.join(fields)} WHERE profile_id = %s",
            tuple(values)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def suspendProfile(profile_id: int) -> None:
        """SET profile status = suspended + suspend all linked accounts."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE userprofile SET status = 'suspended' WHERE profile_id = %s",
            (profile_id,)
        )
        cursor.execute(
            "UPDATE useraccount SET isActive = 0 WHERE profile_id = %s",
            (profile_id,)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def activateProfile(profile_id: int) -> None:
        """SET profile status = active + activate all linked accounts."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE userprofile SET status = 'active' WHERE profile_id = %s",
            (profile_id,)
        )
        cursor.execute(
            "UPDATE useraccount SET isActive = 1 WHERE profile_id = %s",
            (profile_id,)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def searchProfiles(query: str):
        """SEARCH profiles by name."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM userprofile WHERE profile_name LIKE %s ORDER BY profile_id ASC",
            (f"%{query}%",)
        )
        profiles = cursor.fetchall()
        cursor.close()
        return profiles