"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined



@app.route("/")
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of Users"""

   
    return render_template("user_list.html")

@app.route("/login_form")
def login():
    """Show login page"""

    return render_template("login_form.html")

@app.route("/login_form", methods=["POST"])
def check_user_email():
    """check whether user entered email exists in database"""

    user_email = request.form.get("email")
    user_password = request.form.get("password")
    user_found = User.query.filter_by(email=user_email).first()
    password_found = User.query.filter_by(password=user_password).first()

    if user_found is None:
        flash("no email found")
        return redirect("/login_form")
    elif password_found != user_password:
        flash("Incorrect password entered")
        return redirect("/login_form")
    else:
        session["current_user"] = user_email
        flash("Logged In")
        return redirect("/")



    


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
