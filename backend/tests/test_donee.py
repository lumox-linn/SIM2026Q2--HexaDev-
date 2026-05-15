"""
tests/test_donee.py
====================
Sprint 5 — DN-01 to DN-05: Donee Browse & Favourites
"""
import pytest
from unittest.mock import patch
from app.services.donee_controller import (
    BrowseActivityController,
    SaveFavouriteController,
    ViewFavouriteController,
    SearchFavouriteController,
)


def make_activity(activity_id=1, title='Help the Children', status='active', user_id=3):
    return {
        'activity_id':   activity_id,
        'title':         title,
        'description':   'A fundraising activity',
        'category_id':   1,
        'category_name': 'Education',
        'created_by':    user_id,
        'creator':       'fr01',
        'target_amount': 5000.00,
        'amount_raised': 1250.00,
        'start_date':    '2026-05-01',
        'end_date':      '2026-07-31',
        'status':        status,
        'created_at':    '2026-05-02 10:00:00'
    }

def make_favourite(favourite_id=1, activity_id=1, user_id=4):
    fav = make_activity(activity_id=activity_id)
    fav['favourite_id'] = favourite_id
    fav['saved_at']     = '2026-05-10 10:00:00'
    return fav

def make_donee_account():
    return {
        'user_id': 4, 'username': 'donee01', 'role': 'donee',
        'isActive': 1, 'email': None, 'dob': None, 'profile_picture': None,
    }

@pytest.fixture
def donee_token(app):
    from app.utils.auth_utils import generate_token
    return generate_token(user_id=4, role='donee')


# ══════════════════════════════════════════════════════════════
# DN-01 — SEARCH ACTIVITIES — BrowseActivityController
# ══════════════════════════════════════════════════════════════

class TestSearchActivities:

    def test_empty_query_fails(self, client, donee_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_donee_account()):
            res = client.get('/api/donee/activities?query=',
                headers={'Authorization': f'Bearer {donee_token}'})
        assert res.status_code == 400

    @patch('app.models.activity.Activity.search', return_value=[])
    def test_no_results(self, _):
        ok, d = BrowseActivityController.searchActivities('xyz')
        assert ok is False and 'no activities' in d['error'].lower()

    @patch('app.models.activity.Activity.search')
    def test_search_success(self, mock_search):
        mock_search.return_value = [make_activity()]
        ok, d = BrowseActivityController.searchActivities('help')
        assert ok is True and len(d['activities']) == 1

    @patch('app.models.activity.Activity.search')
    def test_search_only_returns_active(self, mock_search):
        mock_search.return_value = [
            make_activity(activity_id=1, status='active'),
            make_activity(activity_id=2, status='suspended'),
        ]
        ok, d = BrowseActivityController.searchActivities('help')
        assert ok is True
        for a in d['activities']:
            assert a['status'] == 'active'


# ══════════════════════════════════════════════════════════════
# DN-02 — VIEW ACTIVITIES — BrowseActivityController
# ══════════════════════════════════════════════════════════════

class TestBrowseActivities:

    @patch('app.models.activity.Activity.getAll', return_value=[])
    def test_get_all_empty(self, _):
        ok, d = BrowseActivityController.getAllActivities()
        assert ok is True and d['activities'] == []

    @patch('app.models.activity.Activity.getAll')
    def test_get_all_returns_active_only(self, mock_get):
        mock_get.return_value = [
            make_activity(activity_id=1, status='active'),
            make_activity(activity_id=2, status='suspended'),
        ]
        ok, d = BrowseActivityController.getAllActivities()
        assert ok is True
        assert len(d['activities']) == 1
        assert d['activities'][0]['status'] == 'active'

    @patch('app.models.activity.Activity.findById', return_value=None)
    def test_view_not_found(self, _):
        ok, d = BrowseActivityController.viewActivity(999)
        assert ok is False and 'not found' in d['error'].lower()

    @patch('app.models.activity.Activity.findById')
    def test_view_success(self, mock_find):
        mock_find.return_value = make_activity()
        ok, d = BrowseActivityController.viewActivity(1)
        assert ok is True and d['activity']['title'] == 'Help the Children'

    @patch('app.models.activity.Activity.findById')
    def test_view_returns_correct_fields(self, mock_find):
        mock_find.return_value = make_activity()
        ok, d = BrowseActivityController.viewActivity(1)
        assert ok is True
        for field in ['activity_id', 'title', 'target_amount', 'amount_raised', 'status']:
            assert field in d['activity']


# ══════════════════════════════════════════════════════════════
# DN-03 — SAVE FAVOURITE — SaveFavouriteController
# ══════════════════════════════════════════════════════════════

class TestSaveFavourite:

    def test_no_activity_id_fails(self, client, donee_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_donee_account()):
            res = client.post('/api/donee/favourites',
                json={},
                headers={'Authorization': f'Bearer {donee_token}'})
        assert res.status_code == 400

    @patch('app.models.favourite.Favourite.exists', return_value=True)
    def test_already_saved_fails(self, _):
        ok, d = SaveFavouriteController.saveFavourite(4, 1)
        assert ok is False and 'already' in d['error'].lower()

    @patch('app.models.favourite.Favourite.activityExists', return_value=False)
    @patch('app.models.favourite.Favourite.exists', return_value=False)
    def test_activity_not_found(self, _, __):
        ok, d = SaveFavouriteController.saveFavourite(4, 999)
        assert ok is False and 'not found' in d['error'].lower()

    @patch('app.models.favourite.Favourite.activityExists', return_value=True)
    @patch('app.models.favourite.Favourite.exists', return_value=False)
    def test_save_success(self, _, __):
        ok, d = SaveFavouriteController.saveFavourite(4, 1)
        assert ok is True and d['status'] == 'success'

    @patch('app.models.favourite.Favourite.exists', return_value=False)
    def test_remove_not_in_favourites(self, _):
        ok, d = SaveFavouriteController.removeFavourite(4, 1)
        assert ok is False and 'not in' in d['error'].lower()

    @patch('app.models.favourite.Favourite.exists', return_value=True)
    def test_remove_success(self, _):
        ok, d = SaveFavouriteController.removeFavourite(4, 1)
        assert ok is True and d['status'] == 'success'


# ══════════════════════════════════════════════════════════════
# DN-04 — SEARCH FAVOURITES — SearchFavouriteController
# ══════════════════════════════════════════════════════════════

class TestSearchFavourites:

    def test_empty_query_fails(self, client, donee_token):
        with patch('app.utils.auth_utils.UserAccount.getProfilePicture', return_value=None), \
             patch('app.utils.auth_utils.UserAccount.findById', return_value=make_donee_account()):
            res = client.get('/api/donee/favourites?query=',
                headers={'Authorization': f'Bearer {donee_token}'})
        assert res.status_code == 400

    @patch('app.models.favourite.Favourite.search', return_value=[])
    def test_no_results(self, _):
        ok, d = SearchFavouriteController.searchFavourites('xyz', 4)
        assert ok is False and 'no favourites' in d['error'].lower()

    @patch('app.models.favourite.Favourite.search')
    def test_search_success(self, mock_search):
        mock_search.return_value = [make_favourite()]
        ok, d = SearchFavouriteController.searchFavourites('help', 4)
        assert ok is True and len(d['favourites']) == 1


# ══════════════════════════════════════════════════════════════
# DN-05 — VIEW FAVOURITES — ViewFavouriteController
# ══════════════════════════════════════════════════════════════

class TestViewFavourites:

    @patch('app.models.favourite.Favourite.getAll', return_value=[])
    def test_get_all_empty(self, _):
        ok, d = ViewFavouriteController.getAllFavourites(4)
        assert ok is True and d['favourites'] == []

    @patch('app.models.favourite.Favourite.getAll')
    def test_get_all_returns_favourites(self, mock_get):
        mock_get.return_value = [make_favourite(), make_favourite(favourite_id=2, activity_id=2)]
        ok, d = ViewFavouriteController.getAllFavourites(4)
        assert ok is True and len(d['favourites']) == 2

    @patch('app.models.favourite.Favourite.getAll')
    def test_favourites_have_correct_fields(self, mock_get):
        mock_get.return_value = [make_favourite()]
        ok, d = ViewFavouriteController.getAllFavourites(4)
        assert ok is True
        fav = d['favourites'][0]
        for field in ['activity_id', 'title', 'target_amount', 'favourite_id', 'saved_at']:
            assert field in fav
