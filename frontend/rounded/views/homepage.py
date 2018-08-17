from . import controller
from rounded.core import url_tools, user
from rounded.core.user_info import get as BANK
import flask

@controller.route("/", methods=["GET"])
def homepage():
    return flask.redirect(flask.url_for("app.setup"))

@controller.route("/data", methods=["GET"])
def datamessage():
    BANK.refresh()
    accounts = BANK.ACCOUNTS
    balance = "0.00"
    for account in accounts:
        if (account.get("nickname") == "Charity Account" and 
                account.get("balance") != None):
            balance = account.get("balance")
            balance = "{0:.2f}".format(balance)   
    return flask.jsonify({
        "balance": balance,
        "charity": user.getCharity(),
    })

