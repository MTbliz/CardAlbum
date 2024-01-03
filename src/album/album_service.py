from src.album.album_repository import AlbumRepository


class AlbumService:

    def __init__(self):
        self.album_repository = AlbumRepository()

    def get_albums(self):
        return self.album_repository.get_albums()

    def get_album(self, album_id):
        return self.album_repository.get_album(album_id)

    def get_album_cards(self, album_title, field_sort, order, filters, page, ROWS_PER_PAGE):
        return self.album_repository.get_album_cards(album_title, field_sort, order, filters, page, ROWS_PER_PAGE)

    def add_album(self, album):
        return self.album_repository.add_album(album)

    def delete_album(self, album_id):
        return self.album_repository.delete_album(album_id)

    def get_albums_by_user(self, user_id):
        return self.album_repository.get_ablums_by_user(user_id)

    def get_albums_by_user_card(self, card_id):
        return self.album_repository.get_albums_by_user_card(card_id)