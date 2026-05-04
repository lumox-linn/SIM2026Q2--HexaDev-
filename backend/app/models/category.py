"""
app/services/category_controller.py — Control Layer
=====================================================
Sprint 3 — PM-01 to PM-05: FSA Category Management
"""
from app.models.category import Category


class CategoryController:

    @staticmethod
    def createCategory(data: dict):
        """PM-01 — Create a FSA category."""
        result = Category.createIfNotExists(data)

        if not result:
            return False, {
                'status': 'fail',
                'error':  f"Category '{data['category_name']}' already exists."
            }
        return True, {
            'status':  'success',
            'message': f"Category '{data['category_name']}' created successfully."
        }

    @staticmethod
    def getAllCategories():
        """PM-02 — Get all FSA categories."""
        categories = Category.getAll()
        return True, {
            'status':     'success',
            'message':    f'{len(categories)} category(s) found.',
            'categories': categories
        }

    @staticmethod
    def viewCategory(category_id: int):
        """PM-02 — View one FSA category."""
        category = Category.findById(category_id)

        if not category:
            return False, {
                'status': 'fail',
                'error':  f'Category with ID {category_id} not found.'
            }
        return True, {
            'status':   'success',
            'category': category
        }

    @staticmethod
    def updateCategory(category_id: int, data: dict):
        """PM-03 — Update a FSA category."""
        result = Category.updateIfExists(category_id, data)

        if result == 'not_found':
            return False, {
                'status': 'fail',
                'error':  f'Category with ID {category_id} not found.'
            }
        if result == 'name_taken':
            return False, {
                'status': 'fail',
                'error':  f"Category name '{data.get('category_name')}' already exists."
            }
        return True, {
            'status':  'success',
            'message': 'Category updated successfully.',
            'category_id': category_id
        }

    @staticmethod
    def deleteCategory(category_id: int):
        """PM-04 — Delete a FSA category."""
        result = Category.deleteIfExists(category_id)

        if result == 'not_found':
            return False, {
                'status': 'fail',
                'error':  f'Category with ID {category_id} not found.'
            }
        return True, {
            'status':  'success',
            'message': 'Category deleted successfully.',
            'category_id': category_id
        }

    @staticmethod
    def searchCategory(query: str):
        """PM-05 — Search for a FSA category."""
        categories = Category.searchCategories(query.strip())

        if not categories:
            return False, {
                'status': 'fail',
                'error':  f"No categories found matching '{query}'."
            }
        return True, {
            'status':     'success',
            'message':    f'{len(categories)} category(s) found.',
            'categories': categories
        }