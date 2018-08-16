import requests
import json
import pprint

my_zip_code = 22102
app_id = "267c5c0d"
app_key = "95a6143616abcad971c5966409b0cb52"
my_profile = {}

# returns list of dictionaries, where each dict is info for one charity
def get_local_charities(zip_code):
	payload = {"app_id": app_id, "app_key": app_key, "zip": zip_code}
	url = "https://api.data.charitynavigator.org/v2/Organizations"
	r = requests.get(url, params=payload)
	return r.json()

# get names of charities in charity_list
def get_names(charity_list):
	return [c_dict['charityName'] for c_dict in charity_list]


pprint.pprint(get_names(get_local_charities(my_zip_code)))

