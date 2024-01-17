from src.models import Album, UserCard, CardSet, CardColor, CardMana, Card, CardDetails, CardColorEnum,\
    albums_user_cards, User
from src import db


class AlbumRepository:

    def get_albums(self):
        albums = Album.query.all()
        return albums

    def get_album(self, album_id):
        album = Album.query.filter_by(id=album_id).first()
        if not album:
            raise Exception("Album not found")
        return album

    def get_album_cards(self, album_title, field_sort, order, filters, page, ROWS_PER_PAGE):
        if order == "asc":
            #query = Album.query.join(albums_user_cards).join(UserCard).join(Card).join(CardDetails)
            query = UserCard.query.join(albums_user_cards).join(Album).join(Card).join(CardDetails)
            query = query.filter(Album.title == album_title)

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


    def add_album(self, album: Album):
        db.session.add(album)
        db.session.commit()

    def delete_album(self, album_id):
        album: Album = Album.query.filter_by(id=album_id).first()
        if not album:
            raise Exception("Album not found")
        album.user_cards = []
        db.session.delete(album)
        db.session.commit()

    def get_ablums_by_user(self, user_id):
        # Add filter by user_id when user will be availabe in app
        user = User.query.get(user_id)
        albums = user.user_albums
        return albums

    def get_albums_by_user_card(self, card_id):
        user_card = UserCard.query.filter_by(id=card_id).first()
        return user_card.albums

