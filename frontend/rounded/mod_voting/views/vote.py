import flask
from rounded.mod_voting import controller
import json

charities = [{'name': "Children's and Family Services", 'description': "lorem ipsum delores something I don't feel like typing", 'votes': 817}, {'name': 'Homeless Services', 'description': "lorem ipsum delores something I don't feel like typing", 'votes': 519}, {'name': 'Youth Development, Shelter, and Crisis Services', 'description': "lorem ipsum delores something I don't feel like typing", 'votes': 243}, {'name': 'Food Banks, Food Pantries, and Food Distribution', 'description': "lorem ipsum delores something I don't feel like typing", 'votes': 882}, {'name': 'Social Services', 'description': "lorem ipsum delores something I don't feel like typing", 'votes': 634}, {'name': 'Multipurpose Human Service Organizations', 'description': "lorem ipsum delores something I don't feel like typing", 'votes': 224}, {'name': 'Scholarship and Financial Support', 'description': "lorem ipsum delores something I don't feel like typing", 'votes': 868}, {'name': 'Private Liberal Arts Colleges', 'description': "lorem ipsum delores something I don't feel like typing", 'votes': 69}, {'name': 'Youth Education Programs and Services', 'description': "lorem ipsum delores something I don't feel like typing", 'votes': 480}, {'name': 'Education Policy and Reform', 'description': "lorem ipsum delores something I don't feel like typing", 'votes': 993}, {'name': 'Social and Public Policy Research', 'description': "lorem ipsum delores something I don't feel like typing", 'votes': 335}]

charities.sort(key=lambda x: x["votes"], reverse=True) # by popularity

@controller.route("/vote", methods=["GET"])
def voting():
    _charities = json.dumps(charities)
    return flask.render_template(
        "voting.html",
        charities=charities,
        _charities=_charities,
    )

# need leaderobard on left side
# options to vote now or view other charities to vote for
