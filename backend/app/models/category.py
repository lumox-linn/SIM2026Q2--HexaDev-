"""
app/models/category.py — Entity Layer
======================================
Sprint 3 — PM-01 to PM-05: FSA Category Management

Entity: maps to category table.
All SQL queries and alternative flows live here.
"""
from app import mysql


class Category:

    # ── Alt Flow Methods ──────────────────────────────────────

    @staticmethod
    def createIfNotExists(data: dict):
        """
        Create a category.
        Alt 1: Category name already exists → return None
        Main: Create, return True
        """
        if Category.exists(data['category_name']):
            return None

        Category.createCategory(data)
        return True

    @staticmethod
    def updateIfExists(category_id: int, data: dict):
        """
        Update a category.
        Alt 1: Category not found → return 'not_found'
        Alt 2: New name already taken → return 'name_taken'
        Main: Update, return True
        """
        category = Category.findById(category_id)

        if not category:
            return 'not_found'

        if data.get('category_name') and data['category_name'] != category['category_name']:
            if Category.exists(data['category_name']):
                return 'name_taken'

        Category.updateCategory(category_id, data)
        return True

    @staticmethod
    def deleteIfExists(category_id: int):
        """
        Delete a category.
        Alt 1: Category not found → return 'not_found'
        Main: Delete, return True
        """
        category = Category.findById(category_id)

        if not category:
            return 'not_found'

        Category.deleteCategory(category_id)
        return True

    # ── Pure SQL Methods ──────────────────────────────────────

    @staticmethod
    def findById(category_id: int):
        """SELECT category by ID."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM category WHERE category_id = %s",
            (category_id,)
        )
        category = cursor.fetchone()
        cursor.close()
        return category

    @staticmethod
    def exists(category_name: str) -> bool:
        """Check if category name already exists."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT category_id FROM category WHERE category_name = %s",
            (category_name,)
        )
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    @staticmethod
    def getAll():
        """SELECT all categories ordered by name."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM category ORDER BY category_name ASC"
        )
        categories = cursor.fetchall()
        cursor.close()
        return categories

    @staticmethod
    def searchCategories(query: str):
        """SEARCH categories by name."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM category WHERE category_name LIKE %s ORDER BY category_name ASC",
            (f"%{query}%",)
        )
        categories = cursor.fetchall()
        cursor.close()
        return categories

    @staticmethod
    def createCategory(data: dict) -> None:
        """INSERT new category."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            """INSERT INTO category (category_name, description, status)
               VALUES (%s, %s, 'active')""",
            (
                data['category_name'].strip(),
                data.get('description', None)
            )
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def updateCategory(category_id: int, data: dict) -> None:
        """UPDATE category fields."""
        fields = []
        values = []

        if data.get('category_name'):
            fields.append('category_name = %s')
            values.append(data['category_name'].strip())
        if 'description' in data:
            fields.append('description = %s')
            values.append(data['description'])

        if not fields:
            return

        values.append(category_id)
        cursor = mysql.connection.cursor()
        cursor.execute(
            f"UPDATE category SET {', '.join(fields)} WHERE category_id = %s",
            tuple(values)
        )
        mysql.connection.commit()
        cursor.close()

    @staticmethod
    def deleteCategory(category_id: int) -> None:
        """DELETE category permanently."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "DELETE FROM category WHERE category_id = %s",
            (category_id,)
        )
        mysql.connection.commit()
        cursor.close()