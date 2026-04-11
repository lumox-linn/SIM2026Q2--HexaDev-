from app import mysql
from werkzeug.security import check_password_hash


class UserAccount:
    """
    Entity — maps to `useraccount` table in csit314 database.
    Columns: user_id, username, password_hash, isActive, role, created_at
    BCE diagram methods: findByUsername, verifyPassword, isActive, hasRole, logout
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
        """
        Expire all active sessions for this user_id.
        Sets status='expired' and logout_time=NOW().
        """
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
    def getAll():
        """Return all accounts without password_hash (admin Sprint 2)."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT user_id, username, isActive, role, created_at FROM useraccount"
        )
        accounts = cursor.fetchall()
        cursor.close()
        return accounts

    @staticmethod
    def findById(user_id: int):
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT user_id, username, isActive, role, created_at FROM useraccount WHERE user_id = %s",
            (user_id,)
        )
        account = cursor.fetchone()
        cursor.close()
        return account

    @staticmethod
    def exists(username: str) -> bool:
        """
        Check if a username already exists in useraccount table.
        Maps to UserAccount.exists(username: String): boolean in BCE diagram.
        Returns True if username is taken.
        """
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
        Maps to UserAccount.createAccount(data): void in BCE diagram.
        data keys: username, password_hash, role, isActive (default 1)
        """
        from werkzeug.security import generate_password_hash
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO useraccount (username, password_hash, isActive, role)
               VALUES (%s, %s, %s, %s)""",
            (
                data['username'],
                generate_password_hash(data['password']),
                data.get('isActive', 1),
                data['role'],
            )
        )
        mysql.connection.commit()
        cursor.close()
