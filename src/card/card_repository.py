from src.models import Card
from sqlalchemy import func, desc, and_
from src import db


class CardRepository:

    def get_cards(self, field_sort, order, filters, page, ROWS_PER_PAGE):
        if order == "asc":
            return Card.query\
                .filter_by(**filters)\
                .order_by(field_sort, Card.availability.asc())\
                .paginate(page=page, per_page=ROWS_PER_PAGE)
        else:
            return Card.query.filter_by(**filters)\
                .order_by(desc(field_sort, Card.availability.asc()))\
                .paginate(page=page, per_page=ROWS_PER_PAGE)

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
