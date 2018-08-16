import requests
import json
import pprint

my_zip_code = "22102"
app_id = "267c5c0d"
app_key = "95a6143616abcad971c5966409b0cb52"
my_profile = {}

def get_local_charities(zip_code):
	results = {}

	payload = {"app_id": app_id, "app_key": app_key, "zip": zip_code}
	url = "https://api.data.charitynavigator.org/v2/Organizations"
	r = requests.get(url, params=payload)
	result = r.json()
	for org in result:
		if not('errorMessage' in org.keys()):
			results[org['charityName']] = org
	return results

def get_names(charities):
	return list(charities.keys())


#def get_classification(charity):
# 	return charity['irsClassification']['nteeType']

def get_categories():
	payload = {"app_id": app_id, "app_key": app_key}
	url = "https://api.data.charitynavigator.org/v2/Categories"
	r = requests.get(url, params=payload)
	return r.json()

def get_causes(categories):
	causes = {}
	for cat in categories:
		for cause in cat['causes']:
			causes[cause['causeName']] = cause
	return causes


# get suggestions based on location, interests, ratings
def get_suggestions(zip_code, interests):
	causes = get_causes(get_categories())
	results = {}
	for interest in interests:
		cause_id = causes[interest]['causeID']
		payload = {"app_id": app_id, "app_key": app_key, "zip": zip_code, "causeID": cause_id, "rating": "RATING: DESC"}
		url = "https://api.data.charitynavigator.org/v2/Organizations"
		r = requests.get(url, params=payload)
		result = r.json()
		for org in result:
			if not('errorMessage' in org.keys()):
				results[org['charityName']] = org
	return results



def get_ratings(charities):
	return [c_dict['currentRating']['rating'] for c_dict in charity_list.values()]

pprint.pprint(get_names(get_suggestions(my_zip_code, ['Diseases, Disorders, and Disciplines', 'Medical Research'])))
