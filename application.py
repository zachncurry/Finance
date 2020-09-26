import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# REFERENCE: Flashing A Response using Jinja: https://flask.palletsprojects.com/en/1.0.x/quickstart/#rendering-templates


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

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page

        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        balance = cash[0]["cash"]
        total = balance
        stocks=db.execute("SELECT symbol, SUM(quantity) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id = session["user_id"])
        quotes={}
        for stock in stocks:
            quotes[stock["symbol"]] = lookup(stock["symbol"])
        return render_template("index.html", total = total, quotes = quotes, stock = stock)

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

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
#REFERENCE: Generate Hash Parameters: https://werkzeug.palletsprojects.com/en/1.0.x/utils/
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password", 403)

        #NEED TO ADD CHECK PASSWORD FUNCTION
        #Flask does not allow functions on the page

        name = request.form.get("username")
        password_var = request.form.get("password")
        hash_pass = generate_password_hash(password_var, method='pbkdf2:sha256',salt_length=8)
        db.execute("INSERT INTO users (username, hash) VALUES (:name, :password)", name = name, password = hash_pass);
        flash("Registered!")
        return render_template("login.html")

    if request.method == "GET":
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


# REFERENCE: Solution Reference from Teacher: https://github.com/mareksuscak/cs50/blob/master/pset7/finance/application.py
# REFERENCE: How to display SQL data in html using pandas: https://stackoverflow.com/questions/58147040/python-flask-sql-query-to-html-page-table

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    if request.method == "GET":
        transactions = db.execute("SELECT symbol, quantity, price_per_share, total_price, date FROM transactions WHERE user_id = :user_id ORDER BY date ASC ", user_id=session["user_id"])
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        balance = cash[0]["cash"]
        total = balance
        return render_template("history.html", transactions = transactions, total = total)


    if request.method == "POST":
        transactions = db.execute("SELECT symbol, quantity, price_per_share, total_price, date FROM transactions WHERE user_id = :user_id ORDER BY date ASC", user_id=session["user_id"])
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        balance = cash[0]["cash"]
        total = balance
        return render_template("history.html", transactions = transactions, total = total)


# REFERENCE: Providing a total using SQL: https://www.w3resource.com/sql/aggregate-functions/sum-with-group-by.php
@app.route("/index", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        balance = cash[0]["cash"]
        total = balance
        stocks=db.execute("SELECT symbol, SUM(quantity) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id = session["user_id"])
        quotes={}
        for stock in stocks:
            quotes[stock["symbol"]] = lookup(stock["symbol"])
        return render_template("index.html", total = total, quotes = quotes, stock = stock)#balance = balance, stocks = stocks, quotes = quotes)


    if request.method == "GET":
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        balance = cash[0]["cash"]
        total = balance
        stocks=db.execute("SELECT symbol, SUM(quantity) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id = session["user_id"])
        quotes={}
        for stock in stocks:
            quotes[stock["symbol"]] = lookup(stock["symbol"])
        return render_template("index.html", total = total, quotes = quotes, stock = stock)#, stocks = stocks, quotes = quotes)


# REFERENCE: How to setup forms to easily connect to functions then render in HTML: https://www.reddit.com/r/cs50/comments/8bn7t8/pset7_finance_question_quote_lookup_page/
# REFERENCE: Using multiple defs() in one route to simplify the appy.py: https://stackoverflow.com/questions/17716436/a-better-way-to-accept-multiple-request-types-in-a-single-view-method

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    #"""Get Stock Quote"""
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        if quote == None:
            return apology("Invalid Symbol", 400)
        return render_template("quoted.html", quote = quote)

    else:
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        #Check symbol
        if quote == None:
            return apology("Invalid Symbol", 400)

        try:
            quantity = int(request.form.get("quantity"))
        except:
            return apology("Must be a positive number",400)

        if quantity <=0:
            return apology("Please enter a number larger than 0",400)

        rows= db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        cash_remaining = rows[0]["cash"]
        price_per_share = quote["price"]

        total_price = price_per_share * quantity

        if total_price > cash_remaining:
            return apology("Insufficient Funds")

        db.execute("CREATE TABLE IF NOT EXISTS transactions(user_id TEXT,symbol TEXT, quantity REAL, price_per_share REAL, total_price REAL,date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
        db.execute("UPDATE users SET cash = cash - :price WHERE id= :user_id", price= total_price, user_id = session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, quantity, price_per_share, total_price) VALUES(:user_id,:symbol, :quantity, :price, :total_price)",
            user_id=session["user_id"], symbol=request.form.get("symbol"), quantity = quantity, price=price_per_share, total_price=total_price)

        flash("Bought!")
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        balance = cash[0]["cash"]
        total = balance
        stocks=db.execute("SELECT symbol, SUM(quantity) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id = session["user_id"])
        quotes={}
        for stock in stocks:
            quotes[stock["symbol"]] = lookup(stock["symbol"])
        return render_template("index.html", total = total, quotes = quotes, stock = stock)

    else:
        return render_template("buy.html")


    return render_template("buy.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        quote=lookup(request.form.get("symbol"))

        if quote == None:
            return apology("Invalid Symbol", 400)

        try:
            quantity = int(request.form.get("quantity"))
        except:
            return apology("Must be a positive number",400)

        if quantity <=0:
            return apology("Must be more than 0", 400)

        stock = db.execute("SELECT SUM(quantity) as total_shares FROM transactions WHERE user_id = :user_id AND symbol=:symbol GROUP BY symbol",
            user_id=session["user_id"],symbol=request.form.get("symbol"))

        if len(stock) != 1 or stock[0]["total_shares"]<=0 or stock[0]["total_shares"]<quantity:
            return apology("You can not sell what you do not own", 400)

        rows = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])

        cash_remaining = rows[0]["cash"]
        price_per_share=quote["price"]

        total_price = price_per_share * quantity

        db.execute("UPDATE users SET cash = cash + :price WHERE id = :user_id", price=total_price, user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, quantity, price_per_share, total_price) VALUES(:user_id, :symbol, :quantity, :price, :total_price)",
            user_id=session["user_id"],
            symbol=request.form.get("symbol"),
            quantity = -1 * quantity,
            price=price_per_share,
            total_price = total_price)

        flash("Sold!")
        cash = db.execute("SELECT cash FROM users WHERE id = :user_id", user_id=session["user_id"])
        balance = cash[0]["cash"]
        total = balance
        stocks=db.execute("SELECT symbol, SUM(quantity) as total_shares FROM transactions WHERE user_id = :user_id GROUP BY symbol HAVING total_shares > 0", user_id = session["user_id"])
        quotes={}
        for stock in stocks:
            quotes[stock["symbol"]] = lookup(stock["symbol"])
        return render_template("index.html", total = total, quotes = quotes, stock = stock)

    else:
        return render_template("sell.html")

