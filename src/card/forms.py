from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from src.models import CardColor, CardRarity, CardSet, CardMana


class CardsFiltersForm(FlaskForm):
    set = SelectField('Set:', choices=[(set.name, set.value) for set in CardSet])
    color = SelectField('Color:', choices=[(color.name, color.value) for color in CardColor])
    mana = SelectField('Mana:', choices=[(mana.name, mana.value) for mana in CardMana])
    rarity = SelectField('Rarity:', choices=[(rarity.name, rarity.value) for rarity in CardRarity])
    submit = SubmitField('Submit')