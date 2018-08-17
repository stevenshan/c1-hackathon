from . import controller
from rounded.core import firebase
import flask, json
from rounded.core import charity_causes
import base64

@controller.route("/setup", methods=["GET"])
def setup():
    db = firebase.getDB()
    interests = firebase.get_interests(db)
    causes = [{
        "name": x,
        "value": base64.b64encode(x.encode("utf8")).decode("utf8"),
        "active": (x in interests),
    } for x in charity_causes.CAUSES]
    return flask.render_template("setup.html", causes=causes)

@controller.route("/setup", methods=["POST"])
def _setup():
    causes = flask.request.form.getlist("cause[]")

    def decode(x):
        return base64.b64decode(str(x).encode("utf8")).decode("utf8")

    causes = [decode(x) for x in causes]

    db = firebase.getDB()

    firebase.change_interests(db, causes)

    return flask.redirect(flask.url_for("app.setup"))
