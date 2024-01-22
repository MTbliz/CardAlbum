import os

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, StringField, DecimalField, IntegerField, FileField
from wtforms.validators import ValidationError


class BasketSellForm(FlaskForm):
    total_price = DecimalField('Total Price:')
    customer = SelectField('Customer:')
    submit = SubmitField('Sell')