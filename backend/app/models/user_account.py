"""
app/models/user_account.py — Entity Layer
==========================================
Sprint 1 + Sprint 2 — UserAccount Entity

REFACTORED:
- Merged createIfNotExists() + createAccount() → create()
- Merged updateIfExists() + updateAccount() → update()
- Merged suspendIfAllowed() + suspendAccount() → suspend()
- Merged activateIfAllowed() + activateAccount() → activate()
- Merged deleteIfAllowed() + deleteAccount() → delete()
- All alt flows and SQL in same method
"""
from app import mysql
from werkzeug.security import check_password_hash, generate_password_hash


class UserAccount:
    """
    Entity — maps to useraccount table.
    All SQL queries and alternative flows live here.
    """

    # ── Login ─────────────────────────────────────────────────

    @staticmethod
    def login(username: str, password: str):
        """
        Find account and verify credentials.
        Alt 1: Account not found → return None
        Alt 2: Password incorrect → return None
        Alt 3: Account suspended → return None
        Main: Return account dict
        """
        account = UserAccount.findByUsername(username)

        if not account:                                          # Alt 1
            return None
        if not check_password_hash(account['password_hash'], password):  # Alt 2
            return None
        if not account['isActive']:                              # Alt 3
            return None

        return account

    # ── Create ────────────────────────────────────────────────

    @staticmethod
    def create(data: dict):
        """
        Create a new user account.
        Alt 1: Username already exists → return None
        Main: INSERT into DB, return True
        """
        from app.models.user_profile import UserProfile

        if UserAccount.findByUsername(data['username']):         # Alt 1
            return None

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
        return True

    # ── Update ────────────────────────────────────────────────

    @staticmethod
    def update(user_id: int, data: dict):
        """
        Update a user account.
        Alt 1: Account not found → return None
        Main: UPDATE in DB, return True
        """
        from app.models.user_profile import UserProfile

        if not UserAccount.findById(user_id):                   # Alt 1
            return None

        fields = []
        values = []

        if data.get('email') is not None:
            fields.append('email = %s')
            values.append(data['email'])
        if data.get('phone') is not None:
            fields.append('phone = %s')
            values.append(data['phone'])
        if data.get('dob') is not None:
            fields.append('dob = %s')
            values.append(data['dob'])
        if data.get('role') is not None:
            fields.append('role = %s')
            values.append(data['role'])
            profile = UserProfile.findByName(data['role'])
            if profile:
                fields.append('profile_id = %s')
                values.append(profile['profile_id'])
        if data.get('password'):
            fields.append('password_hash = %s')
            values.append(generate_password_hash(data['password']))

        if not fields:
            return True

        values.append(user_id)
        cursor = mysql.connection.cursor()
        cursor.execute(
            f"UPDATE useraccount SET {', '.join(fields)} WHERE user_id = %s",
            tuple(values)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Suspend ───────────────────────────────────────────────

    @staticmethod
    def suspend(user_id: int):
        """
        Suspend a user account.
        Alt 1: Account not found → return 'not_found'
        Alt 2: Already suspended → return 'already_suspended'
        Alt 3: Is admin → return 'is_admin'
        Main: UPDATE isActive=0, return True
        """
        account = UserAccount.findById(user_id)

        if not account:                                          # Alt 1
            return 'not_found'
        if account['isActive'] == 0:                            # Alt 2
            return 'already_suspended'
        if account['role'] == 'admin':                          # Alt 3
            return 'is_admin'

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET isActive = 0 WHERE user_id = %s", (user_id,)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Activate ──────────────────────────────────────────────

    @staticmethod
    def activate(user_id: int):
        """
        Activate a user account.
        Alt 1: Account not found → return 'not_found'
        Alt 2: Already active → return 'already_active'
        Main: UPDATE isActive=1, return True
        """
        account = UserAccount.findById(user_id)

        if not account:                                          # Alt 1
            return 'not_found'
        if account['isActive'] == 1:                            # Alt 2
            return 'already_active'

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET isActive = 1 WHERE user_id = %s", (user_id,)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Delete ────────────────────────────────────────────────

    @staticmethod
    def delete(user_id: int):
        """
        Delete a user account.
        Alt 1: Account not found → return 'not_found'
        Alt 2: Is admin → return 'is_admin'
        Main: DELETE from DB, return True
        """
        account = UserAccount.findById(user_id)

        if not account:                                          # Alt 1
            return 'not_found'
        if account['role'] == 'admin':                          # Alt 2
            return 'is_admin'

        cursor = mysql.connection.cursor()
        cursor.execute(
            "DELETE FROM useraccount WHERE user_id = %s", (user_id,)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Search ────────────────────────────────────────────────

    @staticmethod
    def search(query: dict):
        """Search accounts by username and/or role."""
        conditions = []
        values = []

        if query.get('username'):
            conditions.append('ua.username LIKE %s')
            values.append(f"%{query['username']}%")
        if query.get('role'):
            conditions.append('ua.role = %s')
            values.append(query['role'])

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        cursor = mysql.connection.cursor()
        cursor.execute(
            f"""SELECT ua.user_id, ua.username, ua.password_hash, ua.isActive, ua.role,
                       ua.email, ua.phone, ua.dob, ua.profile_picture,
                       ua.created_at, ua.profile_id,
                       up.profile_name, up.status as profile_status,
                       CASE WHEN ua.isActive = 1 THEN 'active' ELSE 'suspended' END as access
                FROM useraccount ua
                LEFT JOIN userprofile up ON ua.profile_id = up.profile_id
                {where}
                GROUP BY ua.user_id
                ORDER BY ua.created_at DESC""",
            tuple(values)
        )
        accounts = cursor.fetchall()
        cursor.close()
        return accounts

    # ── Pure SQL read methods ─────────────────────────────────

    @staticmethod
    def findByUsername(username: str):
        """SELECT account by username."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT ua.*, up.profile_name, up.status as profile_status
               FROM useraccount ua
               LEFT JOIN userprofile up ON ua.profile_id = up.profile_id
               WHERE ua.username = %s""",
            (username,)
        )
        account = cursor.fetchone()
        cursor.close()
        return account

    @staticmethod
    def findById(user_id: int):
        """SELECT account by user_id."""
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
        """Get all accounts, optionally filtered by role."""
        cursor = mysql.connection.cursor()
        if role:
            cursor.execute(
                """SELECT ua.user_id, ua.username, ua.password_hash, ua.isActive, ua.role,
                          ua.email, ua.phone, ua.dob, ua.profile_picture,
                          ua.created_at, ua.profile_id,
                          up.profile_name, up.status as profile_status,
                          CASE WHEN ua.isActive = 1 THEN 'active' ELSE 'suspended' END as access
                   FROM useraccount ua
                   LEFT JOIN userprofile up ON ua.profile_id = up.profile_id
                   WHERE ua.role = %s
                   GROUP BY ua.user_id
                   ORDER BY ua.created_at DESC""",
                (role,)
            )
        else:
            cursor.execute(
                """SELECT ua.user_id, ua.username, ua.password_hash, ua.isActive, ua.role,
                          ua.email, ua.phone, ua.dob, ua.profile_picture,
                          ua.created_at, ua.profile_id,
                          up.profile_name, up.status as profile_status,
                          CASE WHEN ua.isActive = 1 THEN 'active' ELSE 'suspended' END as access
                   FROM useraccount ua
                   LEFT JOIN userprofile up ON ua.profile_id = up.profile_id
                   GROUP BY ua.user_id
                   ORDER BY ua.created_at DESC"""
            )
        accounts = cursor.fetchall()
        cursor.close()
        return accounts

    @staticmethod
    def getProfilePicture(user_id: int):
        """Return profile_picture filename or None."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT profile_picture FROM useraccount WHERE user_id = %s", (user_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        return row['profile_picture'] if row else None

    @staticmethod
    def updateProfilePicture(user_id: int, filename: str) -> None:
        """UPDATE profile_picture filename."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET profile_picture = %s WHERE user_id = %s",
            (filename, user_id)
        )
        mysql.connection.commit()
        cursor.close()