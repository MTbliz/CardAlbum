from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, DecimalField


class BasketSellForm(FlaskForm):
    total_price = DecimalField('Total Price:')
    customer = SelectField('Customer:')
    submit = SubmitField('Sell')
