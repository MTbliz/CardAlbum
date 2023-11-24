from src.models import Card
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
