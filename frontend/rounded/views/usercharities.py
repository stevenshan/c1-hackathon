from . import controller
import flask, json
from flask_googlemaps import Map

# this will be filtered out later if needed
charities = ["Children's and Family Services",
'Homeless Services',
'Youth Development, Shelter, and Crisis Services',
'Food Banks, Food Pantries, and Food Distribution',
'Social Services',
'Multipurpose Human Service Organizations',
'Scholarship and Financial Support',
'Private Liberal Arts Colleges',
'Youth Education Programs and Services',
'Education Policy and Reform',
'Social and Public Policy Research',
'Other Education Programs and Services',
'Private Elementary and Secondary Schools',
'Universities, Graduate Schools, and Technological Institutes',
'Early Childhood Programs and Services',
'International Peace, Security, and Affairs',
'Development and Relief Services',
'Humanitarian Relief Supplies',
'Foreign Charity Support Organizations',
'Advocacy and Education',
'Religious Media and Broadcasting',
'Religious Activities',
'Zoos and Aquariums']

@controller.route("/user-charities", methods=["GET"])
def userCharities():
    map = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        style="height:500px;width:100%;",
        markers=[(37.4419, -122.1419)] # replace with actual markers of locations later on
    )
    return flask.render_template("usercharities.html", map=map, charities=charities)

# for all of a user's charity interests, get a list of charities and display as a list