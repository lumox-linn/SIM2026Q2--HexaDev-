"""
tests/test_category.py
======================
Sprint 3 — PM-01 to PM-05: FSA Category Management

Tests follow BCE structure:
- Boundary tests: validation via HTTP client
- Control tests: controller logic via mock Entity
- Entity tests: alt flow methods via mock SQL
"""
import pytest
from unittest.mock import patch, MagicMock
from app.services.category_controller import CategoryController


# ── Helpers ───────────────────────────────────────────────────

def make_category(category_id=1, name='Education', description='Education activities', status='active'):
    return {
        'category_id':   category_id,
        'category_name': name,
        'description':   description,
        'status':        status,
        'created_at':    '2026-04-25 10:00:00'
    }

def make_pm_account():
    return {
        'user_id':   2,
        'username':  'pm01',
        'role':      'platform_manager',
        'isActive':  1,
        'email':     None,
        'dob':       None,
        'profile_picture': None,
    }

@pytest.fixture
def pm_token(app):
    from app.utils.auth_utils import generate_token
    return generate_token(user_id=2, role='platform_manager')


# ══════════════════════════════════════════════════════════════
# PM-01 — CREATE CATEGORY
# ══════════════════════════════════════════════════════════════

class TestCreateCategory:
    """PM-01 — Platform Manager creates a FSA category."""

    # ── Boundary validation tests ──────────────────────────────

    def test_empty_name_fails(self, client, pm_token):
        """Category name is required."""
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_pm_account()):
            res = client.post('/api/categories/',
                json={'category_name': ''},
                headers={'Authorization': f'Bearer {pm_token}'})
        assert res.status_code == 400
        assert 'name' in res.get_json()['error'].lower()

    def test_short_name_fails(self, client, pm_token):
        """Category name must be at least 2 characters."""
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_pm_account()):
            res = client.post('/api/categories/',
                json={'category_name': 'A'},
                headers={'Authorization': f'Bearer {pm_token}'})
        assert res.status_code == 400

    def test_no_body_fails(self, client, pm_token):
        """Request must have JSON body."""
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_pm_account()):
            res = client.post('/api/categories/',
                headers={'Authorization': f'Bearer {pm_token}'})
        assert res.status_code == 400

    def test_non_pm_cannot_create(self, client):
        """Only platform_manager role can create categories."""
        from app.utils.auth_utils import generate_token
        token = generate_token(user_id=1, role='admin')
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value={
                 'user_id': 1, 'username': 'admin01', 'role': 'admin', 'isActive': 1,
                 'email': None, 'dob': None, 'profile_picture': None
             }):
            res = client.post('/api/categories/',
                json={'category_name': 'Test'},
                headers={'Authorization': f'Bearer {token}'})
        assert res.status_code == 403

    # ── Control tests ──────────────────────────────────────────

    @patch('app.models.category.Category.createIfNotExists', return_value=None)
    def test_duplicate_name_fails(self, _):
        """Cannot create category with duplicate name."""
        ok, d = CategoryController.createCategory({'category_name': 'Education'})
        assert ok is False
        assert 'exists' in d['error'].lower()

    @patch('app.models.category.Category.createIfNotExists', return_value=True)
    def test_create_success(self, _):
        """Successfully creates a category."""
        ok, d = CategoryController.createCategory({'category_name': 'Education'})
        assert ok is True
        assert 'message' in d
        assert d['status'] == 'success'

    @patch('app.models.category.Category.createIfNotExists', return_value=True)
    def test_create_returns_success_message(self, _):
        """Success message contains category name."""
        ok, d = CategoryController.createCategory({'category_name': 'Health'})
        assert ok is True
        assert 'Health' in d['message']


# ══════════════════════════════════════════════════════════════
# PM-02 — VIEW CATEGORY
# ══════════════════════════════════════════════════════════════

class TestViewCategory:
    """PM-02 — Platform Manager views FSA categories."""

    @patch('app.models.category.Category.getAll', return_value=[])
    def test_get_all_empty(self, _):
        """Returns empty list if no categories."""
        ok, d = CategoryController.getAllCategories()
        assert ok is True
        assert d['categories'] == []

    @patch('app.models.category.Category.getAll')
    def test_get_all_returns_categories(self, mock_get):
        """Returns all categories."""
        mock_get.return_value = [make_category(), make_category(category_id=2, name='Health')]
        ok, d = CategoryController.getAllCategories()
        assert ok is True
        assert len(d['categories']) == 2

    @patch('app.models.category.Category.findById', return_value=None)
    def test_view_not_found(self, _):
        """Returns error if category not found."""
        ok, d = CategoryController.viewCategory(999)
        assert ok is False
        assert 'not found' in d['error'].lower()

    @patch('app.models.category.Category.findById')
    def test_view_success(self, mock_find):
        """Returns category details."""
        mock_find.return_value = make_category()
        ok, d = CategoryController.viewCategory(1)
        assert ok is True
        assert d['category']['category_name'] == 'Education'

    @patch('app.models.category.Category.findById')
    def test_view_returns_correct_fields(self, mock_find):
        """Category response has all required fields."""
        mock_find.return_value = make_category()
        ok, d = CategoryController.viewCategory(1)
        assert ok is True
        cat = d['category']
        assert 'category_id' in cat
        assert 'category_name' in cat
        assert 'description' in cat
        assert 'status' in cat


# ══════════════════════════════════════════════════════════════
# PM-03 — UPDATE CATEGORY
# ══════════════════════════════════════════════════════════════

class TestUpdateCategory:
    """PM-03 — Platform Manager updates a FSA category."""

    @patch('app.models.category.Category.updateIfExists', return_value='not_found')
    def test_update_not_found(self, _):
        """Returns error if category not found."""
        ok, d = CategoryController.updateCategory(999, {'category_name': 'New Name'})
        assert ok is False
        assert 'not found' in d['error'].lower()

    @patch('app.models.category.Category.updateIfExists', return_value='name_taken')
    def test_update_duplicate_name_fails(self, _):
        """Cannot update to a name that already exists."""
        ok, d = CategoryController.updateCategory(1, {'category_name': 'Health'})
        assert ok is False
        assert 'exists' in d['error'].lower()

    @patch('app.models.category.Category.updateIfExists', return_value=True)
    def test_update_success(self, _):
        """Successfully updates a category."""
        ok, d = CategoryController.updateCategory(1, {'category_name': 'New Name'})
        assert ok is True
        assert d['status'] == 'success'

    @patch('app.models.category.Category.updateIfExists', return_value=True)
    def test_update_description_only(self, _):
        """Can update description without changing name."""
        ok, d = CategoryController.updateCategory(1, {'description': 'New description'})
        assert ok is True

    def test_short_name_fails(self, client, pm_token):
        """Updated name must be at least 2 characters."""
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_pm_account()):
            res = client.put('/api/categories/1',
                json={'category_name': 'A'},
                headers={'Authorization': f'Bearer {pm_token}'})
        assert res.status_code == 400


# ══════════════════════════════════════════════════════════════
# PM-04 — DELETE CATEGORY
# ══════════════════════════════════════════════════════════════

class TestDeleteCategory:
    """PM-04 — Platform Manager deletes a FSA category."""

    @patch('app.models.category.Category.deleteIfExists', return_value='not_found')
    def test_delete_not_found(self, _):
        """Returns error if category not found."""
        ok, d = CategoryController.deleteCategory(999)
        assert ok is False
        assert 'not found' in d['error'].lower()

    @patch('app.models.category.Category.deleteIfExists', return_value=True)
    def test_delete_success(self, _):
        """Successfully deletes a category."""
        ok, d = CategoryController.deleteCategory(1)
        assert ok is True
        assert d['status'] == 'success'

    @patch('app.models.category.Category.deleteIfExists', return_value=True)
    def test_delete_returns_category_id(self, _):
        """Delete response includes category_id."""
        ok, d = CategoryController.deleteCategory(1)
        assert ok is True
        assert d['category_id'] == 1


# ══════════════════════════════════════════════════════════════
# PM-05 — SEARCH CATEGORY
# ══════════════════════════════════════════════════════════════

class TestSearchCategory:
    """PM-05 — Platform Manager searches for a FSA category."""

    def test_empty_query_fails(self, client, pm_token):
        """Empty search query should fail."""
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_pm_account()):
            res = client.get('/api/categories/?query=',
                headers={'Authorization': f'Bearer {pm_token}'})
        assert res.status_code == 400

    @patch('app.models.category.Category.searchCategories', return_value=[])
    def test_no_results(self, _):
        """Returns error if no matching categories."""
        ok, d = CategoryController.searchCategory('xyz')
        assert ok is False
        assert 'no categories' in d['error'].lower()

    @patch('app.models.category.Category.searchCategories')
    def test_search_success(self, mock_search):
        """Returns matching categories."""
        mock_search.return_value = [make_category()]
        ok, d = CategoryController.searchCategory('Edu')
        assert ok is True
        assert len(d['categories']) == 1

    @patch('app.models.category.Category.searchCategories')
    def test_search_partial_match(self, mock_search):
        """Search works with partial name."""
        mock_search.return_value = [
            make_category(name='Education'),
            make_category(category_id=2, name='Environment')
        ]
        ok, d = CategoryController.searchCategory('E')
        assert ok is True
        assert len(d['categories']) == 2