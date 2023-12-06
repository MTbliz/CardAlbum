from src.models import Card, CardDetails, CardSet
from sqlalchemy import func, desc, and_, asc
from src import db


class CardRepository:

    def get_cards(self, field_sort, order, filters, page, ROWS_PER_PAGE):
        if order == "asc":
            query = Card.query.join(CardDetails)

            # Apply the filters
            for attr, value in filters.items():
                query = query.filter(
                    getattr(CardDetails if 'CardDetails' in attr else Card, attr.split('.')[1]) == value)
            query = query.order_by(field_sort, Card.availability.asc())
            return query.paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)

        else:
            query = Card.query.join(CardDetails)

            # Apply the filters
            for attr, value in filters.items():
                query = query.filter(
                    getattr(CardDetails if 'CardDetails' in attr else Card, attr.split('.')[1]) == value)
            query = query.order_by(desc(field_sort, Card.availability.asc()))
            return query.paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)

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

    def get_set_value_by_name(self, set_name):
        return CardSet[set_name].value
