import requests
import json
import pprint
import sys
from dicttoxml import dicttoxml
sys.path.append("../")
from user_info.accounts import *

global my_zip_code
global my_city
global my_state
app_id = "267c5c0d"
app_key = "95a6143616abcad971c5966409b0cb52"


def state_name_to_postal_code(state):
	state_dict = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
	}
	return state_dict[state]

def get_location():
	global my_zip_code
	global my_city
	global my_state

	nessie_API_key = "5843532b7d4678ebf648c08c09c61d81"
	customers = get_customers(nessie_API_key)
	customers_id = get_customers_id(customers, "Jamey's Account")
	client = make_client(nessie_API_key, customers_id)

	my_zip_code = client.zip
	my_city = client.city
	my_state = state_name_to_postal_code(client.state)



# return list of dictionaries of charities in same zip code
def get_local_charities(zip_code):
	results = {}

	payload = {"app_id": app_id, "app_key": app_key, "zip": zip_code}
	url = "https://api.data.charitynavigator.org/v2/Organizations"
	r = requests.get(url, params=payload)
	result = r.json()
	for org in result:
		if not('errorMessage' in org.keys()):
			results.append(org)
	return results

# return list of names of charities in charity_list
def get_names(charity_list):
	return [c['charityName'] for c in charity_list]


# return list of dictionaries for each category from API
def get_categories():
	payload = {"app_id": app_id, "app_key": app_key}
	url = "https://api.data.charitynavigator.org/v2/Categories"
	r = requests.get(url, params=payload)
	return r.json()

# return dictionary of dictionaries for each cause (interest) from API
def get_causes(categories):
	causes = {}
	for cat in categories:
		for cause in cat['causes']:
			causes[cause['causeName']] = cause
	return causes

# return list of possible interests for each user
def get_possible_interests():
	causes = get_causes(get_categories())
	return list(causes.keys())

# get list of suggestions based on location, interests
def get_suggestions_by_zip(zip_code, interests):
	causes = get_causes(get_categories())
	results = {}
	for interest in interests:
		cause_id = causes[interest]['causeID']
		payload = {"app_id": app_id, "app_key": app_key, "zip": zip_code, "causeID": cause_id}
		url = "https://api.data.charitynavigator.org/v2/Organizations"
		r = requests.get(url, params=payload)
		result = r.json()
		for org in result:
			if not(type(org) is str) and not('errorMessage' in org.keys()):
				results[org['charityName']] = org
	return list(results.values())

# get list of suggestions based on location, interests
def get_suggestions_by_city(city, interests):
	causes = get_causes(get_categories())
	results = {}
	for interest in interests:
		cause_id = causes[interest]['causeID']
		payload = {"app_id": app_id, "app_key": app_key, "city": city, "causeID": cause_id}
		url = "https://api.data.charitynavigator.org/v2/Organizations"
		r = requests.get(url, params=payload)
		result = r.json()
		for org in result:
			if not(type(org) is str) and not('errorMessage' in org.keys()):
				results[org['charityName']] = org
	return list(results.values())

# get list of suggestions based on location, interests
def get_suggestions_by_state(state, interests):
	causes = get_causes(get_categories())
	results = {}
	for interest in interests:
		cause_id = causes[interest]['causeID']
		payload = {"app_id": app_id, "app_key": app_key, "state": state, "causeID": cause_id}
		url = "https://api.data.charitynavigator.org/v2/Organizations"
		r = requests.get(url, params=payload)
		result = r.json()
		for org in result:
			if not(type(org) is str) and not('errorMessage' in org.keys()):
				results[org['charityName']] = org
	return list(results.values())

# sort charity_list in order of descending ratings 
def sort_by_ratings(charity_list):
	charity_list = [c for c in charity_list if 'currentRating' in c.keys()]
	return sorted(charity_list, key = lambda charity: charity['currentRating']['rating'], reverse=True)

# returns list of ratings for each charity
def get_ratings(charity_list):
	return [c_dict['currentRating']['rating'] for c_dict in charity_list]

# get suggestions based on location radius and interests
def get_suggestions(interests, radius='state'):
	get_location()
	if radius=='zip_code':
		return sort_by_ratings(get_suggestions_by_zip(my_zip_code, interests))
	if radius=='city':
		return sort_by_ratings(get_suggestions_by_city(my_city, interests))
	return sort_by_ratings(get_suggestions_by_state(my_state, interests))

# returns (name, url) of charity_name
def get_charity_name_and_url(charity_name):
	payload = {"app_id": app_id, "app_key": app_key, "search": charity_name, "searchType": "NAME_ONLY", "sort": "RELEVANCE"}
	url = "https://api.data.charitynavigator.org/v2/Organizations"
	r = requests.get(url, params=payload)
	result = r.json()[0]
	website = result['websiteURL']
	if website == None: website = result['charityNavigatorURL']
	return (result['charityName'], website)



#pprint.pprint(get_possible_interests())
#pprint.pprint(get_names(get_suggestions(get_possible_interests()[:2])))
#interests = get_possible_interests()
#pprint.pprint(get_names(get_suggestions(interests)))



def output_all():
	print('finding all charities')

	causes = get_causes(get_categories())
	results = {}
	for interest in list(causes.keys()):
		cause_id = causes[interest]['causeID']
		payload = {"app_id": app_id, "app_key": app_key, "causeID": cause_id}
		url = "https://api.data.charitynavigator.org/v2/Organizations"
		r = requests.get(url, params=payload)
		result = r.json()
		for org in result:
			if not(type(org) is str) and not('errorMessage' in org.keys()):
				results[org['charityName']] = org
	#print(results)
	final_results = {}
	#for id in all_results.keys():
	#	org = all_results[id]
	for org_name in results.keys():
		org = results[org_name]
		if not(type(org) is str) and not('errorMessage' in org.keys()):
			if 'cause' in org.keys():
				final_results[org['ein']] = {'charityName': org['charityName'],
											'cause': org['cause']['causeID'],
											'rating': org['currentRating']['rating'],
											'state': org['mailingAddress']['stateOrProvince']}
	return final_results
