from . import controller
from rounded.core import url_tools, user
import flask
from rounded.core.user_info import accounts

@controller.route("/pay", methods=["GET"])
def pay():
    args = flask.request.args
    amount = args.get("amount")

    if amount == None:
        return "Set amount in GET request"
    else:
        accounts.make_payment(float(amount))

        return flask.redirect("/account-overview")

@controller.route("/transfer", methods=["GET"])
def transfer():
    accounts.add_charity_balance()
    return flask.redirect("/account-overview")

@controller.route("/data", methods=["GET"])
def datamessage():
    from rounded.core.user_info import get as BANK
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
