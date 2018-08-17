from . import controller
import flask, json
from flask_googlemaps import Map
from rounded.core import charity_causes
from rounded.core.charity_navigator import recommend, find_charity, user_data
from rounded.core.user_info import accounts
import requests

@controller.route("/user-charities", methods=["GET"])
def userCharities():

	API_key = "5843532b7d4678ebf648c08c09c61d81"
	customers = accounts.get_customers(API_key)
	customers_id = accounts.get_customers_id(customers, "Jamey's Account")
	client = accounts.make_client(API_key, customers_id)

	charitiesByLocation = find_charity.get_suggestions_by_city(client.city)
	charityMarkers = []

	for charity in charitiesByLocation:
		mailingAddress = charity['mailingAddress']
		charityMarkers.append(tuple((convertAddressToLatLong(mailingAddress)).values()))

	charityMarkers = [c for c in charityMarkers[:5] if len(list(c)) >= 2]
	print(charityMarkers)
	map = Map(
    	identifier="view-side",
    	lat=34.9048814,#charityMarkers[0][0],
    	lng=-77.23134360000002,#charityMarkers[0][1],
		style="height:500px;width:100%;",
		markers=[(34.9048814, -77.23134360000002)] # replace with actual markers of locations later on
	)


	causes = recommend.write_final_rec('user1')
	return flask.render_template("usercharities.html", map=map, causes=causes)

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
	# print(json.dumps(response, indent=2))
	#print(response['results'][0]['geometry'])
	if len(response['results'])>0:
		return response['results'][0]['geometry']['location'];
	return {}