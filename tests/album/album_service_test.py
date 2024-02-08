import pytest
from werkzeug.exceptions import NotFound, Forbidden


def test_get_albums(app, album_service_with_mocked_repo):
    with app.app_context():

        # Call the method to test
        albums = album_service_with_mocked_repo.get_albums()

        # Assert that the returned value is a list
        assert isinstance(albums, list), "Returned value is not a list"

        # Assert that the list contains at least two elements
        assert len(albums) >= 2, "List does not contain at least two elements"


# Test for when the album exists and the user is authorized
def test_get_album_authorized(app, album_service_with_mocked_repo):
    with app.app_context():

        album = album_service_with_mocked_repo.get_album(1)

        assert album.title == "Test1"


# Test for when the album doesn't exist
def test_get_album_not_found(app, album_service_with_mocked_repo):
    with app.app_context():
        with pytest.raises(NotFound):
            album_service_with_mocked_repo.get_album(3)


# Test for when the user is not authorized
def test_get_album_unauthorized(app, album_service_with_mocked_repo):
    with app.app_context():
        with pytest.raises(Forbidden):
            album_service_with_mocked_repo.get_album(2)


def test_get_album_cards(app, album_service_with_mocked_repo):
    with app.app_context():
        user_cards = album_service_with_mocked_repo.get_album_cards("Test1", "title", "asc_title", {}, 1, 10)
        # Assert that the returned value is a list
        assert isinstance(user_cards, list), "Returned value is not a list"

        # Assert that the list contains at least two elements
        assert len(user_cards) >= 2, "List does not contain at least two elements"


def test_add_album_authorized(app, album_service_with_mocked_repo):
    with app.app_context():
        album = album_service_with_mocked_repo.get_album(1)
        result = album_service_with_mocked_repo.add_album(album)

        assert result is None


def test_add_album_unauthorized(app, album_service_with_mocked_repo):
    with app.app_context():
        album = album_service_with_mocked_repo.get_album(1)
        album.user_id = 2
        with pytest.raises(Forbidden):
            album_service_with_mocked_repo.add_album(album)


def test_delete_album_authorized(app, album_service_with_mocked_repo):
    with app.app_context():
        result = album_service_with_mocked_repo.delete_album(1)

        assert result is None


def test_delete_album_unauthorized(app, album_service_with_mocked_repo):
    with app.app_context():
        with pytest.raises(Forbidden):
            album_service_with_mocked_repo.delete_album(2)


# Test for when the album doesn't exist
def test_delete_album_not_found(app, album_service_with_mocked_repo):
    with app.app_context():
        with pytest.raises(NotFound):
            album_service_with_mocked_repo.delete_album(3)


def test_get_albums_by_user(app, album_service_with_mocked_repo, logged_in_user):
    with app.app_context():
        albums = album_service_with_mocked_repo.get_albums_by_user(logged_in_user.id)

        # Assert that the returned value is a list
        assert isinstance(albums, list), "Returned value is not a list"

        # Assert that the list contains at least two elements
        assert len(albums) >= 2, "List does not contain at least one elements"

        # Assert that the list contains at least two elements
        assert all(album.user_id == logged_in_user.id for album in albums), "Elements don't have same user_id"


def test_get_albums_by_user_unauthorized(app, album_service_with_mocked_repo):
    with app.app_context():
        with pytest.raises(Forbidden):
            album_service_with_mocked_repo.get_albums_by_user(2)


def test_get_albums_by_user_card(app, album_service_with_mocked_repo, logged_in_user):
    with app.app_context():
        albums = album_service_with_mocked_repo.get_albums_by_user_card(1)

        # Assert that the returned value is a list
        assert isinstance(albums, list), "Returned value is not a list"

        # Assert that the list contains at least two elements
        assert len(albums) >= 2, "List does not contain at least one elements"

        # Assert that the list contains at least two elements
        assert all(album.user_id == logged_in_user.id for album in albums), "Elements don't have same user_id"


def test_get_albums_by_user_card_wrong_albums(app, album_service_with_mocked_repo, logged_in_user):
    with app.app_context():
        with pytest.raises(Forbidden):
            album_service_with_mocked_repo.get_albums_by_user_card(2)

