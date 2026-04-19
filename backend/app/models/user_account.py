from app import mysql
from werkzeug.security import check_password_hash


class UserAccount:
    """
    Entity — maps to `useraccount` table in csit314 database.
    Sprint 1: findByUsername, verifyPassword, isActive, hasRole,
              logout, exists, createAccount, updateProfilePicture,
              getProfilePicture, updateEmail, updateDob
    Sprint 2: findById, getAll, updateAccount, suspendAccount,
              activateAccount, searchAccounts
    """

    # ── Sprint 1 methods ─────────────────────────────────────

    @staticmethod
    def findByUsername(username: str):
        """Returns useraccount row dict or None."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM useraccount WHERE username = %s", (username,)
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
        return account['role'] == role

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
        """Insert a new useraccount row."""
        from werkzeug.security import generate_password_hash
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO useraccount
               (username, password_hash, isActive, role, email, phone, dob)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (
                data['username'],
                generate_password_hash(data['password']),
                data.get('isActive', 1),
                data['role'],
                data.get('email', None),
                data.get('phone', None),
                data.get('dob', None),
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
        SELECT a user by user_id.
        Returns all fields except password_hash.
        Used by: viewAccount, updateAccount, suspendAccount
        SQL: SELECT * FROM useraccount WHERE user_id = ?
        """
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT user_id, username, isActive, role,
                      email, phone, dob, profile_picture, created_at
               FROM useraccount
               WHERE user_id = %s""",
            (user_id,)
        )
        account = cursor.fetchone()
        cursor.close()
        return account

    @staticmethod
    def getAll(role: str = None):
        """
        SELECT all users — optionally filtered by role.
        Never returns password_hash.
        Used by: getAllAccounts (UA-07 view all)
        SQL: SELECT * FROM useraccount [WHERE role = ?]
        """
        cursor = mysql.connection.cursor()
        if role:
            cursor.execute(
                """SELECT user_id, username, isActive, role,
                          email, phone, dob, profile_picture, created_at
                   FROM useraccount
                   WHERE role = %s
                   ORDER BY created_at DESC""",
                (role,)
            )
        else:
            cursor.execute(
                """SELECT user_id, username, isActive, role,
                          email, phone, dob, profile_picture, created_at
                   FROM useraccount
                   ORDER BY created_at DESC"""
            )
        accounts = cursor.fetchall()
        cursor.close()
        return accounts

    @staticmethod
    def updateAccount(user_id: int, data: dict) -> None:
        """
        UPDATE user account fields.
        Only updates fields that are provided in data.
        Used by: updateAccount (UA-08)
        SQL: UPDATE useraccount SET ... WHERE user_id = ?
        """
        from werkzeug.security import generate_password_hash

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

        if 'password' in data and data['password']:
            fields.append('password_hash = %s')
            values.append(generate_password_hash(data['password']))

        if not fields:
            return  # nothing to update

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
        """
        Set isActive = 0 for a user account.
        Used by: suspendAccount (UA-09)
        SQL: UPDATE useraccount SET isActive = 0 WHERE user_id = ?
        """
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET isActive = 0 WHERE user_id = %s",
            (user_id,)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def activateAccount(user_id: int) -> None:
        """
        Set isActive = 1 for a suspended user account.
        Used by: activateAccount (reactivate)
        SQL: UPDATE useraccount SET isActive = 1 WHERE user_id = ?
        """
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET isActive = 1 WHERE user_id = %s",
            (user_id,)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def searchAccounts(query: dict):
        """
        Search accounts by username and/or role.
        Used by: searchAccount (UA-10)
        SQL: SELECT * FROM useraccount WHERE username LIKE ? [AND role = ?]
        """
        conditions = []
        values = []

        if query.get('username'):
            conditions.append('username LIKE %s')
            values.append(f"%{query['username']}%")

        if query.get('role'):
            conditions.append('role = %s')
            values.append(query['role'])

        if query.get('isActive') is not None:
            conditions.append('isActive = %s')
            values.append(query['isActive'])

        where = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        cursor = mysql.connection.cursor()
        cursor.execute(
            f"""SELECT user_id, username, isActive, role,
                       email, phone, dob, profile_picture, created_at
                FROM useraccount
                {where}
                ORDER BY created_at DESC""",
            tuple(values)
        )
        accounts = cursor.fetchall()
        cursor.close()
        return accounts