from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
import re
from werkzeug.exceptions import abort

from Bank266P.auth import login_required
from Bank266P.db import get_db

bp = Blueprint("account", __name__)


@bp.route("/")
def index():
    """Show the balance of the user who has logged in."""
    db = get_db()
    accountdet=[]
    if g.user is not None:
        account = db.execute(
            "SELECT accid,balance FROM bankacc WHERE accid =  ?", (g.user['accid'],)
        ).fetchone()
        accountdet.append(account)
    return render_template("page/index.html", account=accountdet)


def get_account(id, check_author=True):
    """Get a users account based on the account ID of the user
    """
    account = (
        get_db()
        .execute(
            "SELECT accid, balance FROM bankacc WHERE accid =  ?",
            (id,)
        )
        .fetchone()
    )



    return account


@bp.route("/<int:id>/withdraw", methods=("GET", "POST"))
#CWE 425 Vulnerability
# @login_required
def withdraw(id):
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
            if request.form['withdraw'] == "Withdraw":
                result= balance - float(amount)
                if(result < 0):
                    error = "Withdrawn amount is more than current balance!"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE bankacc SET balance = ? WHERE accid = ?", (result, id)
            )
            db.commit()
            return redirect(url_for("account.index"))

    return render_template("page/withdraw.html", account=account)

@bp.route("/<int:id>/deposit", methods=("GET", "POST"))
@login_required
def deposit(id):
    """Deposit an valid amount in the user's account."""
    account = get_account(id)

    if request.method == "POST":
        amount = request.form["amount"]
        error = None

        if not amount:
            error = "An amount is required!"
        elif verify_amount(amount)== False:
            error = "Invalid amount entered!"
        else:
            balance = account['balance']
            if request.form['deposit'] == "Deposit":
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

    return render_template("page/deposit.html", account=account)

def verify_amount(amount):
    amt_pattern = re.compile('(0|[1-9][0-9]*)(\\.[0-9]{2})?')
    amtmatch = amt_pattern.fullmatch(amount)
    if amtmatch is None:
        return False
    else:
        return True