from sqlalchemy import desc

from src import db
from src.models import Card, CardDetails, CardSet, CardColorEnum, CardColor


class CardRepository:

    def get_cards(self, field_sort: str, order: str, filters: dict[str, str], page: int, ROWS_PER_PAGE: int):
        if order == "asc":
            query = Card.query.join(CardDetails)

            # Apply the filters
            for attr, value in filters.items():
                if attr == 'CardDetails.colors' and hasattr(CardColorEnum, value):
                    query = query.filter(CardDetails.colors.any(CardColor.color == CardColorEnum[value]))
                else:
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

    def get_card(self, card_id: int) -> Card:
        card = Card.query.filter_by(id=card_id).first()
        if not card:
            raise Exception("Card not found")
        return card

    def get_card_by_title(self, title: str) -> Card:
        card = Card.query.filter_by(title=title).first()
        if not card:
            raise Exception("Card not found")
        return card

    def add_card(self, card: Card) -> None:
        db.session.add(card)
        db.session.commit()

    def delete_card(self, card_id: int) -> None:
        card: Card = Card.query.filter_by(id=card_id).first()
        if not card:
            raise Exception("Card not found")
        db.session.delete(card)
        db.session.commit()

    def get_set_value_by_name(self, set_name: str) -> str:
        return CardSet[set_name].value

    def check_if_card_exist(self, searched_title: str, searched_set: str) -> bool:
        card = Card.query.join(CardDetails)\
            .filter(Card.title ==searched_title, CardDetails.set == searched_set).first()
        if card:
            return True
        else:
            False
