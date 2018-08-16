from . import controller
import flask, json
from flask_googlemaps import Map

@controller.route("/user-charities", methods=["GET"])
def userCharities():
    map = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        style="height:500px;width:100%;",
        markers=[(37.4419, -122.1419)] # replace with actual markers of locations later on
    )
    return flask.render_template("usercharities.html", map=map)