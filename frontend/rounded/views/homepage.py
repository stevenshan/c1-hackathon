from . import controller
import flask

@controller.route("/", methods=["GET"])
def homepage():
    return flask.render_template("setup-modal.html")

