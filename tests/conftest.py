import pytest
from flask_login import login_user, logout_user

from src import create_app
from src.album.album_service import AlbumService
from src.album.album_controller import AlbumController
from src.models import Album, User, UserCard, CardQuality
from src.user.user_service import UserService


@pytest.fixture(scope="module")
def app():
    yield create_app()


@pytest.fixture(scope="module")
def client(app):
    return app.test_client()


@pytest.fixture
def album_service():
    return AlbumService()


@pytest.fixture()
def albums(logged_in_user):
    album1 = Album()
    album1.id = 1
    album1.title = "Test1"
    album1.user_cards = []
    album1.user_id = logged_in_user.id

    album2 = Album()
    album2.id = 2
    album2.title = "Test2"
    album2.user_cards = []
    album2.user_id = 2

    album3 = Album()
    album3.id = 3
    album3.title = "Test3"
    album3.user_cards = []
    album3.user_id = logged_in_user.id
    yield [album1, album2, album3]


@pytest.fixture()
def user_cards(logged_in_user):
    user_card1 = UserCard()
    user_card1.id = 1
    user_card1.price = 10.0
    user_card1.availability = 100,
    user_card1.quality = CardQuality.MINT,
    user_card1.card_id = 1,
    user_card1.user_id = logged_in_user.id

    user_card2 = UserCard()
    user_card2.id = 2
    user_card2.price = 20.0
    user_card2.availability = 200,
    user_card2.quality = CardQuality.MINT,
    user_card2.card_id = 1,
    user_card2.user_id = logged_in_user.id
    yield [user_card1, user_card2]


@pytest.fixture
def album_repository(logged_in_user, albums, user_cards):
    class MockAlbumRepository:

        def get_albums(self):
            return albums

        def get_album(self, album_id):
            if album_id == 1:
                return albums[0]
            elif album_id == 2:
                return albums[1]
            else:
                return None

        def add_album(self, album):
            return None

        def delete_album(self, album_id):
            if album_id == 1:
                return True
            else:
                return False

        def get_album_cards(self, album_title, field_sort, order, filters, page, ROWS_PER_PAGE):
            return user_cards

        def get_ablums_by_user(self, user_id):
            return [album for album in albums if album.user_id == logged_in_user.id]

        def get_albums_by_user_card(self, card_id):
            if card_id == 1:
                return [album for album in albums if album.user_id == logged_in_user.id]
            else:
                return albums

    return MockAlbumRepository()


@pytest.fixture
def album_service_with_mocked_repo(album_service, album_repository):
    album_service.album_repository = album_repository
    return album_service


@pytest.fixture(scope="module")
def logged_in_user(app, client):
    with app.test_request_context():
        user_service = UserService()
        user: User = user_service.get_user_by_email('testuser@example.com')
        if user and user.check_password('123456'):
            login_user(user)
        yield user
        logout_user()


@pytest.fixture
def album_controller():
    return AlbumController()


@pytest.fixture
def album_service_mocked(logged_in_user, albums):
    class MockAlbumService:

        def get_album(self, album_id):
            return albums[0]

    return MockAlbumService()


@pytest.fixture
def user_card_service_mocked(logged_in_user, user_cards):
    class MockUserCardService:

        def remove_user_card_from_album(self, card_id, album_id):
            return None

    return MockUserCardService()


@pytest.fixture
def album_controller_with_mocked_services(album_controller, user_card_service_mocked, album_service_mocked):
    album_controller.user_card_service = user_card_service_mocked
    album_controller.album_service = album_service_mocked
    return album_controller
