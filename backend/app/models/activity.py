"""
app/models/activity.py — Entity Layer (Updated Sprint 6)
=========================================================
Adds:
- incrementViewCount() for FR-IT-01
- getShortlistCount() for FR-IT-02
- getHistory() for FR-HS-01, FR-HS-02
- getDoneeHistory() for DN-HS-01, DN-HS-02
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
        if Activity.existsByTitle(data["title"], data["created_by"]):
            return None

        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO activity
               (title, description, category_id, created_by,
                target_amount, amount_raised, start_date, end_date, status, view_count)
               VALUES (%s, %s, %s, %s, %s, 0.00, %s, %s, 'active', 0)""",
            (
                data["title"].strip(),
                data.get("description", None),
                data.get("category_id", None),
                data["created_by"],
                data.get("target_amount", 0.00),
                data.get("start_date", None),
                data.get("end_date", None),
            ),
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

        if not activity:
            return "not_found"
        if activity["created_by"] != user_id:
            return "unauthorized"

        fields = []
        values = []

        if data.get("title"):
            fields.append("title = %s")
            values.append(data["title"].strip())
        if "description" in data:
            fields.append("description = %s")
            values.append(data["description"])
        if data.get("category_id") is not None:
            fields.append("category_id = %s")
            values.append(data["category_id"])
        if data.get("target_amount") is not None:
            fields.append("target_amount = %s")
            values.append(data["target_amount"])
        if data.get("amount_raised") is not None:
            fields.append("amount_raised = %s")
            values.append(data["amount_raised"])
        if data.get("start_date") is not None:
            fields.append("start_date = %s")
            values.append(data["start_date"])
        if data.get("end_date") is not None:
            fields.append("end_date = %s")
            values.append(data["end_date"])
        if data.get("status") is not None:
            fields.append("status = %s")
            values.append(data["status"])

        if not fields:
            return True

        values.append(activity_id)
        cursor = mysql.connection.cursor()
        cursor.execute(
            f"UPDATE activity SET {', '.join(fields)} WHERE activity_id = %s",
            tuple(values),
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Delete ────────────────────────────────────────────────

    @staticmethod
    def suspend(activity_id: int, user_id: int):
        """
        Delete a fundraising activity.
        Alt 1: Activity not found → return 'not_found'
        Alt 2: Belongs to different user → return 'unauthorized'
        Main: DELETE from DB, return True
        """
        activity = Activity.findById(activity_id)

        if not activity:
            return "not_found"
        if activity["created_by"] != user_id:
            return "unauthorized"

        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE activity SET status = 'suspended' WHERE activity_id = %s",
            (activity_id,),
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── View Count (FR-IT-01) ─────────────────────────────────

    @staticmethod
    def incrementViewCount(activity_id: int):
        """Increment view count by 1 when donee views an activity."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "UPDATE activity SET view_count = view_count + 1 WHERE activity_id = %s",
            (activity_id,),
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Shortlist Count (FR-IT-02) ────────────────────────────

    @staticmethod
    def getShortlistCount(activity_id: int):
        """Get number of times activity has been saved to favourites."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT COUNT(*) as shortlist_count FROM favourite WHERE activity_id = %s",
            (activity_id,),
        )
        result = cursor.fetchone()
        cursor.close()
        return result["shortlist_count"] if result else 0

    # ── History (FR-HS-01, FR-HS-02) ─────────────────────────

    @staticmethod
    def getHistory(
        user_id: int,
        category_id: int = None,
        start_date: str = None,
        end_date: str = None,
    ):
        """
        Get completed/ended activities for a Fund Raiser.
        Filters by category and/or date period.
        'Completed' = status = 'completed' OR end_date has passed.
        """
        cursor = mysql.connection.cursor()

        query = """
            SELECT a.*, c.category_name, u.username as creator,
                   (SELECT COUNT(*) FROM favourite f WHERE f.activity_id = a.activity_id) as shortlist_count
            FROM activity a
            LEFT JOIN category c ON a.category_id = c.category_id
            LEFT JOIN useraccount u ON a.created_by = u.user_id
            WHERE a.created_by = %s
            AND (a.status = 'completed' OR (a.end_date IS NOT NULL AND a.end_date < CURDATE()))
        """
        params = [user_id]

        if category_id:
            query += " AND a.category_id = %s"
            params.append(category_id)

        if start_date:
            query += " AND a.created_at >= %s"
            params.append(start_date)

        if end_date:
            query += " AND a.created_at <= %s"
            params.append(end_date)

        query += " ORDER BY a.created_at DESC"

        cursor.execute(query, tuple(params))
        activities = cursor.fetchall()
        cursor.close()
        return activities

    # ── Donee History (DN-HS-01, DN-HS-02) ───────────────────

    @staticmethod
    def getDoneeHistory(
        user_id: int,
        category_id: int = None,
        start_date: str = None,
        end_date: str = None,
    ):
        """
        Get activities a Donee has favourited (donation history).
        Filters by category and/or date period.
        """
        cursor = mysql.connection.cursor()

        query = """
            SELECT a.*, c.category_name, u.username as creator,
                   f.created_at as saved_at, f.favourite_id
            FROM favourite f
            JOIN activity a ON f.activity_id = a.activity_id
            LEFT JOIN category c ON a.category_id = c.category_id
            LEFT JOIN useraccount u ON a.created_by = u.user_id
            WHERE f.user_id = %s
        """
        params = [user_id]

        if category_id:
            query += " AND a.category_id = %s"
            params.append(category_id)

        if start_date:
            query += " AND f.created_at >= %s"
            params.append(start_date)

        if end_date:
            query += " AND f.created_at <= %s"
            params.append(end_date)

        query += " ORDER BY f.created_at DESC"

        cursor.execute(query, tuple(params))
        history = cursor.fetchall()
        cursor.close()
        return history

    # ── Search ────────────────────────────────────────────────

    @staticmethod
    def search(query: str, user_id: int = None):
        """SEARCH activities by title."""
        cursor = mysql.connection.cursor()
        if user_id:
            cursor.execute(
                """SELECT a.*, c.category_name, u.username as creator,
                          (SELECT COUNT(*) FROM favourite f WHERE f.activity_id = a.activity_id) as shortlist_count
                   FROM activity a
                   LEFT JOIN category c ON a.category_id = c.category_id
                   LEFT JOIN useraccount u ON a.created_by = u.user_id
                   WHERE a.title LIKE %s AND a.created_by = %s
                   ORDER BY a.created_at DESC""",
                (f"%{query}%", user_id),
            )
        else:
            cursor.execute(
                """SELECT a.*, c.category_name, u.username as creator
                   FROM activity a
                   LEFT JOIN category c ON a.category_id = c.category_id
                   LEFT JOIN useraccount u ON a.created_by = u.user_id
                   WHERE a.title LIKE %s
                   ORDER BY a.created_at DESC""",
                (f"%{query}%",),
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
            """SELECT a.*, c.category_name, u.username as creator,
                      (SELECT COUNT(*) FROM favourite f WHERE f.activity_id = a.activity_id) as shortlist_count
               FROM activity a
               LEFT JOIN category c ON a.category_id = c.category_id
               LEFT JOIN useraccount u ON a.created_by = u.user_id
               WHERE a.activity_id = %s""",
            (activity_id,),
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
            (title.strip(), user_id),
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
                """SELECT a.*, c.category_name, u.username as creator,
                          (SELECT COUNT(*) FROM favourite f WHERE f.activity_id = a.activity_id) as shortlist_count
                   FROM activity a
                   LEFT JOIN category c ON a.category_id = c.category_id
                   LEFT JOIN useraccount u ON a.created_by = u.user_id
                   WHERE a.created_by = %s
                   ORDER BY a.created_at DESC""",
                (user_id,),
            )
        else:
            cursor.execute("""SELECT a.*, c.category_name, u.username as creator
                   FROM activity a
                   LEFT JOIN category c ON a.category_id = c.category_id
                   LEFT JOIN useraccount u ON a.created_by = u.user_id
                   ORDER BY a.created_at DESC""")
        activities = cursor.fetchall()
        cursor.close()
        return activities
