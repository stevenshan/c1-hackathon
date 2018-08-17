import flask
from rounded.mod_voting import controller

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
'Social and Public Policy Research']

charities.sort() # by popularity

@controller.route("/vote", methods=["GET"])
def voting():
    userBalance = 100.25
    return flask.render_template("voting.html", firstCharity=charities[0], charities=charities[1:], userBalance=userBalance)

# need leaderobard on left side
# options to vote now or view other charities to vote for
