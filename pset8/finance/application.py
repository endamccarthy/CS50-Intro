import os
import re

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    # looks through every transaction and groups identical symbols together, adding the SUM of each associated share
    rows = db.execute("SELECT symbol,SUM(quantity) FROM transactions WHERE user_id = :user_id GROUP BY symbol",
                      user_id=session["user_id"])
    rows = [i for i in rows if not (i['SUM(quantity)'] <= 0)]
    grandTotal = 0
    for row in rows:
        company = lookup(row['symbol'])
        companyName = company["name"]
        companyPrice = company["price"]
        total = usd((float(row['SUM(quantity)']) * companyPrice))
        grandTotal = (grandTotal + (float(row['SUM(quantity)']) * companyPrice))
        row.update({'name': companyName})
        row.update({'price': usd(companyPrice)})
        row.update({'total': total})
    cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
    cashValue = usd(cash[0]['cash'])
    grandTotal = usd(grandTotal + cash[0]['cash'])
    return render_template("index.html", rows=rows, cashValue=cashValue, grandTotal=grandTotal)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "GET":
        return render_template("buy.html")
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL!")
        elif not request.form.get("shares"):
            return apology("MISSING SHARES!")
        elif not request.form.get("shares").isdigit():
            return apology("INVALID NUMBER!")
        elif not lookup(request.form.get("symbol")):
            return apology("INVALID SYMBOL!")
        else:
            company = lookup(request.form.get("symbol"))
            companySymbol = company["symbol"]
            companyPrice = company["price"]
            amount = float(request.form.get("shares"))
            balance = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
            if (companyPrice * amount) > balance[0]["cash"]:
                return apology("CAN'T AFFORD!")
            else:
                db.execute("UPDATE users SET cash = :cost WHERE id = :user_id",
                           cost=balance[0]["cash"] - (companyPrice * amount),
                           user_id=session["user_id"])
                db.execute("CREATE TABLE IF NOT EXISTS transactions(user_id int NOT NULL, symbol varchar(10) NOT NULL, price precision NOT NULL, quantity int NOT NULL, transacted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
                db.execute("CREATE UNIQUE INDEX IF NOT EXISTS sale ON transactions(user_id,transacted)")
                db.execute("CREATE INDEX IF NOT EXISTS user_ids ON transactions(user_id)")
                db.execute("CREATE INDEX IF NOT EXISTS symbols ON transactions(symbol)")
                db.execute("INSERT INTO transactions (user_id,symbol,price,quantity) VALUES (:user_id,:symbol,:price,:quantity)",
                           user_id=session["user_id"],
                           symbol=companySymbol,
                           price=companyPrice,
                           quantity=int(amount))
                flash('Bought!')
                return redirect("/")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # sends a jsonify response back to register.html
    username = request.args.get("username")
    if (len(username) > 0) and (len(db.execute("SELECT * FROM users WHERE username = :username", username=username)) == 0):
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Deposit into account"""

    rows = db.execute("SELECT symbol,SUM(quantity) FROM transactions WHERE user_id = :user_id GROUP BY symbol",
                      user_id=session["user_id"])
    if request.method == "GET":
        return render_template("deposit.html")
    if request.method == "POST":
        if not request.form.get("deposit"):
            return apology("MISSING AMOUNT!")
        balance = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        db.execute("UPDATE users SET cash = :new WHERE id = :user_id",
                   new=balance[0]["cash"] + float(request.form.get("deposit")),
                   user_id=session["user_id"])
        flash('Deposit Successful!')
        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    rows = db.execute("SELECT symbol,quantity,price,transacted FROM transactions WHERE user_id = :user_id",
                      user_id=session["user_id"])
    for row in rows:
        row['price'] = usd(row['price'])
    return render_template("history.html", rows=rows)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "GET":
        return render_template("quote.html")
    if request.method == "POST":
        if not lookup(request.form.get("symbol")):
            return apology("INVALID SYMBOL")
        else:
            company = lookup(request.form.get("symbol"))
            companyName = company["name"]
            companyPrice = usd(company["price"])
            companySymbol = company["symbol"]
            return render_template("quoted.html", companyName=companyName, companyPrice=companyPrice, companySymbol=companySymbol)


@app.route("/password", methods=["GET", "POST"])
@login_required
def password():
    """Change password"""

    if request.method == "GET":
        return render_template("password.html")
    if request.method == "POST":
        rows = db.execute("SELECT * FROM users WHERE id = :user_id",
                          user_id=session["user_id"])
        if not request.form.get("password"):
            return apology("MISSING PASSWORD!")
        if not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("CURRENT PASSWORD INCORRECT")
        if not request.form.get("new"):
            return apology("ENTER NEW PASSWORD!")
        if len(request.form.get("new")) < 8:
            return apology("Make sure your password is at lest 8 letters")
        if re.search('[0-9]', request.form.get("new")) is None:
            return apology("Make sure your password has a number in it")
        if re.search('[A-Z]', request.form.get("new")) is None:
            return apology("Make sure your password has a capital letter in it")
        if not request.form.get("confirmation"):
            return apology("PASSWORDS DON'T MATCH")
        if request.form.get("new") != request.form.get("confirmation"):
            return apology("PASSWORDS DON'T MATCH")

        db.execute("UPDATE users SET hash = :hashed WHERE id = :user_id",
                   hashed=generate_password_hash(request.form.get("new")),
                   user_id=session["user_id"])
        flash('Password Changed!')
        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "GET":
        # Forget any user_id
        session.clear()
        return render_template("register.html")
    if request.method == "POST":
        if not request.form.get("username"):
            return apology("MISSING USERNAME!")
        if not request.form.get("password"):
            return apology("MISSING PASSWORD!")
        if len(request.form.get("password")) < 8:
            return apology("Make sure your password is at lest 8 letters")
        if re.search('[0-9]', request.form.get("password")) is None:
            return apology("Make sure your password has a number in it")
        if re.search('[A-Z]', request.form.get("password")) is None:
            return apology("Make sure your password has a capital letter in it")
        if not request.form.get("confirmation"):
            return apology("PASSWORDS DON'T MATCH")
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("PASSWORDS DON'T MATCH")

        """ because username is a UNIQUE value in the database, the following will not succeed if an
        identical username is passsed in. It will return false for result in this case. """
        result = db.execute("INSERT INTO users (id,username,hash) VALUES (NULL,:username,:hashed)",
                            username=request.form.get("username"),
                            hashed=generate_password_hash(request.form.get("password")))
        if not result:
            return apology("USERNAME IS NOT AVAILABLE!")

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))
        session["user_id"] = rows[0]["id"]
        db.execute("CREATE TABLE IF NOT EXISTS transactions(user_id int NOT NULL, symbol varchar(10) NOT NULL, price precision NOT NULL, quantity int NOT NULL, transacted timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP)")
        db.execute("CREATE UNIQUE INDEX IF NOT EXISTS sale ON transactions(user_id,transacted)")
        db.execute("CREATE INDEX IF NOT EXISTS user_ids ON transactions(user_id)")
        db.execute("CREATE INDEX IF NOT EXISTS symbols ON transactions(symbol)")
        flash('Registered!')
        return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    rows = db.execute("SELECT symbol,SUM(quantity) FROM transactions WHERE user_id = :user_id GROUP BY symbol",
                      user_id=session["user_id"])
    if request.method == "GET":
        return render_template("sell.html", rows=rows)
    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("MISSING SYMBOL!")
        if not request.form.get("shares"):
            return apology("MISSING SHARES!")
        stock = next(item for item in rows if item.get("symbol") == request.form.get("symbol"))
        stockAmount = stock['SUM(quantity)']
        if float(request.form.get("shares")) > stockAmount:
            return apology("TOO MANY SHARES!")
        company = lookup(request.form.get("symbol"))
        companySymbol = company["symbol"]
        companyPrice = company["price"]
        amount = float(request.form.get("shares"))
        db.execute("INSERT INTO transactions (user_id,symbol,price,quantity) VALUES (:user_id,:symbol,:price,:quantity)",
                   user_id=session["user_id"],
                   symbol=companySymbol,
                   price=companyPrice,
                   quantity=(int(-amount)))
        balance = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        db.execute("UPDATE users SET cash = :cost WHERE id = :user_id",
                   cost=balance[0]["cash"] + (companyPrice * amount),
                   user_id=session["user_id"])
        flash('Sold!')
        return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
