from . import controller
from rounded.core import url_tools
import flask

@controller.route("/", methods=["GET"])
def homepage():
    return flask.redirect(flask.url_for("app.setup"))

