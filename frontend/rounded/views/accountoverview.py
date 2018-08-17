from . import controller
import flask
from rounded.core.user_info import get as BANK

# this will be filtered out later if needed
accounts = ["Venture One",
'Essential Checking', "kill me"]

@controller.route("/account-overview", methods=["GET"])
def accountoverview():
    accounts = BANK.ACCOUNTS
    for account in accounts:
        if account["balance"] == None:
            account["strBalance"] = "0.00"
            continue 
        account["strBalance"] = "{0:.2f}".format(account["balance"])
    return flask.render_template("accountoverview.html", map=map, accounts=accounts)

# for all of a user's charity interests, get a list of charities and display as a list