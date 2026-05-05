"""
app/routes/category_routes.py — Boundary Layer
================================================
Sprint 3 — PM-01 to PM-05: FSA Category Management

Separate boundary class per use case:
- CreateCategoryBoundary (PM-01)
- ViewCategoryBoundary   (PM-02)
- UpdateCategoryBoundary (PM-03)
- DeleteCategoryBoundary (PM-04)
- SearchCategoryBoundary (PM-05)
"""
from flask import Blueprint, request, jsonify
from app.services.category_controller import (
    CreateCategoryController,
    ViewCategoryController,
    UpdateCategoryController,
    DeleteCategoryController,
    SearchCategoryController,
)
from app.utils.auth_utils import token_required

category_bp = Blueprint('category', __name__)


class CreateCategoryBoundary:
    """Boundary — CreateCategoryBoundary (PM-01)"""

    @staticmethod
    @category_bp.route('/', methods=['POST'])
    @token_required(roles=['platform_manager'])
    def create_category(current_user):
        data = request.get_json()

        # [BOUNDARY] Input validation
        if not data:
            return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400
        if not data.get('category_name') or not str(data['category_name']).strip():
            return jsonify({'status': 'fail', 'error': 'Category name is required.'}), 400
        if len(str(data['category_name']).strip()) < 2:
            return jsonify({'status': 'fail', 'error': 'Category name must be at least 2 characters.'}), 400

        ok, payload = CreateCategoryController.createCategory(data)
        if ok:
            return jsonify(payload), 201
        return jsonify(payload), 400


class ViewCategoryBoundary:
    """Boundary — ViewCategoryBoundary (PM-02)"""

    @staticmethod
    @category_bp.route('/', methods=['GET'])
    @token_required(roles=['platform_manager'])
    def get_all_categories(current_user):
        query = request.args.get('query', '').strip()

        # [BOUNDARY] Validate empty query
        if 'query' in request.args and query == '':
            return jsonify({'status': 'fail', 'error': 'Search query cannot be empty.'}), 400

        if query:
            return SearchCategoryBoundary._search(query)

        ok, payload = ViewCategoryController.getAllCategories()
        return jsonify(payload), 200

    @staticmethod
    @category_bp.route('/<int:category_id>', methods=['GET'])
    @token_required(roles=['platform_manager'])
    def view_category(current_user, category_id):
        ok, payload = ViewCategoryController.viewCategory(category_id)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404


class UpdateCategoryBoundary:
    """Boundary — UpdateCategoryBoundary (PM-03)"""

    @staticmethod
    @category_bp.route('/<int:category_id>', methods=['PUT'])
    @token_required(roles=['platform_manager'])
    def update_category(current_user, category_id):
        data = request.get_json()

        # [BOUNDARY] Input validation
        if not data:
            return jsonify({'status': 'fail', 'error': 'Request body must be JSON.'}), 400
        if data.get('category_name') and len(str(data['category_name']).strip()) < 2:
            return jsonify({'status': 'fail', 'error': 'Category name must be at least 2 characters.'}), 400

        ok, payload = UpdateCategoryController.updateCategory(category_id, data)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 400


class DeleteCategoryBoundary:
    """Boundary — DeleteCategoryBoundary (PM-04)"""

    @staticmethod
    @category_bp.route('/<int:category_id>', methods=['DELETE'])
    @token_required(roles=['platform_manager'])
    def delete_category(current_user, category_id):
        ok, payload = DeleteCategoryController.deleteCategory(category_id)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404


class SearchCategoryBoundary:
    """Boundary — SearchCategoryBoundary (PM-05)"""

    @staticmethod
    def _search(query: str):
        ok, payload = SearchCategoryController.searchCategory(query)
        if ok:
            return jsonify(payload), 200
        return jsonify(payload), 404