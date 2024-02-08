def test_create_album_controller(app, client, logged_in_user):
    response = client.post('/albums/album', data={'title': 'Test Album'}, follow_redirects=True)

    assert response.status_code == 200
    assert b'Test Album' in response.data
    assert b'Create Album' in response.data
    assert b'Title:' in response.data


def test_delete_album_controller(app, client, logged_in_user):
    response = client.get('/albums/album/delete')

    assert b'Delete Album' in response.data
    assert b'Album:'

    assert response.status_code == 200


def test_album_cards_controller(app, client, logged_in_user):
    response = client.get('/albums/album_cards')

    assert b'rarity' in response.data
    assert b'mana' in response.data
    assert b'set' in response.data
    assert b'color' in response.data

    assert response.status_code == 200


def test_remove_user_card_from_album(app, client, logged_in_user, album_controller_with_mocked_services):
    response = album_controller_with_mocked_services.remove_user_card_from_album(1, 1, "test")

    assert b'<a href="/albums/test">' in response.data

    assert response.status_code == 302

