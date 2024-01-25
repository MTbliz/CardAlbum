import os

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, DecimalField, IntegerField, FileField
from wtforms.validators import ValidationError

from src.models import CardColorEnum, CardRarity, CardSet, CardMana, CardQuality


class CardsFiltersForm(FlaskForm):
    set = SelectField('Set:', choices=[(set.name, set.value) for set in CardSet])
    color = SelectField('Color:', choices=[(color.name, color.value) for color in CardColorEnum])
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

    def validate_title(self, field):
        if not os.path.exists(f'src/static/img/{field.data}.jpg'):
            raise ValidationError("Invalid title input.")

    def validate_mana(self, field):
        if not CardMana(str(field.data)).value:
            raise ValidationError("Invalid mana input.")

    def validate_set(self, field):
        if not CardSet(str(field.data)).value:
            raise ValidationError("Invalid set input.")

    def validate_rarity(self, field):
        if not CardRarity(str(field.data)).value:
            raise ValidationError("Invalid rarity input.")
