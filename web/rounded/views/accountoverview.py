from . import controller
import flask
from rounded.core import url_tools

@controller.route("/account-overview", methods=["GET"])
def accountoverview():
    from rounded.core.user_info import get as BANK
    BANK.refresh()
    accounts = BANK.ACCOUNTS
    hasCharity = False
    for account in accounts:
        if account.get("nickname") == "Charity Account":
            hasCharity = True
        if account.get("balance") == None:
            account["strBalance"] = "0.00"
            continue 
        account["strBalance"] = "{0:.2f}".format(account["balance"])
    return url_tools.render_template("accountoverview.html", map=map, accounts=accounts, hasCharity=hasCharity)

# for all of a user's charity interests, get a list of charities and display as a list