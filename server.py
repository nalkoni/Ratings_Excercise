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


@app.route("/movies")
def movies_list():
    """Show list of movies"""

    movies = Movie.query.all()
    return render_template("movies.html",
                            movies=movies)


@app.route("/users")
def user_list():
    """Show list of Users"""

    users = User.query.all()
    return render_template("user_list.html",
                            users=users)


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
    

    if user_found is None:
        flash("no email found")
        return redirect("/login_form")

    if user_found.password != user_password:
        flash("Incorrect password entered")
        return redirect("/login_form")


    session["current_user"] = user_found.user_id
    flash("Logged In")
    return redirect("/")


@app.route("/create_account")
def add_user():
    """user account creation"""

    return render_template("create_account.html")


@app.route("/create_account", methods=["POST"])
def add_user_db():
    """adding new user to db"""

    user_email = request.form.get("email")
    user_password = request.form.get("password")
    user_age = request.form.get("age")
    user_zipcode = request.form.get("zipcode")

    user = User(email=user_email, password=user_password, age=user_age, zipcode=user_zipcode)
    db.session.add(user)
    db.session.commit()

    return redirect("/user_details.html")

@app.route("/user_details", methods=["POST"])
def returning_user_info():
    user = session['current_user'] 
    user = User.query.filter_by(user_id=user_id).first()
    user_ratings_list = user.ratings

    return render_template("user_details.html",
                            user)


@app.route("/logout")
def log_out():
    """logging user out"""
    
    session.clear()

    return render_template("logout.html")



    


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
