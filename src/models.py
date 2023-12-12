from src import db
import enum
from sqlalchemy import Enum


class CardSet(enum.Enum):

    ALL = 'All'
    SET1 = "Wilds of Eldraine"
    SET2 = "March of the Machine: The Aftermath"
    SET3 = "March of the Machine"
    SET4 = "Phyrexia: All Will Be One"
    SET5 = "The Brothers' War"
    SET6 = "Dominaria Unite"
    SET7 = "Streets of New Capenna"
    SET8 = "Kamigawa: Neon Dynast"
    SET9 = "Innistrad: Crimson Vow"
    SET10 = "Innistrad: Midnight Hunt"


class CardRarity(enum.Enum):

    ALL = 'All'
    COMMON = 'Common'
    UNCOMMON = 'Uncommon'
    RARE = 'Rare'
    MYTHIC_RARE = 'Mythic'


class CardColorEnum(enum.Enum):

    ALL = 'All'
    BLACK = 'black'
    BLUE = 'blue'
    GREEN = 'green'
    RED = 'red'
    WHITE = 'white'
    COLORLESS = 'colorless'


class CardMana(enum.Enum):

    ALL = 'All'
    ZERO = '0'
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    TEN = '10'


class CardQuality(enum.Enum):

    MINT = 'Mint'
    NEAR_MINT = 'Near Mint'
    GOOD_LIGHTLY_PLAYED = 'Good (Lightly Played)'
    PLAYED = 'Played'
    HEAVILY_PLAYED = 'Heavily Played'
    POOR = 'Poor'


albums_user_cards = db.Table('albums_user_cards', db.Model.metadata,
                             db.Column('album_id', db.Integer, db.ForeignKey('albums.id')),
                             db.Column('user_card_id', db.Integer, db.ForeignKey('user_cards.id'))
                             )

colors_card_details = db.Table('colors_card_details', db.Model.metadata,
                               db.Column("card_color_id", db.Integer, db.ForeignKey('card_colors.id'), primary_key=True),
                               db.Column('card_details_id', db.Integer, db.ForeignKey('card_details.id'), primary_key=True)
                      )


class Album(db.Model):

    __tablename__ = "albums"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    user_cards = db.relationship("UserCard", secondary=albums_user_cards, backref='albums')


class UserCard(db.Model):

    __tablename__ = "user_cards"

    id = db.Column(db.Integer(), primary_key=True)

    price = db.Column(db.Float(), nullable=False)
    availability = db.Column(db.Integer(), nullable=False)
    quality = db.Column(Enum(CardQuality))
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))


class Card(db.Model):

    __tablename__ = "cards"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    card_details = db.relationship('CardDetails', backref='card', uselist=False)
    user_cards = db.relationship('UserCard', backref='card')

    def __repr__(self) -> str:
        return f'{self.id}'


class CardDetails(db.Model):

    __tablename__ = "card_details"

    id = db.Column(db.Integer(), primary_key=True)
    mana = db.Column(Enum(CardMana))
    rarity = db.Column(Enum(CardRarity))
    set = db.Column(Enum(CardSet))
    type = db.Column(db.String(), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'), nullable=False)
    colors = db.relationship("CardColor", secondary=colors_card_details)


class CardColor(db.Model):

    __tablename__ = 'card_colors'

    id = db.Column(db.Integer(), primary_key=True)
    color = db.Column(Enum(CardColorEnum), nullable=False)




