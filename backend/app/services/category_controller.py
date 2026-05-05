"""
app/services/category_controller.py — Control Layer
=====================================================
Sprint 3 — PM-01 to PM-05: FSA Category Management

Separate controller class per use case:
- CreateCategoryController (PM-01)
- ViewCategoryController   (PM-02)
- UpdateCategoryController (PM-03)
- DeleteCategoryController (PM-04)
- SearchCategoryController (PM-05)
"""
from app.models.category import Category


class CreateCategoryController:
    """Control — CreateCategoryController (PM-01)"""

    @staticmethod
    def createCategory(data: dict):
        result = Category.create(data)
        if not result:
            return False, {
                'status': 'fail',
                'error':  f"Category '{data['category_name']}' already exists."
            }
        return True, {
            'status':  'success',
            'message': f"Category '{data['category_name']}' created successfully."
        }


class ViewCategoryController:
    """Control — ViewCategoryController (PM-02)"""

    @staticmethod
    def getAllCategories():
        categories = Category.getAll()
        return True, {
            'status':     'success',
            'message':    f'{len(categories)} category(s) found.',
            'categories': categories
        }

    @staticmethod
    def viewCategory(category_id: int):
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


class UpdateCategoryController:
    """Control — UpdateCategoryController (PM-03)"""

    @staticmethod
    def updateCategory(category_id: int, data: dict):
        result = Category.update(category_id, data)
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
            'status':      'success',
            'message':     'Category updated successfully.',
            'category_id': category_id
        }


class DeleteCategoryController:
    """Control — DeleteCategoryController (PM-04)"""

    @staticmethod
    def deleteCategory(category_id: int):
        result = Category.delete(category_id)
        if result == 'not_found':
            return False, {
                'status': 'fail',
                'error':  f'Category with ID {category_id} not found.'
            }
        return True, {
            'status':      'success',
            'message':     'Category deleted successfully.',
            'category_id': category_id
        }


class SearchCategoryController:
    """Control — SearchCategoryController (PM-05)"""

    @staticmethod
    def searchCategory(query: str):
        categories = Category.search(query.strip())
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


# Keep old name as alias for backward compatibility
class CategoryController:
    createCategory = CreateCategoryController.createCategory
    getAllCategories = ViewCategoryController.getAllCategories
    viewCategory    = ViewCategoryController.viewCategory
    updateCategory  = UpdateCategoryController.updateCategory
    deleteCategory  = DeleteCategoryController.deleteCategory
    searchCategory  = SearchCategoryController.searchCategory