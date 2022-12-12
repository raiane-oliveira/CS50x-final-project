import re
import locale

from datetime import datetime
from PilLite import Image
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
locale.setlocale(locale.LC_MONETARY, 'en_US.UTF-8')

# Remember user ID for all functions
userID = 0

# List of goals options - Page Plan a Sale
GOALS = [
    "Money goal",
    "Sales goal"
]


@app.route("/", methods=["POST", "GET"])
def index():
    """ Render index page apresentation"""

    # Checks if have a sale plan and change the index page se sim
    checkSalePlan = db.execute("SELECT * FROM salesPlan WHERE user_id = ?", userID)

    # Seleciona os dados da venda planejada
    salePlan = None
    if len(checkSalePlan) != 0:
        salePlan = db.execute("SELECT * FROM salesPlan WHERE user_id = ?", userID)
        
        # Recebe o id da venda planejada e seleciona os dados desse id
        id = request.form.get("id-edit")
        card_salePlan = db.execute("SELECT * FROM salesPlan WHERE id = ? AND user_id = ?", id, userID)


    return render_template("index.html", checkSalePlan=len(checkSalePlan), salePlan=salePlan, card=card_salePlan)


@app.route("/delete", methods=["POST"])
def delete():
    """Delete a sale plan"""

    # Gets sale plan id
    id = request.form.get("id-del")

    # Delete from database
    if id:
        db.execute("DELETE FROM salesPlan WHERE id = ? AND user_id = ?", id, userID)
    return redirect("/")


@app.route("/edit", methods=["POST", "GET"])
def edit():
    """Edit sale plan"""

    if request.method == "POST":

        # Checking erros
        if not request.form.get("name") or not request.form.get("price") or not request.form.get("goal") or not request.form.get("stock"):
            return redirect("/")

        # Store data from sale planning
        id = request.form.get("id")
        name = request.form.get("name")
        date_start = request.form.get("date-start")
        date_end = request.form.get("date-end")
        stock = int(request.form.get("stock"))

        # Checks if the data is numeric
        check_price = isnumber(request.form.get("price").replace(",", "."))
        check_goal = None
        if request.form.get("goal") == "Money goal":
            check_goal = isnumber(request.form.get("goal-option").replace(",", "."))
        else:
            check_goal = isnumber(request.form.get("goal-option"))

        if not check_price or not check_goal:
            return redirect("/")

        # Store price and goal
        price = locale.atof(request.form.get("price").replace(',', '.'))
        price = locale.currency(price, grouping=True)

        if request.form.get("goal") == "Money goal":
            goal = locale.atof(request.form.get("goal-option").replace(',', '.'))
            goal = locale.currency(goal, grouping=True)
        else:
            goal = locale.atoi(request.form.get("goal-option"))

        # Update the planning
        db.execute("UPDATE salesPlan SET name = ?, price = ?, goal = ?, date_start = ?, date_end = ?, stock = ? WHERE id = ? AND user_id = ?",
                   name, price, goal, date_start, date_end, stock, id, userID)

        return redirect("/")

    return redirect("/")


@app.route("/login", methods=["POST", "GET"])
def login():
    """ Log user in """

    # route via POST
    if request.method == "POST":

        # Cheking erros
        if not request.form.get("username"):
            return redirect("/login", message="You must provide a username")
        if not request.form.get("password"):
            return redirect("/login", message="You must provide a password")

        # Store data
        username = request.form.get("username")
        password = request.form.get("password")
        user = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username and password match
        if len(user) != 1 or not check_password_hash(user[0]["hash"], password):
            return redirect("/login", message="invalid password and/or username")

        # Remember which user has logged in
        session["user_id"] = user[0]["id"]
        userID = user[0]["id"]

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

        # Acess duplicates
        duplicate_username = db.execute("SELECT username FROM users WHERE username = ?", username)

        # Checking erros
        if not username or not password or not confirm_password:
            return redirect("/register")
        if confirm_password != password:
            return redirect("/register")
        if duplicate_username:
            return redirect("/register")

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

    # route via POST
    if request.method == "POST":

        # Checking erros
        if not request.form.get("name") or not request.form.get("price") or not request.form.get("goal") or not request.form.get("stock"):
            return redirect("/plansale")

        # Store data from sale planning
        name = request.form.get("name")
        date_start = request.form.get("date-start")
        date_end = request.form.get("date-end")
        stock = int(request.form.get("stock"))

        # Checks if the data is numeric
        check_price = isnumber(request.form.get("price").replace(",", "."))
        check_goal = None
        if request.form.get("goal") == "Money goal":
            check_goal = isnumber(request.form.get("goal-option").replace(",", "."))
        else:
            check_goal = isnumber(request.form.get("goal-option"))

        if not check_price or not check_goal:
            return redirect("/plansale")

        # Store price goal
        price = locale.atof(request.form.get("price").replace(',', '.'))
        price = locale.currency(price, grouping=True)
        if request.form.get("goal") == "Money goal":
            goal = locale.atof(request.form.get("goal-option").replace(',', '.'))
            goal = locale.currency(goal, grouping=True)
        else:
            goal = locale.atoi(request.form.get("goal-option"))

        # Insert sale plan into the database
        db.execute("INSERT INTO salesPlan (name, price, goal, date_start, date_end, stock, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                name, price, goal, date_start, date_end, stock, userID)
        
        return redirect("/")

    # route via GET
    return render_template("plansale.html")


# Checks if the field is numeric
def isnumber(value):
    try:
        float(value)
    except ValueError:
        return False
    return True


if __name__ == "__main__":
    app.run(debug=True)