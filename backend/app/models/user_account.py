from app import mysql
from werkzeug.security import check_password_hash


class UserAccount:
    """
    Entity — maps to useraccount table.
    Sprint 1 + Sprint 2 methods.
    Note: userprofile JOIN queries are disabled until migration runs on Aiven.
    """

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
        return check_password_hash(password_hash, password)

    @staticmethod
    def isActive(account) -> bool:
        return bool(account['isActive'])

    @staticmethod
    def hasRole(account, role: str) -> bool:
        return account['role'] == role

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

    @staticmethod
    def findById(user_id: int):
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT user_id, username, isActive, role,
                      email, phone, dob, profile_picture, created_at
               FROM useraccount WHERE user_id = %s""",
            (user_id,)
        )
        account = cursor.fetchone()
        cursor.close()
        return account

    @staticmethod
    def getAll(role: str = None):
        cursor = mysql.connection.cursor()
        if role:
            cursor.execute(
                """SELECT user_id, username, isActive, role,
                          email, phone, dob, profile_picture, created_at
                   FROM useraccount WHERE role = %s
                   ORDER BY created_at DESC""",
                (role,)
            )
        else:
            cursor.execute(
                """SELECT user_id, username, isActive, role,
                          email, phone, dob, profile_picture, created_at
                   FROM useraccount ORDER BY created_at DESC"""
            )
        accounts = cursor.fetchall()
        cursor.close()
        return accounts

    @staticmethod
    def updateAccount(user_id: int, data: dict) -> None:
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
        cursor.execute(
            "UPDATE useraccount SET isActive = 0 WHERE user_id = %s", (user_id,)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def activateAccount(user_id: int) -> None:
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE useraccount SET isActive = 1 WHERE user_id = %s", (user_id,)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def searchAccounts(query: dict):
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
                FROM useraccount {where}
                ORDER BY created_at DESC""",
            tuple(values)
        )
        accounts = cursor.fetchall()
        cursor.close()
        return accounts