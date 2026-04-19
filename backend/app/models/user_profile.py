"""
app/models/user_profile.py — Entity Layer
==========================================
Sprint 2 — User Profile Management

Represents the userprofile table in MySQL.
A profile = a role type in the system.

Database table: userprofile
+------------+------------------+--------+---------------------+
| profile_id | profile_name     | status | description         |
+------------+------------------+--------+---------------------+
|     1      | admin            | active | System administrator|
|     2      | fund_raiser      | active | Creates campaigns   |
|     3      | donee            | active | Donates to campaigns|
|     4      | platform_manager | active | Manages categories  |
+------------+------------------+--------+---------------------+

When a profile is suspended:
  - No new accounts can be assigned that profile
  - Existing accounts with that profile are also suspended (isActive=0)
"""
from app import mysql


class UserProfile:

    @staticmethod
    def getAll():
        """
        Get all profiles.
        Used by: getAllProfiles (UA-02 view all)
        """
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM userprofile ORDER BY profile_id ASC"
        )
        profiles = cursor.fetchall()
        cursor.close()
        return profiles

    @staticmethod
    def findById(profile_id: int):
        """
        Find a profile by ID.
        Used by: viewProfile (UA-02)
        """
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM userprofile WHERE profile_id = %s",
            (profile_id,)
        )
        profile = cursor.fetchone()
        cursor.close()
        return profile

    @staticmethod
    def findByName(profile_name: str):
        """
        Find a profile by name.
        Used by: login, register to get profile_id
        """
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM userprofile WHERE profile_name = %s",
            (profile_name,)
        )
        profile = cursor.fetchone()
        cursor.close()
        return profile

    @staticmethod
    def exists(profile_name: str) -> bool:
        """
        Check if a profile name already exists.
        Used by: createProfile (UA-01)
        """
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT profile_id FROM userprofile WHERE profile_name = %s",
            (profile_name,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    @staticmethod
    def createProfile(data: dict) -> None:
        """
        Insert a new profile into userprofile table.
        Used by: createProfile (UA-01)
        SQL: INSERT INTO userprofile (profile_name, description) VALUES (...)
        """
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO userprofile (profile_name, status, description)
               VALUES (%s, 'active', %s)""",
            (
                data['profile_name'],
                data.get('description', None),
            )
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def updateProfile(profile_id: int, data: dict) -> None:
        """
        Update profile details.
        Used by: updateProfile (UA-03)
        SQL: UPDATE userprofile SET ... WHERE profile_id = ?
        """
        fields = []
        values = []

        if 'profile_name' in data and data['profile_name']:
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
        """
        Suspend a profile — set status = 'suspended'.
        Also suspends all accounts with this profile (isActive = 0).
        Used by: suspendProfile (UA-04)
        """
        cursor = mysql.connection.cursor()

        # Suspend the profile
        cursor.execute(
            "UPDATE userprofile SET status = 'suspended' WHERE profile_id = %s",
            (profile_id,)
        )

        # Also suspend all accounts with this profile
        cursor.execute(
            "UPDATE useraccount SET isActive = 0 WHERE profile_id = %s",
            (profile_id,)
        )

        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def activateProfile(profile_id: int) -> None:
        """
        Reactivate a suspended profile — set status = 'active'.
        Also reactivates all accounts with this profile (isActive = 1).
        """
        cursor = mysql.connection.cursor()

        # Activate the profile
        cursor.execute(
            "UPDATE userprofile SET status = 'active' WHERE profile_id = %s",
            (profile_id,)
        )

        # Also reactivate all accounts with this profile
        cursor.execute(
            "UPDATE useraccount SET isActive = 1 WHERE profile_id = %s",
            (profile_id,)
        )

        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def searchProfiles(query: str):
        """
        Search profiles by name.
        Used by: searchProfile (UA-05)
        SQL: SELECT * FROM userprofile WHERE profile_name LIKE ?
        """
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM userprofile WHERE profile_name LIKE %s ORDER BY profile_id ASC",
            (f"%{query}%",)
        )
        profiles = cursor.fetchall()
        cursor.close()
        return profiles
