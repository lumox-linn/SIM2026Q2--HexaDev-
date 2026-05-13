"""
app/models/activity.py — Entity Layer
======================================
Sprint 4 — FR-01 to FR-05: Fundraising Activity Management

Entity: maps to activity table.
All SQL queries and alternative flows live here.
"""
from app import mysql


class Activity:

    # ── Create ────────────────────────────────────────────────

    @staticmethod
    def create(data: dict):
        """
        Create a fundraising activity.
        Alt 1: Title already exists for this user → return None
        Main: INSERT into DB, return True
        """
        if Activity.existsByTitle(data['title'], data['created_by']):
            return None

        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO activity
               (title, description, category_id, created_by,
                target_amount, amount_raised, start_date, end_date, status)
               VALUES (%s, %s, %s, %s, %s, 0.00, %s, %s, 'active')""",
            (
                data['title'].strip(),
                data.get('description', None),
                data.get('category_id', None),
                data['created_by'],
                data.get('target_amount', 0.00),
                data.get('start_date', None),
                data.get('end_date', None),
            )
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Update ────────────────────────────────────────────────

    @staticmethod
    def update(activity_id: int, user_id: int, data: dict):
        """
        Update a fundraising activity.
        Alt 1: Activity not found → return 'not_found'
        Alt 2: Belongs to different user → return 'unauthorized'
        Main: UPDATE in DB, return True
        """
        activity = Activity.findById(activity_id)

        if not activity:                              # Alt 1
            return 'not_found'
        if activity['created_by'] != user_id:         # Alt 2
            return 'unauthorized'

        fields = []
        values = []

        if data.get('title'):
            fields.append('title = %s')
            values.append(data['title'].strip())
        if 'description' in data:
            fields.append('description = %s')
            values.append(data['description'])
        if data.get('category_id') is not None:
            fields.append('category_id = %s')
            values.append(data['category_id'])
        if data.get('target_amount') is not None:
            fields.append('target_amount = %s')
            values.append(data['target_amount'])
        if data.get('amount_raised') is not None:
            fields.append('amount_raised = %s')
            values.append(data['amount_raised'])
        if data.get('start_date') is not None:
            fields.append('start_date = %s')
            values.append(data['start_date'])
        if data.get('end_date') is not None:
            fields.append('end_date = %s')
            values.append(data['end_date'])

        if not fields:
            return True

        values.append(activity_id)
        cursor = mysql.connection.cursor()
        cursor.execute(
            f"UPDATE activity SET {', '.join(fields)} WHERE activity_id = %s",
            tuple(values)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Delete ────────────────────────────────────────────────

    @staticmethod
    def delete(activity_id: int, user_id: int):
        """
        Delete a fundraising activity.
        Alt 1: Activity not found → return 'not_found'
        Alt 2: Belongs to different user → return 'unauthorized'
        Main: DELETE from DB, return True
        """
        activity = Activity.findById(activity_id)

        if not activity:                              # Alt 1
            return 'not_found'
        if activity['created_by'] != user_id:         # Alt 2
            return 'unauthorized'

        cursor = mysql.connection.cursor()
        cursor.execute(
            "DELETE FROM activity WHERE activity_id = %s", (activity_id,)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Search ────────────────────────────────────────────────

    @staticmethod
    def search(query: str, user_id: int = None):
        """SEARCH activities by title."""
        cursor = mysql.connection.cursor()
        if user_id:
            cursor.execute(
                """SELECT a.*, c.category_name, u.username as creator
                   FROM activity a
                   LEFT JOIN category c ON a.category_id = c.category_id
                   LEFT JOIN useraccount u ON a.created_by = u.user_id
                   WHERE a.title LIKE %s AND a.created_by = %s
                   ORDER BY a.created_at DESC""",
                (f"%{query}%", user_id)
            )
        else:
            cursor.execute(
                """SELECT a.*, c.category_name, u.username as creator
                   FROM activity a
                   LEFT JOIN category c ON a.category_id = c.category_id
                   LEFT JOIN useraccount u ON a.created_by = u.user_id
                   WHERE a.title LIKE %s
                   ORDER BY a.created_at DESC""",
                (f"%{query}%",)
            )
        activities = cursor.fetchall()
        cursor.close()
        return activities

    # ── Pure SQL read methods ─────────────────────────────────

    @staticmethod
    def findById(activity_id: int):
        """SELECT activity by ID."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            """SELECT a.*, c.category_name, u.username as creator
               FROM activity a
               LEFT JOIN category c ON a.category_id = c.category_id
               LEFT JOIN useraccount u ON a.created_by = u.user_id
               WHERE a.activity_id = %s""",
            (activity_id,)
        )
        activity = cursor.fetchone()
        cursor.close()
        return activity

    @staticmethod
    def existsByTitle(title: str, user_id: int) -> bool:
        """Check if same title exists for this fund raiser."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT activity_id FROM activity WHERE title = %s AND created_by = %s",
            (title.strip(), user_id)
        )
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    @staticmethod
    def getAll(user_id: int = None):
        """Get all activities, optionally filtered by creator."""
        cursor = mysql.connection.cursor()
        if user_id:
            cursor.execute(
                """SELECT a.*, c.category_name, u.username as creator
                   FROM activity a
                   LEFT JOIN category c ON a.category_id = c.category_id
                   LEFT JOIN useraccount u ON a.created_by = u.user_id
                   WHERE a.created_by = %s
                   ORDER BY a.created_at DESC""",
                (user_id,)
            )
        else:
            cursor.execute(
                """SELECT a.*, c.category_name, u.username as creator
                   FROM activity a
                   LEFT JOIN category c ON a.category_id = c.category_id
                   LEFT JOIN useraccount u ON a.created_by = u.user_id
                   ORDER BY a.created_at DESC"""
            )
        activities = cursor.fetchall()
        cursor.close()
        return activities