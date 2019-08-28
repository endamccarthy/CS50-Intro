import requests
import urllib.parse
from sqlalchemy import func
from flask import abort, render_template, request, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user
from core import db
from core.models import Post, User, Transaction
from core.finance.forms import QuoteForm, BuyForm, SellForm, DepositForm
from wtforms.validators import ValidationError


# 'finance' will be the name of the blueprint
finance = Blueprint('finance', __name__)


@finance.route("/finance")
@login_required
def index():
    tempRows = db.session.query(Transaction.symbol, func.sum(Transaction.quantity))\
        .group_by(Transaction.symbol)\
        .filter_by(user_id=current_user.id).all()
    tempRows = [i for i in tempRows if not (i[1] <= 0)]
    grandTotal = 0
    rows = []
    for tempRow in tempRows:
        company = lookup(tempRow[0])
        companyName = company["name"]
        companyPrice = company["price"]
        total = usd((float(tempRow[1]) * companyPrice))
        grandTotal = (grandTotal + (float(tempRow[1]) * companyPrice))
        tempRow = tempRow + (companyName, usd(companyPrice), total)
        rows.append(tempRow)
    row = User.query.filter_by(username=current_user.username).first()
    balance = float(row.cash)
    balance = usd(balance)
    grandTotal = usd(float(grandTotal) + float(row.cash))
    return render_template('finance/index.html', title="Finance", rows=rows, balance=balance, grandTotal=grandTotal, finance=finance)


@finance.route("/quote", methods=['GET', 'POST'])
@login_required
def quote():
    form = QuoteForm()
    if form.validate_on_submit():
        company = lookup(form.symbol.data)
        companyName = company["name"]
        companyPrice = usd(company["price"])
        companySymbol = company["symbol"]
        return render_template("finance/quote.html", title="Quoted", companyName=companyName, companyPrice=companyPrice, 
                               companySymbol=companySymbol, legend='Get Current Stock Price', form=form)
    return render_template('finance/quote.html', title="Quote", legend='Get Current Stock Price', form=form, finance=finance)


@finance.route("/buy", methods=['GET', 'POST'])
@login_required
def buy():
    form = BuyForm()
    if form.validate_on_submit():
        company = lookup(form.symbol.data)
        companyPrice = company["price"]
        companySymbol = company["symbol"]
        amount = float(form.shares.data)
        row = User.query.filter_by(username=current_user.username).first()
        balance = float(row.cash)
        if (float(companyPrice) * amount) > balance:
            abort(404, 'You do not have sufficient funds for this purchase, please check your balance and try again.')
        row.cash = (balance - (companyPrice * amount))
        transaction = Transaction(user_id=current_user.id, symbol=companySymbol, price=companyPrice, quantity=int(amount))
        db.session.add(transaction)
        db.session.commit()
        flash('Bought!', 'info')
        return redirect(url_for('finance.index'))
    return render_template('finance/buy.html', title="Buy", legend='Buy Stock', form=form, finance=finance)


@finance.route("/sell", methods=['GET', 'POST'])
@login_required
def sell():
    # create a list of tuples containing each option of the symbol drop down menu
    # this is then passed into the sell form under the choices parameter
    tempRows = db.session.query(Transaction.symbol, func.sum(Transaction.quantity))\
                .group_by(Transaction.symbol)\
                .filter_by(user_id=current_user.id).all()
    tempRows = [i for i in tempRows if not (i[1] <= 0)]
    def choices():
        rows = [('', "Select Symbol")]
        for tempRow in tempRows:
            rows.append((tempRow[0], tempRow[0]))
        return rows
    choices = choices()
    form = SellForm()
    form.symbol.choices = choices

    if form.validate_on_submit():
        if not lookup(form.symbol.data):
            abort(404, 'This symbol is not recognized, please try again with a different symbol.')
        else:
            company = lookup(form.symbol.data)
            companyPrice = company["price"]
            companySymbol = company["symbol"]
            inputAmount = form.shares.data
            row = User.query.filter_by(username=current_user.username).first()
            balance = float(row.cash)
            for tempRow in tempRows: 
                if (tempRow[0] == form.symbol.data):
                    ownedAmount = tempRow[1]
                    break
            if inputAmount > ownedAmount:
                abort(404, 'You do not own this many shares, please try again with a lesser amount.')
            else:
                row.cash = (balance + (companyPrice * inputAmount))
                transaction = Transaction(user_id=current_user.id, symbol=companySymbol, price=companyPrice, quantity=int(-inputAmount))
                db.session.add(transaction)
                db.session.commit()
                flash('Sold!', 'info')
                return redirect(url_for('finance.index'))
    return render_template('finance/sell.html', title="Sell", legend='Sell Stock', form=form, finance=finance)


@finance.route("/history")
@login_required
def history():
    rows = Transaction.query.filter_by(user_id=current_user.id).all()
    for row in rows:
        row.price = usd(float(row.price))
    return render_template('finance/history.html', title="History", rows=rows, finance=finance)


@finance.route("/deposit", methods=['GET', 'POST'])
@login_required
def deposit():
    form = DepositForm()
    if form.validate_on_submit():
        row = User.query.filter_by(username=current_user.username).first()
        amount = float(form.deposit.data)
        row.cash = (float(row.cash) + amount)
        db.session.commit()
        return redirect(url_for('finance.index'))
    return render_template('finance/deposit.html', title="Deposit", form=form, finance=finance)


def lookup(symbol):
    # Contact API
    try:
        response = requests.get(f"https://api.iextrading.com/1.0/stock/{urllib.parse.quote_plus(symbol)}/quote")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        quote = response.json()
        return {
            "name": quote["companyName"],
            "price": float(quote["latestPrice"]),
            "symbol": quote["symbol"]
        }
    except (KeyError, TypeError, ValueError):
        return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"

