from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, DecimalField, IntegerField, FileField
from src.models import CardColor, CardRarity, CardSet, CardMana, CardQuality


class CardsFiltersForm(FlaskForm):
    set = SelectField('Set:', choices=[(set.name, set.value) for set in CardSet])
    color = SelectField('Color:', choices=[(color.name, color.value) for color in CardColor])
    mana = SelectField('Mana:', choices=[(mana.name, mana.value) for mana in CardMana])
    rarity = SelectField('Rarity:', choices=[(rarity.name, rarity.value) for rarity in CardRarity])
    submit = SubmitField('Submit')


class CardSearchForm(FlaskForm):
    title = StringField('Title:')
    set = SelectField('Set:', choices=[(set.name, set.value) for set in CardSet])
    submit = SubmitField('Get Card')


class CreateCardForm(FlaskForm):
    title = StringField('Title:', render_kw={'disabled': ''})
    price = DecimalField('Price:')
    availability = IntegerField('Availability:')
    color = StringField('Color:', render_kw={'disabled': ''})
    mana = IntegerField('Mana:', render_kw={'disabled': ''})
    rarity = StringField('Rarity:', render_kw={'disabled': ''})
    set = StringField('Set:', render_kw={'disabled': ''})
    type = StringField('Type:', render_kw={'disabled': ''})
    quality = SelectField('Quality:', choices=[(quality.name, quality.value) for quality in CardQuality])
    image = FileField('Image:')
    submit = SubmitField('Add Card')


