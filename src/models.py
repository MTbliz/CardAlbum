from src import db


albums_cards = db.Table('albums_cards', db.Model.metadata,
                             db.Column('album_id', db.Integer, db.ForeignKey('albums.id')),
                             db.Column('card_id', db.Integer, db.ForeignKey('cards.id'))
                        )


class Album(db.Model):

    __tablename__ = "albums"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    cards = db.relationship("Card", secondary=albums_cards, backref='albums')


class Card(db.Model):

    __tablename__ = "cards"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    price = db.Column(db.Float(), nullable=False)
    availability = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)

    def __repr__(self) -> str:
        return f'{self.id}'