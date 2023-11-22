from src.main.repository import CardRepository, AlbumRepository


class CardService:

    def __init__(self):
        self.card_repository = CardRepository()

    def get_cards(self):
        return self.card_repository.get_cards()

    def get_card(self, card_id):
        return self.card_repository.get_card(card_id)

    def add_card(self, card):
        return self.card_repository.add_card(card)

    def delete_card(self, card_id):
        return self.card_repository.delete_card(card_id)


class AlbumService:

    def __init__(self):
        self.album_repository = AlbumRepository()

    def get_albums(self):
        return self.album_repository.get_albums()

    def get_album(self, album_id):
        return self.album_repository.get_album(album_id)

    def add_album(self, album):
        return self.album_repository.add_album(album)

    def delete_album(self, album_id):
        return self.album_repository.delete_album(album_id)