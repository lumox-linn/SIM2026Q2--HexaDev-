from app import mysql
import secrets
from datetime import datetime, timedelta


class UserSession:
    """
    Entity — maps to `usersession` table in csit314 database.
    Columns: session_id, user_id, token, login_time, logout_time, expires_at, status
    """

    SESSION_HOURS = 8

    @staticmethod
    def create(user_id: int) -> str:
        """
        Create a new session for user_id.
        Returns the generated token string.
        """
        token = secrets.token_hex(32)
        expires_at = datetime.now() + timedelta(hours=UserSession.SESSION_HOURS)
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO usersession (user_id, token, expires_at, status)
               VALUES (%s, %s, %s, 'active')""",
            (user_id, token, expires_at)
        )
        mysql.connection.commit()
        cursor.close()
        return token

    @staticmethod
    def findByToken(token: str):
        """Returns usersession row dict or None."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM usersession WHERE token = %s", (token,)
        )
        session = cursor.fetchone()
        cursor.close()
        return session

    @staticmethod
    def isValid(token: str) -> bool:
        """
        Returns True if token exists, status='active', and not expired.
        Auto-expires token in DB if past expires_at.
        """
        session = UserSession.findByToken(token)
        if not session:
            return False
        if session['status'] != 'active':
            return False
        if datetime.now() > session['expires_at']:
            UserSession.expire(token)
            return False
        return True

    @staticmethod
    def expire(token: str) -> None:
        """Mark a single session as expired (token-based logout or expiry)."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            """UPDATE usersession
               SET status = 'expired', logout_time = NOW()
               WHERE token = %s""",
            (token,)
        )
        mysql.connection.commit()
        cursor.close()
