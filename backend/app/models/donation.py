"""
app/models/donation.py — Entity Layer
=======================================
Sprint 6 — DN-HS-01, DN-HS-02: Donee Donation History.

Entity: maps to donation table.
All SQL queries and alt flows live here.
"""
from app import mysql


class Donation:

    @staticmethod
    def getHistory(user_id: int, category_id: int = None,
                   start_date: str = None, end_date: str = None):
        """
        Get donation history for a Donee.
        Alt 1: No donations found → return []
        Main: SELECT from donation table with optional filters
        """
        cursor = mysql.connection.cursor()

        query = """
            SELECT d.donation_id, d.amount, d.donated_at,
                   a.activity_id, a.title, a.description,
                   a.target_amount, a.amount_raised,
                   a.status, a.start_date, a.end_date,
                   c.category_name,
                   u.username as creator
            FROM donation d
            JOIN activity a ON d.activity_id = a.activity_id
            LEFT JOIN category c ON a.category_id = c.category_id
            LEFT JOIN useraccount u ON a.created_by = u.user_id
            WHERE d.user_id = %s
        """
        params = [user_id]

        if category_id:
            query += " AND a.category_id = %s"
            params.append(category_id)

        if start_date:
            query += " AND d.donated_at >= %s"
            params.append(start_date)

        if end_date:
            query += " AND d.donated_at <= %s"
            params.append(end_date)

        query += " ORDER BY d.donated_at DESC"

        cursor.execute(query, tuple(params))
        history = cursor.fetchall()
        cursor.close()
        return history
