"""
app/models/user_account.py — Entity Layer
==========================================
Updated for Sprint 2 — now links to userprofile table via profile_id FK.

useraccount now has:
  - role (ENUM) — kept for backward compatibility
  - profile_id (FK) — links to userprofile table
"""
from app import mysql
from werkzeug.security import check_password_hash


class UserAccount:

    # ── Sprint 1 methods ─────────────────────────────────────

    @staticmethod
    def findByUsername(username: str):
        """
        Find account by username.
        Returns account row dict or None.
        """
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM useraccount WHERE username = %s",
            (username,)
        )
        account = cursor.fetchone()
        cursor.close()
        return account

    @staticmethod
    def verifyPassword(password: str, password_hash: str) -> bool:
        """Verify plain password against stored hash."""
        return check_password_hash(password_hash, password)

    @staticmethod
    def isActive(account) -> bool:
        """Returns True if isActive = 1."""
        return bool(account['isActive'])

    @staticmethod
    def hasRole(account, role: str) -> bool:
        """Returns True if account role matches given role."""
        return account.get('role') == role or account.get('profile_name') == role

    @staticmethod
    def logout(accountId: str) -> None:
        """Expire all active sessions for this user_id."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            """UPDATE usersession
               SET status = 'expired', logout_time = NOW()
               WHERE user_id = %s AND status = 'active'""",
            (accountId,)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def exists(username: str) -> bool:
        """Check if a username already exists."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT user_id FROM useraccount WHERE username = %s", (username,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    @staticmethod
    def createAccount(data: dict) -> None:
        """
        Insert a new useraccount row.
        Now also sets profile_id from userprofile table.
        """
        from werkzeug.security import generate_password_hash
        from app.models.user_profile import UserProfile

        # Get profile_id from profile_name
        profile = UserProfile.findByName(data['role'])
        profile_id = profile['profile_id'] if profile else None

        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO useraccount
               (username, password_hash, isActive, role, email, phone, dob, profile_id)
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
            (
                data['username'],
                generate_password_hash(data['password']),
                data.get('isActive', 1),
                data['role'],
                data.get('email', None),
                data.get('phone', None),
                data.get('dob', None),
                profile_id,
            )
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def updateProfilePicture(user_id: int, filename: str) -> None:
        """Store uploaded image filename for a user."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET profile_picture = %s WHERE user_id = %s",
            (filename, user_id)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def getProfilePicture(user_id: int):
        """Return profile_picture filename for a user, or None."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT profile_picture FROM useraccount WHERE user_id = %s",
            (user_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        return row['profile_picture'] if row else None

    @staticmethod
    def updateEmail(user_id: int, email: str) -> None:
        """Update email for a user account."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET email = %s WHERE user_id = %s",
            (email, user_id)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def updateDob(user_id: int, dob: str) -> None:
        """Update date of birth for a user account."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET dob = %s WHERE user_id = %s",
            (dob, user_id)
        )
        mysql.connection.commit()
        cursor.close()

    # ── Sprint 2 methods ─────────────────────────────────────

    @staticmethod
    def findById(user_id: int):
        """
        Find account by user_id — joins with userprofile.
        Never returns password_hash.
        """
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT ua.user_id, ua.username, ua.isActive, ua.role,
                      ua.email, ua.phone, ua.dob, ua.profile_picture,
                      ua.created_at, ua.profile_id,
                      up.profile_name, up.status as profile_status
               FROM useraccount ua
               LEFT JOIN userprofile up ON ua.profile_id = up.profile_id
               WHERE ua.user_id = %s""",
            (user_id,)
        )
        account = cursor.fetchone()
        cursor.close()
        return account

    @staticmethod
    def getAll(role: str = None):
        """
        Get all accounts — joins with userprofile.
        Never returns password_hash.
        Optionally filter by role.
        """
        cursor = mysql.connection.cursor()
        if role:
            cursor.execute(
                """SELECT ua.user_id, ua.username, ua.isActive, ua.role,
                          ua.email, ua.phone, ua.dob, ua.profile_picture,
                          ua.created_at, ua.profile_id,
                          up.profile_name, up.status as profile_status
                   FROM useraccount ua
                   LEFT JOIN userprofile up ON ua.profile_id = up.profile_id
                   WHERE ua.role = %s
                   ORDER BY ua.created_at DESC""",
                (role,)
            )
        else:
            cursor.execute(
                """SELECT ua.user_id, ua.username, ua.isActive, ua.role,
                          ua.email, ua.phone, ua.dob, ua.profile_picture,
                          ua.created_at, ua.profile_id,
                          up.profile_name, up.status as profile_status
                   FROM useraccount ua
                   LEFT JOIN userprofile up ON ua.profile_id = up.profile_id
                   ORDER BY ua.created_at DESC"""
            )
        accounts = cursor.fetchall()
        cursor.close()
        return accounts

    @staticmethod
    def updateAccount(user_id: int, data: dict) -> None:
        """Update user account fields."""
        from werkzeug.security import generate_password_hash
        from app.models.user_profile import UserProfile

        fields = []
        values = []

        if 'email' in data and data['email'] is not None:
            fields.append('email = %s')
            values.append(data['email'])

        if 'phone' in data and data['phone'] is not None:
            fields.append('phone = %s')
            values.append(data['phone'])

        if 'dob' in data and data['dob'] is not None:
            fields.append('dob = %s')
            values.append(data['dob'])

        if 'role' in data and data['role'] is not None:
            fields.append('role = %s')
            values.append(data['role'])
            # Also update profile_id
            profile = UserProfile.findByName(data['role'])
            if profile:
                fields.append('profile_id = %s')
                values.append(profile['profile_id'])

        if 'password' in data and data['password']:
            fields.append('password_hash = %s')
            values.append(generate_password_hash(data['password']))

        if not fields:
            return

        values.append(user_id)
        cursor = mysql.connection.cursor()
        cursor.execute(
            f"UPDATE useraccount SET {', '.join(fields)} WHERE user_id = %s",
            tuple(values)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def suspendAccount(user_id: int) -> None:
        """Set isActive = 0 for a user account."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET isActive = 0 WHERE user_id = %s",
            (user_id,)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def activateAccount(user_id: int) -> None:
        """Set isActive = 1 for a suspended user account."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET isActive = 1 WHERE user_id = %s",
            (user_id,)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def searchAccounts(query: dict):
        """Search accounts by username and/or role."""
        conditions = []
        values = []

        if query.get('username'):
            conditions.append('ua.username LIKE %s')
            values.append(f"%{query['username']}%")

        if query.get('role'):
            conditions.append('ua.role = %s')
            values.append(query['role'])

        if query.get('isActive') is not None:
            conditions.append('ua.isActive = %s')
            values.append(query['isActive'])

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        cursor = mysql.connection.cursor()
        cursor.execute(
            f"""SELECT ua.user_id, ua.username, ua.isActive, ua.role,
                       ua.email, ua.phone, ua.dob, ua.profile_picture,
                       ua.created_at, ua.profile_id,
                       up.profile_name, up.status as profile_status
                FROM useraccount ua
                LEFT JOIN userprofile up ON ua.profile_id = up.profile_id
                {where}
                ORDER BY ua.created_at DESC""",
            tuple(values)
        )
        accounts = cursor.fetchall()
        cursor.close()
        return accounts