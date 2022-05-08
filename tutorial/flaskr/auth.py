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

    acc_id = session.get("acc_id")
    if acc_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM bankacc WHERE accid = ?", (acc_id,)).fetchone()



@bp.route("/register", methods=("GET", "POST"))
def register():
    """Register a new user.

    Validates that the username is not already taken. Hashes the
    password for security.
    """
    session.clear()
    if request.method == "POST":
        fname = request.form["firstname"]
        lname = request.form["lastname"]
        username = request.form["username"]
        password = request.form["password"]
        balance = request.form["balance"]

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
        elif not balance:
            error = "Initial Balance is required!"
        elif verify_bal(balance) == False:
            error = "Initial Balance is not valid!"
        elif db.execute(
                'SELECT accid FROM bankacc WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered!'.format(username)

        if len(username) > 127:
            error = "Username too long!"
        elif len(password) > 127:
            error = "Password too long!"



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
                    "INSERT INTO bankacc (first_name,last_name,username, password, balance) VALUES (?, ?, ?, ?, ?)",
                    (fname,lname, username, generate_password_hash(password),balance)
                )
                db.commit()
            except db.IntegrityError:
                # The username was already taken, which caused the
                # commit to fail. Show a validation error.
                error = f"User {username} is already registered!"
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
        user = None

        check_password_hash = db.execute('SELECT password from bankacc WHERE username="' + username +'"').fetchone()
        if check_password_hash is not None:
            stmt = 'SELECT * FROM bankacc WHERE username = "' + username + '" AND ' + \
                   ('1' if check_password_hash(check_password_hash['password'], password) else '0')
            user = db.execute(stmt).fetchone()

        if user is None or check_password_hash is None:
            error = "Incorrect username/password."

        if error is None:
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

def verify_bal(balance):
    bal_pattern = re.compile('(0|[1-9][0-9]*)(\\.[0-9]{2})?')
    balmatch = bal_pattern.fullmatch(balance)
    if balmatch is None:
        return False
    else:
        return True


@bp.route("/logout")
def logout():
    """Clear the current session, including the stored user id."""
    session.clear()
    return redirect(url_for("index"))
