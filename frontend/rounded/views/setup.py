from . import controller
import flask, json
from rounded.core import charity_causes, url_tools, firebase
import base64

@controller.route("/setup", methods=["GET"])
def setup():
    interests = firebase.get_interests()
    causes = [{
        "name": x,
        "value": base64.b64encode(x.encode("utf8")).decode("utf8"),
        "active": (x in interests),
    } for x in charity_causes.CAUSES]
    return url_tools.render_template("setup.html", causes=causes)

@controller.route("/setup", methods=["POST"])
def _setup():
    causes = flask.request.form.getlist("cause[]")

    def decode(x):
        return base64.b64decode(str(x).encode("utf8")).decode("utf8")

    causes = [decode(x) for x in causes]

    firebase.change_interests(causes)

    return flask.redirect(flask.url_for("app.accountoverview"))
