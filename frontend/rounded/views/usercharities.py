from . import controller
import flask, json
from flask_googlemaps import Map
from rounded.core import charity_causes
from rounded.core.charity_navigator import recommend

@controller.route("/user-charities", methods=["GET"])
def userCharities():
    map = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        style="height:500px;width:100%;",
        markers=[(37.4419, -122.1419)] # replace with actual markers of locations later on
    )
    causes = recommend.write_final_rec('user1')
    return flask.render_template("usercharities.html", map=map, causes=causes)

# for all of a user's charity interests, get a list of charities and display as a list