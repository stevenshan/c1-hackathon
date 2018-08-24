from . import controller
import flask, json
from flask_googlemaps import Map
from rounded.core import charity_causes, user, url_tools, firebase
from rounded.core.charity_navigator import recommend, find_charity, user_data
from rounded.mod_voting.lib import db as topDB
from rounded.core.user_info import accounts
from flask import current_app as app
import requests
import os
from multiprocessing import Pool

TESTING = False

@controller.route("/user-charities", methods=["GET"])
def userCharities():

	charityChoice = flask.request.args.get("choose")
	if charityChoice != None:
		user.setCharity(str(charityChoice))
		return flask.redirect(flask.url_for("app.userCharities"))

	customers = accounts.get_customers()
	customers_id = accounts.get_customers_id(customers, app.config.get("CUSTOMER"))
	client = accounts.make_client(customers_id)

	charityMarkers = []
	charities = []

	if not TESTING:
		try:
			pool = Pool(processes=2)
			charitiesByLocation = find_charity.get_suggestions_by_city(client.city)
			charityMarkers = pool.map(charityMarker, charitiesByLocation[:5],2)
			charityMarkers = [x for x in charityMarkers if x != None]
			charities = recommend.write_final_rec('user1')
		except Exception as e:
			print("SKIPPED")
			import traceback
			traceback.print_exc()
			print(e)
			pass
	try:
		map = Map(
	    	identifier="view-side",
	    	lat=38.64181689999999,
	    	lng=-83.7657646,
			style="height:500px;width:100%;",
			zoom=12,
			# fit_markers_to_bounds=True,
			markers=charityMarkers,
		)
	except:
		map = None

	topCharity = topDB.getTopCharity()

	return url_tools.render_template(
		"usercharities.html",
		map=map,
		charities=charities,
		topCharity = topCharity,
	)

def charityMarker(charity):
	mailingAddress = charity['mailingAddress']
	coords = convertAddressToLatLong(mailingAddress)
	if len(coords) >= 2:
		name = str(charity["charityName"])
		coords.update({
			"infobox": '<a href="?choose=' + name + '">' + name + '</a>'
		})
		return coords

	return None

def convertAddressToLatLong(address):
	url = "https://maps.googleapis.com/maps/api/geocode/json"

	formattedAddress = address['streetAddress1'] + ', ' + address['city'] + ', ' + address['stateOrProvince']
	querystring = {
		"address": formattedAddress,
		"key": os.environ.get("GOOGLE_API_KEY")
	}

	response = requests.request("GET", url, params=querystring)
	response = json.loads(response.text)
	if len(response['results'])>0:
		return response['results'][0]['geometry']['location'];
	return {}