"""
app/models/favourite.py — Entity Layer
=======================================
Sprint 5 — DN-03 to DN-05: Donee Favourites

Entity: maps to favourite table.
All SQL queries and alternative flows live here.
"""
from app import mysql


class Favourite:

    # ── Save ──────────────────────────────────────────────────

    @staticmethod
    def save(user_id: int, activity_id: int):
        """
        Save an activity to favourites.
        Alt 1: Already saved → return 'already_saved'
        Alt 2: Activity not found → return 'not_found'
        Main: INSERT into DB, return True
        """
        if Favourite.exists(user_id, activity_id):              # Alt 1
            return 'already_saved'

        if not Favourite.activityExists(activity_id):           # Alt 2
            return 'not_found'

        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO favourite (user_id, activity_id)
               VALUES (%s, %s)""",
            (user_id, activity_id)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Remove ────────────────────────────────────────────────

    @staticmethod
    def remove(user_id: int, activity_id: int):
        """
        Remove an activity from favourites.
        Alt 1: Not in favourites → return 'not_found'
        Main: DELETE from DB, return True
        """
        if not Favourite.exists(user_id, activity_id):          # Alt 1
            return 'not_found'

        cursor = mysql.connection.cursor()
        cursor.execute(
            "DELETE FROM favourite WHERE user_id = %s AND activity_id = %s",
            (user_id, activity_id)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Search ────────────────────────────────────────────────

    @staticmethod
    def search(query: str, user_id: int):
        """SEARCH favourites by activity title."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT a.*, c.category_name, u.username as creator,
                      f.favourite_id, f.created_at as saved_at
               FROM favourite f
               JOIN activity a ON f.activity_id = a.activity_id
               LEFT JOIN category c ON a.category_id = c.category_id
               LEFT JOIN useraccount u ON a.created_by = u.user_id
               WHERE f.user_id = %s AND a.title LIKE %s
               ORDER BY f.created_at DESC""",
            (user_id, f"%{query}%")
        )
        favourites = cursor.fetchall()
        cursor.close()
        return favourites

    # ── Pure SQL read methods ─────────────────────────────────

    @staticmethod
    def getAll(user_id: int):
        """Get all favourites for a donee."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT a.*, c.category_name, u.username as creator,
                      f.favourite_id, f.created_at as saved_at
               FROM favourite f
               JOIN activity a ON f.activity_id = a.activity_id
               LEFT JOIN category c ON a.category_id = c.category_id
               LEFT JOIN useraccount u ON a.created_by = u.user_id
               WHERE f.user_id = %s
               ORDER BY f.created_at DESC""",
            (user_id,)
        )
        favourites = cursor.fetchall()
        cursor.close()
        return favourites

    @staticmethod
    def exists(user_id: int, activity_id: int) -> bool:
        """Check if already saved."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT favourite_id FROM favourite WHERE user_id = %s AND activity_id = %s",
            (user_id, activity_id)
        )
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    @staticmethod
    def activityExists(activity_id: int) -> bool:
        """Check if activity exists."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT activity_id FROM activity WHERE activity_id = %s",
            (activity_id,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result is not None
