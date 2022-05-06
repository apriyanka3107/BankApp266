from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
import re
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("account", __name__)


@bp.route("/")
def index():
    """Show all the posts, most recent first."""
    db = get_db()
    accountdet=[]
    if g.user is not None:
        account = db.execute(
            "SELECT accid,balance FROM bankacc WHERE accid =  ?", (g.user['accid'],)
        ).fetchone()
        accountdet.append(account)
    return render_template("blog/index.html", account=accountdet)


def get_account(id, check_author=True):
    """Get a post and its author by id.

    Checks that the id exists and optionally that the current user is
    the author.

    :param id: id of post to get
    :param check_author: require the current user to be the author
    :return: the post with author information
    :raise 404: if a post with the given id doesn't exist
    :raise 403: if the current user isn't the author
    """
    account = (
        get_db()
        .execute(
            "SELECT accid, balance FROM bankacc WHERE accid =  ?",
            (id,)
        )
        .fetchone()
    )

    # if post is None:
    #     abort(404, f"Post id {id} doesn't exist.")
    #
    # if check_author and post["author_id"] != g.user["id"]:
    #     abort(403)

    return account


@bp.route("/<int:id>/update", methods=("GET", "POST"))
@login_required
def update(id):
    """Update a post if the current user is the author."""
    account = get_account(id)

    if request.method == "POST":
        amount = request.form["amount"]
        error = None

        if not amount:
            error = "An amount is required."
        elif verify_amount(amount)== False:
            error = "Invalid amount entered!"
        else:
            balance = account['balance']
            if request.form['update'] == "Withdraw":
                result= balance - float(amount)
                if(result < 0):
                    error = "Withdrawn amount is more than current balance!"
            elif request.form['update'] == "Deposit":
                result = balance + float(amount)

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE bankacc SET balance = ? WHERE accid = ?", (result, id)
            )
            db.commit()
            return redirect(url_for("account.index"))

    return render_template("blog/update.html", account=account)

def verify_amount(amount):
    amt_pattern = re.compile('(0|[1-9][0-9]*)(\\.[0-9]{2})?')
    amtmatch = amt_pattern.fullmatch(amount)
    if amtmatch is None:
        return False
    else:
        return True