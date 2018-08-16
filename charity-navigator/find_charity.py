import requests
import json
import pprint

my_zip_code = "22102"
app_id = "267c5c0d"
app_key = "95a6143616abcad971c5966409b0cb52"
my_profile = {}

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

# return dictionary of dictionaries for each cause from API
def get_causes(categories):
	causes = {}
	for cat in categories:
		for cause in cat['causes']:
			causes[cause['causeName']] = cause
	return causes


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

pprint.pprint(get_names(sort_by_ratings(get_suggestions_by_zip(my_zip_code, ['Diseases, Disorders, and Disciplines', 'Medical Research']))))
pprint.pprint(get_names(sort_by_ratings(get_suggestions_by_city('McLean', ['Diseases, Disorders, and Disciplines', 'Medical Research']))))
pprint.pprint(get_names(sort_by_ratings(get_suggestions_by_state('VA', ['Diseases, Disorders, and Disciplines', 'Medical Research']))))