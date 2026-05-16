"""
app/models/report.py — Entity Layer
=====================================
Sprint 6 — PM-06, PM-07, PM-08: Platform Manager Reports

Entity: generates daily, weekly, monthly reports.
All SQL queries live here.
"""
from app import mysql
from datetime import datetime, timedelta


class Report:

    @staticmethod
    def getDaily():
        """
        Generate daily report.
        Returns stats for today.
        """
        cursor = mysql.connection.cursor()
        today = datetime.now().date()

        # New activities today
        cursor.execute(
            "SELECT COUNT(*) as count FROM activity WHERE DATE(created_at) = %s",
            (today,)
        )
        new_activities = cursor.fetchone()['count']

        # New favourites today
        cursor.execute(
            "SELECT COUNT(*) as count FROM favourite WHERE DATE(created_at) = %s",
            (today,)
        )
        new_favourites = cursor.fetchone()['count']

        # New accounts today
        cursor.execute(
            "SELECT COUNT(*) as count FROM useraccount WHERE DATE(created_at) = %s",
            (today,)
        )
        new_accounts = cursor.fetchone()['count']

        # Total active activities
        cursor.execute("SELECT COUNT(*) as count FROM activity WHERE status = 'active'")
        active_activities = cursor.fetchone()['count']

        # Top categories today
        cursor.execute("""
            SELECT c.category_name, COUNT(a.activity_id) as count
            FROM activity a
            JOIN category c ON a.category_id = c.category_id
            WHERE DATE(a.created_at) = %s
            GROUP BY c.category_name
            ORDER BY count DESC
            LIMIT 5
        """, (today,))
        top_categories = cursor.fetchall()

        cursor.close()
        return {
            'period':           'daily',
            'date':             str(today),
            'new_activities':   new_activities,
            'new_favourites':   new_favourites,
            'new_accounts':     new_accounts,
            'active_activities':active_activities,
            'top_categories':   top_categories,
        }

    @staticmethod
    def getWeekly():
        """
        Generate weekly report.
        Returns stats for the last 7 days.
        """
        cursor = mysql.connection.cursor()
        today     = datetime.now().date()
        week_ago  = today - timedelta(days=7)

        cursor.execute(
            "SELECT COUNT(*) as count FROM activity WHERE DATE(created_at) BETWEEN %s AND %s",
            (week_ago, today)
        )
        new_activities = cursor.fetchone()['count']

        cursor.execute(
            "SELECT COUNT(*) as count FROM favourite WHERE DATE(created_at) BETWEEN %s AND %s",
            (week_ago, today)
        )
        new_favourites = cursor.fetchone()['count']

        cursor.execute(
            "SELECT COUNT(*) as count FROM useraccount WHERE DATE(created_at) BETWEEN %s AND %s",
            (week_ago, today)
        )
        new_accounts = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM activity WHERE status = 'active'")
        active_activities = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM activity WHERE status = 'completed'")
        completed_activities = cursor.fetchone()['count']

        cursor.execute("""
            SELECT c.category_name, COUNT(a.activity_id) as count
            FROM activity a
            JOIN category c ON a.category_id = c.category_id
            WHERE DATE(a.created_at) BETWEEN %s AND %s
            GROUP BY c.category_name
            ORDER BY count DESC
            LIMIT 5
        """, (week_ago, today))
        top_categories = cursor.fetchall()

        cursor.close()
        return {
            'period':               'weekly',
            'from_date':            str(week_ago),
            'to_date':              str(today),
            'new_activities':       new_activities,
            'new_favourites':       new_favourites,
            'new_accounts':         new_accounts,
            'active_activities':    active_activities,
            'completed_activities': completed_activities,
            'top_categories':       top_categories,
        }

    @staticmethod
    def getMonthly():
        """
        Generate monthly report.
        Returns stats for the last 30 days.
        """
        cursor = mysql.connection.cursor()
        today      = datetime.now().date()
        month_ago  = today - timedelta(days=30)

        cursor.execute(
            "SELECT COUNT(*) as count FROM activity WHERE DATE(created_at) BETWEEN %s AND %s",
            (month_ago, today)
        )
        new_activities = cursor.fetchone()['count']

        cursor.execute(
            "SELECT COUNT(*) as count FROM favourite WHERE DATE(created_at) BETWEEN %s AND %s",
            (month_ago, today)
        )
        new_favourites = cursor.fetchone()['count']

        cursor.execute(
            "SELECT COUNT(*) as count FROM useraccount WHERE DATE(created_at) BETWEEN %s AND %s",
            (month_ago, today)
        )
        new_accounts = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM activity WHERE status = 'active'")
        active_activities = cursor.fetchone()['count']

        cursor.execute("SELECT COUNT(*) as count FROM activity WHERE status = 'completed'")
        completed_activities = cursor.fetchone()['count']

        cursor.execute("""
            SELECT c.category_name, COUNT(a.activity_id) as count
            FROM activity a
            JOIN category c ON a.category_id = c.category_id
            WHERE DATE(a.created_at) BETWEEN %s AND %s
            GROUP BY c.category_name
            ORDER BY count DESC
        """, (month_ago, today))
        top_categories = cursor.fetchall()

        # Most viewed activities this month
        cursor.execute("""
            SELECT a.title, a.view_count, c.category_name
            FROM activity a
            LEFT JOIN category c ON a.category_id = c.category_id
            ORDER BY a.view_count DESC
            LIMIT 5
        """)
        most_viewed = cursor.fetchall()

        cursor.close()
        return {
            'period':               'monthly',
            'from_date':            str(month_ago),
            'to_date':              str(today),
            'new_activities':       new_activities,
            'new_favourites':       new_favourites,
            'new_accounts':         new_accounts,
            'active_activities':    active_activities,
            'completed_activities': completed_activities,
            'top_categories':       top_categories,
            'most_viewed':          most_viewed,
        }
