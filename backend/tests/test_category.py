"""
Sprint 3 Unit Tests — FSA Category Management
Assigned to: Jiecheng
Run: pytest tests/test_category.py -v
"""
import pytest
from unittest.mock import patch
from app.services.category_controller import (
    CreateCategoryController,
    ViewCategoryController,
    UpdateCategoryController,
    DeleteCategoryController,
    SearchCategoryController,
)


def make_category(category_id=1, name='Education', description='Educational activities', status='active'):
    return {
        'category_id':   category_id,
        'category_name': name,
        'description':   description,
        'status':        status,
        'created_at':    '2026-04-25 10:00:00'
    }

def make_pm_account():
    return {
        'user_id': 2, 'username': 'pm01', 'role': 'platform_manager',
        'isActive': 1, 'email': None, 'dob': None, 'profile_picture': None,
    }

def make_account(role='admin'):
    return {
        'user_id': 1, 'username': 'admin01', 'role': role,
        'isActive': 1, 'email': None, 'dob': None, 'profile_picture': None,
    }

@pytest.fixture
def pm_token(app):
    from app.utils.auth_utils import generate_token
    return generate_token(user_id=2, role='platform_manager')


# ══════════════════════════════════════════════════════════════
# PM-01 — CREATE CATEGORY — CreateCategoryController
# ══════════════════════════════════════════════════════════════

class TestCreateCategory:

    # Boundary tests via route
    def test_empty_name_fails(self, client, pm_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_pm_account()):
            res = client.post('/api/categories/',
                json={'category_name': ''},
                headers={'Authorization': f'Bearer {pm_token}'})
        assert res.status_code == 400
        assert 'name' in res.get_json()['error'].lower()

    def test_short_name_fails(self, client, pm_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_pm_account()):
            res = client.post('/api/categories/',
                json={'category_name': 'A'},
                headers={'Authorization': f'Bearer {pm_token}'})
        assert res.status_code == 400

    def test_no_body_fails(self, client, pm_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_pm_account()):
            res = client.post('/api/categories/',
                headers={'Authorization': f'Bearer {pm_token}'})
        assert res.status_code == 400

    def test_non_pm_cannot_create(self, client):
        from app.utils.auth_utils import generate_token
        token = generate_token(user_id=1, role='admin')
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_account(role='admin')):
            res = client.post('/api/categories/',
                json={'category_name': 'Test'},
                headers={'Authorization': f'Bearer {token}'})
        assert res.status_code == 403

    # Controller tests
    @patch('app.models.category.Category.exists', return_value=True)
    def test_duplicate_name_fails(self, _):
        ok, d = CreateCategoryController.createCategory({'category_name': 'Education'})
        assert ok is False and 'exists' in d['error'].lower()

    @patch('app.models.category.Category.exists', return_value=False)
    def test_create_success(self, _):
        ok, d = CreateCategoryController.createCategory({'category_name': 'Education'})
        assert ok is True and d['status'] == 'success'

    @patch('app.models.category.Category.exists', return_value=False)
    def test_create_returns_success_message(self, _):
        ok, d = CreateCategoryController.createCategory({'category_name': 'Health'})
        assert ok is True and 'Health' in d['message']


# ══════════════════════════════════════════════════════════════
# PM-02 — VIEW CATEGORY — ViewCategoryController
# ══════════════════════════════════════════════════════════════

class TestViewCategory:

    @patch('app.models.category.Category.getAll', return_value=[])
    def test_get_all_empty(self, _):
        ok, d = ViewCategoryController.getAllCategories()
        assert ok is True and d['categories'] == []

    @patch('app.models.category.Category.getAll')
    def test_get_all_returns_categories(self, mock_get):
        mock_get.return_value = [make_category(), make_category(category_id=2, name='Health')]
        ok, d = ViewCategoryController.getAllCategories()
        assert ok is True and len(d['categories']) == 2

    @patch('app.models.category.Category.findById', return_value=None)
    def test_view_not_found(self, _):
        ok, d = ViewCategoryController.viewCategory(999)
        assert ok is False and 'not found' in d['error'].lower()

    @patch('app.models.category.Category.findById')
    def test_view_success(self, mock_find):
        mock_find.return_value = make_category()
        ok, d = ViewCategoryController.viewCategory(1)
        assert ok is True and d['category']['category_name'] == 'Education'

    @patch('app.models.category.Category.findById')
    def test_view_returns_correct_fields(self, mock_find):
        mock_find.return_value = make_category()
        ok, d = ViewCategoryController.viewCategory(1)
        assert ok is True
        for field in ['category_id', 'category_name', 'description', 'status']:
            assert field in d['category']


# ══════════════════════════════════════════════════════════════
# PM-03 — UPDATE CATEGORY — UpdateCategoryController
# ══════════════════════════════════════════════════════════════

class TestUpdateCategory:

    @patch('app.models.category.Category.findById', return_value=None)
    def test_update_not_found(self, _):
        ok, d = UpdateCategoryController.updateCategory(999, {'category_name': 'New'})
        assert ok is False and 'not found' in d['error'].lower()

    @patch('app.models.category.Category.findById')
    @patch('app.models.category.Category.exists', return_value=True)
    def test_update_duplicate_name_fails(self, _, mock_find):
        mock_find.return_value = make_category(name='Education')
        ok, d = UpdateCategoryController.updateCategory(1, {'category_name': 'Health'})
        assert ok is False and 'exists' in d['error'].lower()

    @patch('app.models.category.Category.findById')
    def test_update_success(self, mock_find):
        mock_find.return_value = make_category()
        ok, d = UpdateCategoryController.updateCategory(1, {'category_name': 'New Name'})
        assert ok is True and d['status'] == 'success'

    @patch('app.models.category.Category.findById')
    def test_update_description_only(self, mock_find):
        mock_find.return_value = make_category()
        ok, d = UpdateCategoryController.updateCategory(1, {'description': 'New desc'})
        assert ok is True

    def test_short_name_fails(self, client, pm_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_pm_account()):
            res = client.put('/api/categories/1',
                json={'category_name': 'A'},
                headers={'Authorization': f'Bearer {pm_token}'})
        assert res.status_code == 400


# ══════════════════════════════════════════════════════════════
# PM-04 — DELETE CATEGORY — DeleteCategoryController
# ══════════════════════════════════════════════════════════════

class TestDeleteCategory:

    @patch('app.models.category.Category.findById', return_value=None)
    def test_delete_not_found(self, _):
        ok, d = DeleteCategoryController.deleteCategory(999)
        assert ok is False and 'not found' in d['error'].lower()

    @patch('app.models.category.Category.findById')
    def test_delete_success(self, mock_find):
        mock_find.return_value = make_category()
        ok, d = DeleteCategoryController.deleteCategory(1)
        assert ok is True and d['status'] == 'success'

    @patch('app.models.category.Category.findById')
    def test_delete_returns_category_id(self, mock_find):
        mock_find.return_value = make_category()
        ok, d = DeleteCategoryController.deleteCategory(1)
        assert ok is True and d['category_id'] == 1


# ══════════════════════════════════════════════════════════════
# PM-05 — SEARCH CATEGORY — SearchCategoryController
# ══════════════════════════════════════════════════════════════

class TestSearchCategory:

    def test_empty_query_fails(self, client, pm_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_pm_account()):
            res = client.get('/api/categories/?query=',
                headers={'Authorization': f'Bearer {pm_token}'})
        assert res.status_code == 400

    @patch('app.models.category.Category.search', return_value=[])
    def test_no_results(self, _):
        ok, d = SearchCategoryController.searchCategory('xyz')
        assert ok is False and 'no categories' in d['error'].lower()

    @patch('app.models.category.Category.search')
    def test_search_success(self, mock_search):
        mock_search.return_value = [make_category()]
        ok, d = SearchCategoryController.searchCategory('Edu')
        assert ok is True and len(d['categories']) == 1

    @patch('app.models.category.Category.search')
    def test_search_partial_match(self, mock_search):
        mock_search.return_value = [
            make_category(name='Education'),
            make_category(category_id=2, name='Environment')
        ]
        ok, d = SearchCategoryController.searchCategory('E')
        assert ok is True and len(d['categories']) == 2