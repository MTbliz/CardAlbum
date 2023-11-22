from src.models import Card, Album
from src import db


class CardRepository:

    def get_cards(self):
        cards = Card.query.all()
        return cards

    def get_card(self, card_id):
        card = Card.query.filter_by(id=card_id).first()
        if not card:
            raise Exception("Card not found")
        return card

    def add_card(self, card: Card):
        db.session.add(card)
        db.session.commit()

    def delete_card(self, card_id):
        card = Card.query.filter_by(id=card_id).first()
        if not card:
            raise Exception("Card not found")
        db.session.delete(card)
        db.session.commit()


class AlbumRepository:

    def get_albums(self):
        albums = Album.query.all()
        return albums

    def get_album(self, album_id):
        album = Album.query.filter_by(id=album_id).first()
        if not album:
            raise Exception("Album not found")
        return album

    def add_album(self, album: Album):
        db.session.add(album)
        db.session.commit()

    def delete_album(self, album_id):
        album = Album.query.filter_by(id=album_id).first()
        if not album:
            raise Exception("Album not found")
        db.session.delete(album)
        db.session.commit()
