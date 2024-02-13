import enum
from typing import Optional

from flask_login import UserMixin
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash

from src import db, login_manager


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


class OrderStateSet(enum.Enum):
    STATUS_1 = "Started"
    STATUS_2 = "Accepted"
    STATUS_3 = "Sent"
    STATUS_4 = "Delivered"
    STATUS_5 = "Finalized"


albums_user_cards = db.Table('albums_user_cards', db.Model.metadata,
                             db.Column('album_id', db.Integer, db.ForeignKey('albums.id')),
                             db.Column('user_card_id', db.Integer, db.ForeignKey('user_cards.id'))
                             )

colors_card_details = db.Table('colors_card_details', db.Model.metadata,
                               db.Column("card_color_id", db.Integer, db.ForeignKey('card_colors.id'),
                                         primary_key=True),
                               db.Column('card_details_id', db.Integer, db.ForeignKey('card_details.id'),
                                         primary_key=True)
                               )

user_contacts = db.Table(
    'user_contacts',
    db.Model.metadata,
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('contact_id', db.Integer, db.ForeignKey('users.id'))
)


class Album(db.Model):
    __tablename__ = "albums"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    user_cards = db.relationship("UserCard", secondary=albums_user_cards, backref='albums')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class UserCard(db.Model):
    __tablename__ = "user_cards"

    id = db.Column(db.Integer(), primary_key=True)

    price = db.Column(db.Float(), nullable=False)
    availability = db.Column(db.Integer(), nullable=False)
    quality = db.Column(Enum(CardQuality))
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    basket_items = db.relationship('BasketItem', backref='user_card')


class Card(db.Model):
    __tablename__ = "cards"

    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    type = db.Column(db.String(), nullable=False)
    card_details = db.relationship('CardDetails', backref='card', uselist=False)
    user_cards = db.relationship('UserCard', backref='card')
    order_items = db.relationship('OrderItem', backref='card')

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


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128))
    user_albums = db.relationship('Album', backref='user')
    user_cards = db.relationship('UserCard', backref='user')
    basket = db.relationship('Basket', backref='user', uselist=False)

    contacts = db.relationship(
        'User',
        secondary=user_contacts,
        primaryjoin=(user_contacts.c.user_id == id),
        secondaryjoin=(user_contacts.c.contact_id == id),
        backref=db.backref('contacted_by', lazy='dynamic')
    )

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.basket: Basket = Basket()

    def set_password(self, password) -> None:
        self.password: str = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password, password)


@login_manager.user_loader
def load_user(user_id) -> User:
    return User.query.get(int(user_id))


@login_manager.request_loader
def request_loader(request) -> Optional[User]:
    email: str = request.form.get('email')
    user: User = User.query.filter_by(email=email).first()
    if user:
        return user
    else:
        return None


@login_manager.unauthorized_handler
def unauthorized_handler() -> str:
    return 'Unauthorized', 401


class Basket(db.Model):
    __tablename__ = 'baskets'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    basket_items = db.relationship('BasketItem', backref='basket')


class BasketItem(db.Model):
    __tablename__ = 'basket_items'

    id = db.Column(db.Integer, primary_key=True)
    basket_id = db.Column(db.Integer, db.ForeignKey('baskets.id'))
    user_card_id = db.Column(db.Integer, db.ForeignKey('user_cards.id'))
    quantity = db.Column(db.Integer)

    @property
    def total_price(self) -> float:
        return self.quantity * self.user_card.price


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer(), primary_key=True)

    total_price = db.Column(db.Float(), nullable=False)
    order_items = db.relationship('OrderItem', backref='order')
    order_state = db.Column(Enum(OrderStateSet))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    order_date = db.Column(db.DateTime, nullable=False)

    user = db.relationship('User', backref='orders_as_seller', foreign_keys=[user_id])
    customer = db.relationship('User', backref='orders_as_customer', foreign_keys=[customer_id])


class OrderItem(db.Model):
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    card_id = db.Column(db.Integer, db.ForeignKey('cards.id'))
    quantity = db.Column(db.Integer)
    quality = db.Column(Enum(CardQuality))
    total_price = db.Column(db.Float(), nullable=False)


class Invite(db.Model):

    __tablename__ = 'invites'

    id = db.Column(db.Integer, primary_key=True)
    invite_date = db.Column(db.DateTime, nullable=False)
    expiration_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    contact_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', backref='invites_send', foreign_keys=[user_id])
    contact = db.relationship('User', backref='invites_received', foreign_keys=[contact_id])

