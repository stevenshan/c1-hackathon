from . import controller
import flask

# this will be filtered out later if needed
accounts = ["Venture One",
'Essential Checking', "kill me"]

@controller.route("/account-overview", methods=["GET"])
def accountoverview():
    return flask.render_template("accountoverview.html", map=map, accounts=accounts)

# for all of a user's charity interests, get a list of charities and display as a list