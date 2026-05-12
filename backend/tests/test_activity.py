"""
tests/test_activity.py
======================
Sprint 4 — FR-01 to FR-05: Fundraising Activity Management
"""
import pytest
from unittest.mock import patch
from app.services.activity_controller import (
    CreateActivityController,
    ViewActivityController,
    UpdateActivityController,
    DeleteActivityController,
    SearchActivityController,
)


def make_activity(activity_id=1, title='Help the Children', user_id=3,
                  category_id=1, status='active'):
    return {
        'activity_id':   activity_id,
        'title':         title,
        'description':   'A fundraising activity',
        'category_id':   category_id,
        'category_name': 'Education',
        'created_by':    user_id,
        'creator':       'fr01',
        'status':        status,
        'created_at':    '2026-05-02 10:00:00'
    }

def make_fr_account():
    return {
        'user_id': 3, 'username': 'fr01', 'role': 'fund_raiser',
        'isActive': 1, 'email': None, 'dob': None, 'profile_picture': None,
    }

@pytest.fixture
def fr_token(app):
    from app.utils.auth_utils import generate_token
    return generate_token(user_id=3, role='fund_raiser')


# ══════════════════════════════════════════════════════════════
# FR-01 — CREATE ACTIVITY — CreateActivityController
# ══════════════════════════════════════════════════════════════

class TestCreateActivity:

    # Boundary tests
    def test_empty_title_fails(self, client, fr_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_fr_account()):
            res = client.post('/api/activities/',
                json={'title': ''},
                headers={'Authorization': f'Bearer {fr_token}'})
        assert res.status_code == 400
        assert 'title' in res.get_json()['error'].lower()

    def test_short_title_fails(self, client, fr_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_fr_account()):
            res = client.post('/api/activities/',
                json={'title': 'ab'},
                headers={'Authorization': f'Bearer {fr_token}'})
        assert res.status_code == 400

    def test_no_body_fails(self, client, fr_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_fr_account()):
            res = client.post('/api/activities/',
                headers={'Authorization': f'Bearer {fr_token}'})
        assert res.status_code in [400, 415]

    def test_non_fr_cannot_create(self, client):
        from app.utils.auth_utils import generate_token
        token = generate_token(user_id=1, role='admin')
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value={
                 'user_id': 1, 'username': 'admin01', 'role': 'admin',
                 'isActive': 1, 'email': None, 'dob': None, 'profile_picture': None
             }):
            res = client.post('/api/activities/',
                json={'title': 'Test Activity'},
                headers={'Authorization': f'Bearer {token}'})
        assert res.status_code == 403

    # Controller tests
    @patch('app.models.activity.Activity.existsByTitle', return_value=True)
    def test_duplicate_title_fails(self, _):
        ok, d = CreateActivityController.createActivity(
            {'title': 'Help the Children'}, user_id=3
        )
        assert ok is False
        assert 'already' in d['error'].lower()

    @patch('app.models.activity.Activity.existsByTitle', return_value=False)
    def test_create_success(self, _):
        ok, d = CreateActivityController.createActivity(
            {'title': 'Help the Children', 'description': 'A good cause'},
            user_id=3
        )
        assert ok is True and d['status'] == 'success'

    @patch('app.models.activity.Activity.existsByTitle', return_value=False)
    def test_create_returns_success_message(self, _):
        ok, d = CreateActivityController.createActivity(
            {'title': 'Save the Ocean'}, user_id=3
        )
        assert ok is True and 'Save the Ocean' in d['message']


# ══════════════════════════════════════════════════════════════
# FR-02 — VIEW ACTIVITY — ViewActivityController
# ══════════════════════════════════════════════════════════════

class TestViewActivity:

    @patch('app.models.activity.Activity.getAll', return_value=[])
    def test_get_all_empty(self, _):
        ok, d = ViewActivityController.getAllActivities(user_id=3)
        assert ok is True and d['activities'] == []

    @patch('app.models.activity.Activity.getAll')
    def test_get_all_returns_activities(self, mock_get):
        mock_get.return_value = [
            make_activity(),
            make_activity(activity_id=2, title='Feed the Poor')
        ]
        ok, d = ViewActivityController.getAllActivities(user_id=3)
        assert ok is True and len(d['activities']) == 2

    @patch('app.models.activity.Activity.findById', return_value=None)
    def test_view_not_found(self, _):
        ok, d = ViewActivityController.viewActivity(999)
        assert ok is False and 'not found' in d['error'].lower()

    @patch('app.models.activity.Activity.findById')
    def test_view_success(self, mock_find):
        mock_find.return_value = make_activity()
        ok, d = ViewActivityController.viewActivity(1)
        assert ok is True and d['activity']['title'] == 'Help the Children'

    @patch('app.models.activity.Activity.findById')
    def test_view_returns_correct_fields(self, mock_find):
        mock_find.return_value = make_activity()
        ok, d = ViewActivityController.viewActivity(1)
        assert ok is True
        for field in ['activity_id', 'title', 'description', 'category_id', 'status']:
            assert field in d['activity']


# ══════════════════════════════════════════════════════════════
# FR-03 — UPDATE ACTIVITY — UpdateActivityController
# ══════════════════════════════════════════════════════════════

class TestUpdateActivity:

    @patch('app.models.activity.Activity.findById', return_value=None)
    def test_update_not_found(self, _):
        ok, d = UpdateActivityController.updateActivity(999, 3, {'title': 'New'})
        assert ok is False and 'not found' in d['error'].lower()

    @patch('app.models.activity.Activity.findById')
    def test_update_unauthorized(self, mock_find):
        mock_find.return_value = make_activity(user_id=5)  # different user
        ok, d = UpdateActivityController.updateActivity(1, 3, {'title': 'New'})
        assert ok is False and 'only' in d['error'].lower()

    @patch('app.models.activity.Activity.findById')
    def test_update_success(self, mock_find):
        mock_find.return_value = make_activity(user_id=3)
        ok, d = UpdateActivityController.updateActivity(1, 3, {'title': 'Updated Title'})
        assert ok is True and d['status'] == 'success'

    @patch('app.models.activity.Activity.findById')
    def test_update_description_only(self, mock_find):
        mock_find.return_value = make_activity(user_id=3)
        ok, d = UpdateActivityController.updateActivity(1, 3, {'description': 'New desc'})
        assert ok is True

    def test_short_title_fails(self, client, fr_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_fr_account()):
            res = client.put('/api/activities/1',
                json={'title': 'ab'},
                headers={'Authorization': f'Bearer {fr_token}'})
        assert res.status_code == 400


# ══════════════════════════════════════════════════════════════
# FR-04 — DELETE ACTIVITY — DeleteActivityController
# ══════════════════════════════════════════════════════════════

class TestDeleteActivity:

    @patch('app.models.activity.Activity.findById', return_value=None)
    def test_delete_not_found(self, _):
        ok, d = DeleteActivityController.deleteActivity(999, 3)
        assert ok is False and 'not found' in d['error'].lower()

    @patch('app.models.activity.Activity.findById')
    def test_delete_unauthorized(self, mock_find):
        mock_find.return_value = make_activity(user_id=5)  # different user
        ok, d = DeleteActivityController.deleteActivity(1, 3)
        assert ok is False and 'only' in d['error'].lower()

    @patch('app.models.activity.Activity.findById')
    def test_delete_success(self, mock_find):
        mock_find.return_value = make_activity(user_id=3)
        ok, d = DeleteActivityController.deleteActivity(1, 3)
        assert ok is True and d['status'] == 'success'

    @patch('app.models.activity.Activity.findById')
    def test_delete_returns_activity_id(self, mock_find):
        mock_find.return_value = make_activity(user_id=3)
        ok, d = DeleteActivityController.deleteActivity(1, 3)
        assert ok is True and d['activity_id'] == 1


# ══════════════════════════════════════════════════════════════
# FR-05 — SEARCH ACTIVITY — SearchActivityController
# ══════════════════════════════════════════════════════════════

class TestSearchActivity:

    def test_empty_query_fails(self, client, fr_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_fr_account()):
            res = client.get('/api/activities/?query=',
                headers={'Authorization': f'Bearer {fr_token}'})
        assert res.status_code == 400

    @patch('app.models.activity.Activity.search', return_value=[])
    def test_no_results(self, _):
        ok, d = SearchActivityController.searchActivity('xyz', user_id=3)
        assert ok is False and 'no activities' in d['error'].lower()

    @patch('app.models.activity.Activity.search')
    def test_search_success(self, mock_search):
        mock_search.return_value = [make_activity()]
        ok, d = SearchActivityController.searchActivity('Help', user_id=3)
        assert ok is True and len(d['activities']) == 1

    @patch('app.models.activity.Activity.search')
    def test_search_partial_match(self, mock_search):
        mock_search.return_value = [
            make_activity(title='Help the Children'),
            make_activity(activity_id=2, title='Help the Elderly')
        ]
        ok, d = SearchActivityController.searchActivity('Help', user_id=3)
        assert ok is True and len(d['activities']) == 2
