from . import controller
import flask, json
from flask_wtf import FlaskForm

charityCauses = ["Children's and Family Services",
'Homeless Services',
'Youth Development, Shelter, and Crisis Services',
'Food Banks, Food Pantries, and Food Distribution',
'Social Services',
'Multipurpose Human Service Organizations',
'Scholarship and Financial Support',
'Private Liberal Arts Colleges',
'Youth Education Programs and Services',
'Education Policy and Reform',
'Special Education',
'Adult Education Programs and Services',
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
'Zoos and Aquariums',
'Wildlife Conservation',
'Animal Rights, Welfare, and Services',
'Libraries, Historical Societies and Landmark Preservation',
'Museums',
'Public Broadcasting and Media', 
'Performing Arts', 
'Botanical Gardens, Parks, and Nature Centers',
'Environmental Protection and Conservation',
'Patient and Family Support',
'Diseases, Disorders, and Disciplines',
'Treatment and Prevention Services',
'Medical Research',
'Community Foundations',
'United Ways',
'Jewish Federations',
'Fundraising',
'Housing and Neighborhood Development',
'Non-Medical Science & Technology Research',
'Social and Public Policy Research']

@controller.route("/setup", methods=["GET"])
def setup():
    return flask.render_template("setup.html", charityCauses=charityCauses)


def checkBoxes