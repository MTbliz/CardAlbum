from src import db
from src.models import UserCard, Card, CardDetails, CardColorEnum, CardColor, Album


class UserCardRepository:

    def get_cards(self, user_id: int, field_sort: str, order: str, filters: dict[str, str], page: int,
                  ROWS_PER_PAGE: int):
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

    def get_card(self, card_id: int) -> UserCard:
        user_card: UserCard = UserCard.query.filter_by(id=card_id).first()
        return user_card

    def add_card(self, user_card: UserCard) -> None:
        db.session.add(user_card)
        db.session.commit()

    def delete_card(self, user_card_id: int) -> bool:
        user_card: UserCard = UserCard.query.filter_by(id=user_card_id).first()
        if not user_card:
            return False
        else:
            user_card.user = None
            db.session.delete(user_card)
            db.session.commit()
            return True

    def check_if_user_card_exists(self, card_id: int, user_id: int) -> bool:
        user_card: UserCard = UserCard.query.filter_by(card_id=card_id, user_id=user_id).first()
        return True if user_card else False

    def remove_user_card_from_album(self, card_id: int, album_id: int) -> bool:
        album: Album = Album.query.get(album_id)
        if not album:
            return False
        else:
            user_card: UserCard = UserCard.query.get(card_id)
            album.user_cards.remove(user_card)
            db.session.commit()
            return True

    def add_user_card_to_album(self, card_id: int, album_id: int) -> None:
        album: Album = Album.query.get(album_id)
        user_card: UserCard = UserCard.query.get(card_id)
        album.user_cards.append(user_card)
        db.session.commit()
