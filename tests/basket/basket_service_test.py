import pytest
from werkzeug.exceptions import NotFound, Forbidden
from src.models import Basket


def test_get_basket_authorized(app, logged_in_user, basket_service_with_mocked_repo):
    with app.app_context():

        # Call the method to test
        basket = basket_service_with_mocked_repo.get_basket(1)

        # Assert that the returned value is a list
        assert isinstance(basket, Basket), "Returned value is not a Basket"
        assert basket.user_id == logged_in_user.id


# Test for when the album doesn't exist
def test_get_basket_not_found(app, basket_service_with_mocked_repo):
    with app.app_context():
        with pytest.raises(NotFound):
            basket_service_with_mocked_repo.get_basket(3)


# Test for when the user is not authorized
def test_get_basket_unauthorized(app, basket_service_with_mocked_repo):
    with app.app_context():
        with pytest.raises(Forbidden):
            basket_service_with_mocked_repo.get_basket(2)


def test_get_basket_by_user_authorized(app, logged_in_user, basket_service_with_mocked_repo):
    with app.app_context():

        # Call the method to test
        basket = basket_service_with_mocked_repo.get_basket_by_user(1)

        # Assert that the returned value is a list
        assert isinstance(basket, Basket), "Returned value is not a Basket"
        assert basket.user_id == logged_in_user.id


# Test for when the album doesn't exist
def test_get_basket_by_user_not_found(app, basket_service_with_mocked_repo):
    with app.app_context():
        with pytest.raises(NotFound):
            basket_service_with_mocked_repo.get_basket_by_user(3)


# Test for when the user is not authorized
def test_get_basket_by_user_unauthorized(app, basket_service_with_mocked_repo):
    with app.app_context():
        with pytest.raises(Forbidden):
            basket_service_with_mocked_repo.get_basket_by_user(2)


def test_add_user_card_to_basket_authorized(app, logged_in_user, basket_service_with_mocked_repo):
    with app.app_context():

        # Call the method to test
        result = basket_service_with_mocked_repo.add_user_card_to_basket(1, 1)

        assert result is None


# Test for when the album doesn't exist
def test_add_user_card_to_basket_not_found(app, basket_service_with_mocked_repo):
    with app.app_context():
        with pytest.raises(NotFound):
            basket_service_with_mocked_repo.add_user_card_to_basket(3, 1)


# Test for when the user is not authorized
def test_add_user_card_to_basket_unauthorized(app, basket_service_with_mocked_repo):
    with app.app_context():
        with pytest.raises(Forbidden):
            basket_service_with_mocked_repo.add_user_card_to_basket(2, 1)


def test_clear_basket_authorized(app, logged_in_user, basket_service_with_mocked_repo):
    with app.app_context():

        # Call the method to test
        result = basket_service_with_mocked_repo.clear_basket(logged_in_user.id)

        assert result is None


# Test for when the user is not authorized
def test_clear_basket_unauthorized(app, basket_service_with_mocked_repo):
    with app.app_context():
        with pytest.raises(Forbidden):
            basket_service_with_mocked_repo.clear_basket(10)
