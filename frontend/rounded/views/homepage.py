from . import controller
import flask

@controller.route("/", methods=["GET"])
def homepage():
    return flask.render_template("base_page.html")

@controller.route("/test", methods=["GET"])
def test():
    return flask.render_template("setup-modal.html")

