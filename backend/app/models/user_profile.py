"""
app/models/user_profile.py — Entity Layer
==========================================
Sprint 2 — User Profile Management

REFACTORED:
- Merged createIfNotExists() + createProfile() → create()
- Merged updateIfExists() + updateProfile() → update()
- Merged suspendIfAllowed() + suspendProfile() → suspend()
- Merged activateIfAllowed() + activateProfile() → activate()
- All alt flows and SQL in same method
"""
from app import mysql

PROTECTED_PROFILES = ['admin']


class UserProfile:

    # ── Create ────────────────────────────────────────────────

    @staticmethod
    def create(data: dict):
        """
        Create a profile.
        Alt 1: Profile name already exists → return None
        Main: INSERT into DB, return True
        """
        if UserProfile.exists(data['profile_name']):            # Alt 1
            return None

        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO userprofile (profile_name, status, description)
               VALUES (%s, 'active', %s)""",
            (data['profile_name'], data.get('description', None))
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Update ────────────────────────────────────────────────

    @staticmethod
    def update(profile_id: int, data: dict):
        """
        Update a profile.
        Alt 1: Profile not found → return 'not_found'
        Alt 2: New name already taken → return 'name_taken'
        Main: UPDATE in DB, return True
        """
        profile = UserProfile.findById(profile_id)

        if not profile:                                          # Alt 1
            return 'not_found'

        if data.get('profile_name') and data['profile_name'] != profile['profile_name']:
            if UserProfile.exists(data['profile_name']):        # Alt 2
                return 'name_taken'

        fields = []
        values = []

        if data.get('profile_name'):
            fields.append('profile_name = %s')
            values.append(data['profile_name'])
        if 'description' in data:
            fields.append('description = %s')
            values.append(data['description'])

        if not fields:
            return True

        values.append(profile_id)
        cursor = mysql.connection.cursor()
        cursor.execute(
            f"UPDATE userprofile SET {', '.join(fields)} WHERE profile_id = %s",
            tuple(values)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Suspend ───────────────────────────────────────────────

    @staticmethod
    def suspend(profile_id: int):
        """
        Suspend a profile + all linked accounts.
        Alt 1: Profile not found → return 'not_found'
        Alt 2: Already suspended → return 'already_suspended'
        Alt 3: Protected profile → return 'protected'
        Main: UPDATE status=suspended, return True
        """
        profile = UserProfile.findById(profile_id)

        if not profile:                                          # Alt 1
            return 'not_found'
        if profile['status'] == 'suspended':                    # Alt 2
            return 'already_suspended'
        if profile['profile_name'] in PROTECTED_PROFILES:       # Alt 3
            return 'protected'

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
        return True

    # ── Activate ──────────────────────────────────────────────

    @staticmethod
    def activate(profile_id: int):
        """
        Activate a profile + all linked accounts.
        Alt 1: Profile not found → return 'not_found'
        Alt 2: Already active → return 'already_active'
        Main: UPDATE status=active, return True
        """
        profile = UserProfile.findById(profile_id)

        if not profile:                                          # Alt 1
            return 'not_found'
        if profile['status'] == 'active':                       # Alt 2
            return 'already_active'

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
        return True

    # ── Search ────────────────────────────────────────────────

    @staticmethod
    def search(query: str):
        """SEARCH profiles by name."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM userprofile WHERE profile_name LIKE %s ORDER BY profile_id ASC",
            (f"%{query}%",)
        )
        profiles = cursor.fetchall()
        cursor.close()
        return profiles

    # ── Pure SQL read methods ─────────────────────────────────

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