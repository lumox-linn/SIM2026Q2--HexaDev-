from app import mysql
from werkzeug.security import check_password_hash


class UserAccount:
    """
    Entity — maps to useraccount table.
    Includes login_status (online/offline) and access (active/suspended).
    """

    @staticmethod
    def findByUsername(username: str):
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
    def verifyPassword(password: str, password_hash: str) -> bool:
        return check_password_hash(password_hash, password)

    @staticmethod
    def isActive(account) -> bool:
        return bool(account['isActive'])

    @staticmethod
    def hasRole(account, role: str) -> bool:
        return account.get('role') == role or account.get('profile_name') == role

    @staticmethod
    def logout(accountId: str) -> None:
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
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT user_id FROM useraccount WHERE username = %s", (username,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    @staticmethod
    def createAccount(data: dict) -> None:
        from werkzeug.security import generate_password_hash
        from app.models.user_profile import UserProfile
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
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET profile_picture = %s WHERE user_id = %s",
            (filename, user_id)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def getProfilePicture(user_id: int):
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
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET email = %s WHERE user_id = %s",
            (email, user_id)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def updateDob(user_id: int, dob: str) -> None:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET dob = %s WHERE user_id = %s",
            (dob, user_id)
        )
        mysql.connection.commit()
        cursor.close()
 # ── Sprint 2 methods ────────────────────────────────────
    @staticmethod
    def findById(user_id: int):
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT ua.user_id, ua.username, ua.isActive, ua.role,
                      ua.email, ua.phone, ua.dob, ua.profile_picture,
                      ua.created_at, ua.profile_id,
                      up.profile_name, up.status as profile_status,
                      CASE WHEN s.session_id IS NOT NULL
                           THEN 'online' ELSE 'offline'
                      END as login_status,
                      CASE WHEN ua.isActive = 1
                           THEN 'active' ELSE 'suspended'
                      END as access
               FROM useraccount ua
               LEFT JOIN userprofile up ON ua.profile_id = up.profile_id
               LEFT JOIN usersession s ON ua.user_id = s.user_id
                  AND s.status = 'active' AND s.expires_at > NOW()
               WHERE ua.user_id = %s""",
            (user_id,)
        )
        account = cursor.fetchone()
        cursor.close()
        return account

    @staticmethod
    def getAll(role: str = None):
        """
        Get all accounts with login_status and access fields.
        login_status = online/offline (from usersession)
        access = active/suspended (from isActive)
        """
        cursor = mysql.connection.cursor()
        base_query = """SELECT ua.user_id, ua.username, ua.isActive, ua.role,
                          ua.email, ua.phone, ua.dob, ua.profile_picture,
                          ua.created_at, ua.profile_id,
                          up.profile_name, up.status as profile_status,
                          CASE WHEN s.session_id IS NOT NULL
                               THEN 'online' ELSE 'offline'
                          END as login_status,
                          CASE WHEN ua.isActive = 1
                               THEN 'active' ELSE 'suspended'
                          END as access
                   FROM useraccount ua
                   LEFT JOIN userprofile up ON ua.profile_id = up.profile_id
                   LEFT JOIN usersession s ON ua.user_id = s.user_id
                      AND s.status = 'active' AND s.expires_at > NOW()"""
        if role:
            cursor.execute(base_query + " WHERE ua.role = %s ORDER BY ua.created_at DESC", (role,))
        else:
            cursor.execute(base_query + " ORDER BY ua.created_at DESC")
        accounts = cursor.fetchall()
        cursor.close()
        return accounts

    @staticmethod
    def updateAccount(user_id: int, data: dict) -> None:
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
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE useraccount SET isActive = 0 WHERE user_id = %s", (user_id,))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def activateAccount(user_id: int) -> None:
        cursor = mysql.connection.cursor()
        cursor.execute("UPDATE useraccount SET isActive = 1 WHERE user_id = %s", (user_id,))
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def searchAccounts(query: dict):
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
                       up.profile_name, up.status as profile_status,
                       CASE WHEN s.session_id IS NOT NULL
                            THEN 'online' ELSE 'offline'
                       END as login_status,
                       CASE WHEN ua.isActive = 1
                            THEN 'active' ELSE 'suspended'
                       END as access
                FROM useraccount ua
                LEFT JOIN userprofile up ON ua.profile_id = up.profile_id
                LEFT JOIN usersession s ON ua.user_id = s.user_id
                   AND s.status = 'active' AND s.expires_at > NOW()
                {where}
                ORDER BY ua.created_at DESC""",
            tuple(values)
        )
        accounts = cursor.fetchall()
        cursor.close()
        return accounts