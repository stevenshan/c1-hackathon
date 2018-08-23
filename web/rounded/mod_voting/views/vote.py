import flask
from rounded.core import redis, user, url_tools
from rounded.mod_voting import controller
from rounded.mod_voting.lib import db as voting_db
from rounded.mod_voting.lib import twitterCalls as tweeting
import json

@controller.route("/vote", methods=["GET"])
def vote():

    try:
        charities = voting_db.get_charities()
    except Exception as e:
        return "Error retrieving charities: " + str(e)

    for charity in charities:
        charity["description"] = redis.hget("charity:" + charity["name"], "mission")

    _charities = json.dumps(charities)
    return url_tools.render_template(
        "voting.html",
        charities=charities,
        _charities=_charities,
    )

@controller.route("/vote", methods=["POST"])
def _vote():
    form = flask.request.form

    type_ = form.get("submitType")

    if type_ == "vote":
        votedFor = form.get("selectedCharity") 

        if votedFor != None:
            user.setCharity(votedFor)
            voting_db.increment_charity(votedFor)
    elif type_ == "tweet":
        tweet()

    return flask.redirect(flask.url_for("mod_voting.vote"))


def tweet():
    print('tweet')
    form = flask.request.form
    votedFor = form.get("selectedCharity")
    if votedFor != None:
        tweeting.tweetVoteMessage(votedFor)
        flask.flash("You just tweeted for your voted charity!")
