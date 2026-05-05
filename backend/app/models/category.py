"""
app/models/category.py — Entity Layer
======================================
Sprint 3 — PM-01 to PM-05: FSA Category Management

REFACTORED:
- Merged createIfNotExists() + createCategory() → create()
- Merged updateIfExists() + updateCategory() → update()
- Merged deleteIfExists() + deleteCategory() → delete()
- Merged searchCategories() → search()
- All alt flows and SQL in same method
"""
from app import mysql


class Category:

    # ── Create ────────────────────────────────────────────────

    @staticmethod
    def create(data: dict):
        """
        Create a category.
        Alt 1: Category name already exists → return None
        Main: INSERT into DB, return True
        """
        if Category.exists(data['category_name']):               # Alt 1
            return None

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
        return True

    # ── Update ────────────────────────────────────────────────

    @staticmethod
    def update(category_id: int, data: dict):
        """
        Update a category.
        Alt 1: Category not found → return 'not_found'
        Alt 2: New name already taken → return 'name_taken'
        Main: UPDATE in DB, return True
        """
        category = Category.findById(category_id)

        if not category:                                          # Alt 1
            return 'not_found'

        if data.get('category_name') and data['category_name'] != category['category_name']:
            if Category.exists(data['category_name']):           # Alt 2
                return 'name_taken'

        fields = []
        values = []

        if data.get('category_name'):
            fields.append('category_name = %s')
            values.append(data['category_name'].strip())
        if 'description' in data:
            fields.append('description = %s')
            values.append(data['description'])

        if not fields:
            return True

        values.append(category_id)
        cursor = mysql.connection.cursor()
        cursor.execute(
            f"UPDATE category SET {', '.join(fields)} WHERE category_id = %s",
            tuple(values)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Delete ────────────────────────────────────────────────

    @staticmethod
    def delete(category_id: int):
        """
        Delete a category.
        Alt 1: Category not found → return 'not_found'
        Main: DELETE from DB, return True
        """
        if not Category.findById(category_id):                   # Alt 1
            return 'not_found'

        cursor = mysql.connection.cursor()
        cursor.execute(
            "DELETE FROM category WHERE category_id = %s", (category_id,)
        )
        mysql.connection.commit()
        cursor.close()
        return True

    # ── Search ────────────────────────────────────────────────

    @staticmethod
    def search(query: str):
        """SEARCH categories by name."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM category WHERE category_name LIKE %s ORDER BY category_name ASC",
            (f"%{query}%",)
        )
        categories = cursor.fetchall()
        cursor.close()
        return categories

    # ── Pure SQL read methods ─────────────────────────────────

    @staticmethod
    def findById(category_id: int):
        """SELECT category by ID."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT * FROM category WHERE category_id = %s", (category_id,)
        )
        category = cursor.fetchone()
        cursor.close()
        return category

    @staticmethod
    def exists(category_name: str) -> bool:
        """Check if category name already exists."""
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT category_id FROM category WHERE category_name = %s", (category_name,)
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