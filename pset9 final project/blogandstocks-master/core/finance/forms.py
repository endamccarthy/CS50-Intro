import requests
import urllib.parse
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, FloatField
from wtforms.validators import DataRequired, NumberRange, ValidationError


def validateSymbol(form, field):
    # Contact API
    try:
        response = requests.get(f"https://api.iextrading.com/1.0/stock/{urllib.parse.quote_plus(field.data)}/quote")
        response.raise_for_status()
    except requests.RequestException:
        raise ValidationError('Invalid! Please choose a valid symbol.')


class QuoteForm(FlaskForm):
    symbol = StringField('Enter stock symbol:', validators=[DataRequired(), validateSymbol])
    submit = SubmitField('Quote')


class BuyForm(FlaskForm):
    symbol = StringField('Enter stock symbol:', validators=[DataRequired(), validateSymbol])
    shares = IntegerField('Enter amount of shares:', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Buy')


class SellForm(FlaskForm):
    symbol = SelectField('Enter stock symbol:', choices=[], validators=[DataRequired()])
    shares = IntegerField('Enter amount of shares:', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Sell')


class DepositForm(FlaskForm):
    deposit = FloatField('Amount ($):', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Make Deposit')