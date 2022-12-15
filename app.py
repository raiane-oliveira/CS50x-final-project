import locale

from cs50 import SQL
from flask import Flask, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Sets a session usage limit and where it will be saved (hard drive)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 library to user SQLite database
db = SQL("sqlite:///planningSale.db")

# Configure locale library to format numbers in money format
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Remember user ID for all functions
userID = 0


@app.route("/", methods=["POST", "GET"])
def index():
    """ Render index page apresentation"""

    # Checks if have user id
    if session.get("user_id"):
        userID = session["user_id"]

        # Checks if have a sale plan
        salePlan = db.execute("SELECT * FROM salesPlan WHERE user_id = ?", userID)    
        if not salePlan:
            return render_template("index.html", salePlan=salePlan)
            
        # Selects all sales with the filter chosen by the user
        selling = db.execute("SELECT * FROM salesPlan WHERE filters = ? AND user_id = ?", "selling", userID)
        not_started = db.execute("SELECT * FROM salesPlan WHERE filters = ? AND user_id = ?", "not-started", userID)
        sold = db.execute("SELECT * FROM salesPlan WHERE filters = ? AND user_id = ?", "sold", userID)

        return render_template("index.html", salePlan=salePlan, selling=selling, not_started=not_started, sold=sold)

    salePlan = None
    return render_template("index.html", salePlan=salePlan)


@app.route("/delete", methods=["POST"])
def delete():
    """Delete a sale plan"""

    # Remember user id
    userID = session["user_id"]

    # Delete from database
    id = request.form.get("id-del")
    if id:
        db.execute("DELETE FROM salesPlan WHERE id = ? AND user_id = ?", id, userID)
    return redirect("/")


@app.route("/account", methods=["POST", "GET"])
def account():
    """Delete the user account"""

    # Checks if have user_id
    if session.get("user_id"):
        userID = session["user_id"]

        # route via POST
        if request.method == "POST":

            # Delete all data from user account
            db.execute("DELETE FROM salesPlan WHERE user_id = ?", userID)

            # Delete account
            db.execute("DELETE FROM users WHERE id = ?", userID)

            # Free session
            session.clear()

            return redirect("/")
    
        # route via GET 
        return render_template("account.html")
    
    return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():
    """ Log user in """

    # route via POST
    if request.method == "POST":

        # Cheking erros
        if not request.form.get("username"):
            return render_template("login.html", message="You must provide a username!")
        if not request.form.get("password"):
            return render_template("login.html", message="You must provide a password!")

        # Store data
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username and password match
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return render_template("login.html", message="invalid password and/or username")

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]

        return redirect("/")

    # route via GET
    return render_template("login.html")


@app.route("/register", methods=["POST", "GET"])
def register():
    """Register user"""

    # route via POST
    if request.method == "POST":

        # Gets data
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm-password")

        # Access duplicates
        duplicate_username = db.execute("SELECT username FROM users WHERE username = ?", username)

        # Checking erros
        if not username or not password or not confirm_password:
            return render_template("register.html", message="blank fields!")
        if confirm_password != password:
            return render_template("register.html", message="passwords don't match!")
        if duplicate_username:
            return render_template("register.html", message="this username is already in use")

        # Change the password to hash code
        hash = generate_password_hash(password)

        # Add to database
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)

        return redirect("/login")

    # route via GET
    return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    return redirect("/")


@app.route("/plansale", methods=["POST", "GET"])
def plansale():
    """Plan a sale of the user"""

    # Checks if have user id
    if session.get("user_id"):
        userID = session["user_id"]

        # route via POST
        if request.method == "POST":

            # Checking erros
            if not request.form.get("name") or not request.form.get("price") or not request.form.get("goal") or not request.form.get("stock"):
                return render_template("plansale.html", message="Blank required fields!")
            if request.form.get("goal") not in ["Money goal", "Sales goal"]:
                return render_template("plansale.html", message="Invalid type of goal")

            # Store data from sale planning
            name = request.form.get("name")
            stock = int(request.form.get("stock"))
            goal_type = request.form.get("goal")
            notes = request.form.get("notes")
            date_start = request.form.get("date-start")
            date_end = request.form.get("date-end")

            # Checks if the price and goal is numeric
            check_price = isnumber(request.form.get("price"))
            check_goal = isnumber(request.form.get("goal-option"))
            if not check_price or not check_goal:
                return render_template("plansale.html", message="Invalid price and/or goal!")

            # Convert price to US dollar
            price = locale.atof(request.form.get("price"))
            price = locale.currency(price, grouping=True)

            # Convert money goal to US dollar
            if goal_type == "Money goal":
                goal = locale.atof(request.form.get("goal-option"))
                goal = locale.currency(goal, grouping=True)
            else:
                goal = locale.atoi(request.form.get("goal-option"))

            # Store filter
            filter = request.form.get("id")

            # Insert sale plan into the database
            db.execute("INSERT INTO salesPlan (name, price, goal, date_start, date_end, stock, filters, goal_options, notes, user_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    name, price, goal, date_start, date_end, stock, filter, goal_type, notes, userID)

            return redirect("/")

        # route via GET
        return render_template("plansale.html")

    return redirect("/")


# Checks if the field is numeric
def isnumber(value):
    try:
        float(value)
    except ValueError:
        return False
    return True