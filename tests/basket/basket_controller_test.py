import json


def test_get_basket(app, client, logged_in_user):
    response = client.get('/basket', follow_redirects=True)

    assert b'quantity' in response.data
    assert b'price' in response.data
    assert b'title' in response.data

    assert response.status_code == 200


def test_add_user_card_to_basket(app, client, logged_in_user, basket_controller_with_mocked_services):
    response = basket_controller_with_mocked_services.add_user_card_to_basket(1, 1)

    assert 'Item added to basket' in response[0]

    assert response[1] == 200


def test_delete_basket_item(app, client, logged_in_user, basket_controller_with_mocked_services):
    response = basket_controller_with_mocked_services.delete_basket_item(1, 1)

    assert response.status_code == 302


def test_clear_basket(app, client, logged_in_user, basket_controller_with_mocked_services):
    response = basket_controller_with_mocked_services.clear_basket()

    assert response.status_code == 302


def test_update_basket_item_quantity(app, client, logged_in_user, basket_controller_with_mocked_services):
    response = basket_controller_with_mocked_services.update_basket_item_quantity(1, 1, 3)

    assert {"basket_count": 2} == json.loads(response[0].data)

    assert response[1] == 200
