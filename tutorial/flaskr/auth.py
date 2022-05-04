import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flaskr.db import get_db
import re

bp = Blueprint("auth", __name__, url_prefix="/auth")


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a user id is stored in the session, load the user object from
    the database into ``g.user``."""
    acc_id = session.get("acc_id")

    if acc_id is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM bankacc WHERE accid = ?", (acc_id,)).fetchone()
        )


@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    if request.method == "POST":
        fname = request.form["firstname"]
        lname = request.form["lastname"]
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]


        db = get_db()
        error = None

        if not username:
            error = "Username is required!"
        elif not password:
            error = "Password is required!"
        elif not fname:
            error = "First Name is required!"
        elif not lname:
            error = "Last Name is required!"
        elif not email:
            error = "Email is required!"
        elif db.execute(
                'SELECT accid FROM bankacc WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered!'.format(username)

        if len(username) > 127:
            error = "Username too long"
        elif len(password) > 127:
            error = "Password too long"

        regex = re.compile("[_\\-\\.0-9a-z]+")
        unamereg = regex.fullmatch(username)
        if unamereg is None:
            error = "Username contains illegal characters!"
        pwdreg = regex.fullmatch(password)
        if pwdreg is None:
            error = "Password contains illegal characters!"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO bankacc (first_name,last_name,email,username, password) VALUES (?, ?, ?, ?, ?)",
                    (fname,lname,email, username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {username} is already registered."
            else:
                # Success, go to the login page.
                return redirect(url_for("auth.login"))

        flash(error)


    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login():
    """Log in a registered user by adding the user id to the session."""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM bankacc WHERE username = ?", (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password):
            error = "Incorrect password."

        if error is None:
            # store the user id in a new session and return to the index
            session.clear()
            session["acc_id"] = user["accid"]
            return redirect(url_for("index"))

        flash(error)
        if request.method == 'GET':
            username = session.get('username', None)

            if username:
                query = 'SELECT accid from bankacc WHERE username="' + username + '"'
                db = get_db()
                acc_id = db.execute(query).fetchone()

                if(acc_id['accid']):
                    session['acc_id'] = acc_id['id']
                    return redirect(url_for('index'))

    return render_template("auth/login.html")


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
