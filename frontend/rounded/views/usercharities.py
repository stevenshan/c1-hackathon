from . import controller
import flask, json
from flask_googlemaps import Map
from rounded.core import charity_causes
from rounded.core.charity_navigator import recommend, find_charity, user_data
from rounded.core.user_info import accounts
import requests
from multiprocessing import Pool

TESTING = True

@controller.route("/user-charities", methods=["GET"])
def userCharities():

	API_key = "5843532b7d4678ebf648c08c09c61d81"
	customers = accounts.get_customers(API_key)
	customers_id = accounts.get_customers_id(customers, "Jamey's Account")
	client = accounts.make_client(API_key, customers_id)

	charityMarkers = []
	charities = []

	if not TESTING:
		pool = Pool(processes=4)
		charitiesByLocation = find_charity.get_suggestions_by_city(client.city)
		charityMarkers = pool.map(charityMarker, charitiesByLocation[:10],2)
		charityMarkers = [x for x in charityMarkers if x != None]
		charities = recommend.write_final_rec('user1')

	map = Map(
    	identifier="view-side",
    	lat=38.64181689999999,
    	lng=-83.7657646,
		style="height:500px;width:100%;",
		zoom=12,
		# fit_markers_to_bounds=True,
		markers=charityMarkers,
	)


	return flask.render_template("usercharities.html", map=map, charities=charities)

def charityMarker(charity):
	mailingAddress = charity['mailingAddress']
	coords = convertAddressToLatLong(mailingAddress)
	if len(coords) >= 2:
		coords.update({
			"infobox": str(charity["charityName"])
		})
		return coords

	return None

def convertAddressToLatLong(address):
	url = "https://maps.googleapis.com/maps/api/geocode/json"
	googleApiKey = "AIzaSyAIVzJ6N9u3IVhFmdmQ8_TsoF7R2b0C088"

	formattedAddress = address['streetAddress1'] + ', ' + address['city'] + ', ' + address['stateOrProvince']
	querystring = {"address":formattedAddress, "key":googleApiKey}

	headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "cbbebf39-ce47-4d89-9ee6-65a6a5049ba8"
	}

	response = requests.request("GET", url, headers=headers, params=querystring)
	response = json.loads(response.text)
	if len(response['results'])>0:
		return response['results'][0]['geometry']['location'];
	return {}