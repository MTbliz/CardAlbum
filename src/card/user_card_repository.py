from src.models import UserCard, Card, CardDetails, CardSet, CardColorEnum, CardColor, Album
from sqlalchemy import func, desc, and_, asc
from src import db


class UserCardRepository:

    def get_cards(self, user_id, field_sort, order, filters, page, ROWS_PER_PAGE):
        if order == "asc":
            query = UserCard.query.filter_by(user_id=user_id).join(Card).join(CardDetails)

            # Apply the filters
            for attr, value in filters.items():
                if attr == 'CardDetails.colors' and hasattr(CardColorEnum, value):
                    query = query.filter(CardDetails.colors.any(CardColor.color == CardColorEnum[value]))
                elif attr == 'Card.title' or attr == 'Card.type':
                    query = query.filter(getattr(Card, attr.split('.')[1]) == value)
                else:
                    query = query.filter(
                        getattr(CardDetails if 'CardDetails' in attr else UserCard, attr.split('.')[1]) == value)
            query = query.order_by(field_sort, UserCard.availability.asc())
            return query.paginate(page=page, per_page=ROWS_PER_PAGE, error_out=False)

    def get_card(self, card_id):
        user_card = UserCard.query.filter_by(id=card_id).first()
        if not user_card:
            raise Exception("Card not found")
        return user_card

    def add_card(self, user_card: UserCard):
        db.session.add(user_card)
        db.session.commit()

    def delete_card(self, user_card_id):
        user_card = UserCard.query.filter_by(id=user_card_id).first()
        user_card.user = None
        if not user_card:
            raise Exception("Card not found")
        db.session.delete(user_card)
        db.session.commit()

    def check_if_user_card_exists(self, card_id, user):
        user_card = UserCard.query.filter_by(card_id=card_id, user_id=user.id).first()
        return True if user_card else False

    def remove_user_card_from_album(self, card_id, album_id):
        album = Album.query.get(album_id)
        user_card = UserCard.query.get(card_id)
        album.user_cards.remove(user_card)
        db.session.commit()

    def add_user_card_to_album(self, card_id, album_id):
        album = Album.query.get(album_id)
        user_card = UserCard.query.get(card_id)
        album.user_cards.append(user_card)
        db.session.commit()

