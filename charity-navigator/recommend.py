from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *
from find_charity import *
from user_data import *
import ujson

num_recs = 10
user = 'user1'
db_name = "team-2"
secret_token = "SFgtcueq51BZqYNKN8QMm9HuuWCN0lPOtUTZpwjg8uquAQ1ggzLtrEMaBceN9AD9"
client = RecombeeClient(db_name, secret_token)

global all_charity_data

# client.send(AddItemProperty('cause', 'string'))
# client.send(AddItemProperty('rating', 'int'))
# client.send(AddItemProperty('state', 'string'))

def output_dict():
	all_charity_data = output_all()
	print('done getting charities')
	with open('data.json', 'w+') as outfile:
		ujson.dump(all_charity_data, outfile)

def get_dict():
	global all_charity_data
	with open('data.json', 'r') as infile:
		all_charity_data = ujson.load(infile)


def add_items():
	results = client.send(ListItems())
	print(results)
	for item_id in results:
		client.send(DeleteItem(item_id))
	# return

	all_charities_dict = all_charity_data
	for id in all_charities_dict.keys():
		org = all_charities_dict[id]
		client.send(AddItem(id))
		values = {'cause': org['cause'], 'rating': org['rating'], 'state': org['state']}
		client.send(SetItemValues(id, values)) #optional parameters:cascade_create=<boolean>))


def add_donation(user, charity_navigator_url):
	r = AddPurchase(user, charity_navigator_url)
	client.send(r)

def get_recommendations(user):
	recommended = client.send(RecommendItemsToUser(user, num_recs, min_relevance='medium'))
	ids = []
	for rec in recommended['recomms']:
	 	ids.append(rec['id'])
	recommended_list = ids
	hard_coded_suggestions = access_suggestions()
	return (recommended_list, hard_coded_suggestions)

def add_rejection(user, item):
	client.send(AddRating(user, item, 1))

def get_index_in_ML_list(recommended_list, item_id):
	try:
		return recommended_list.index(item_id)
	except ValueError:
		return num_recs
		

def get_index_in_hard_coded_list(hard_coded_suggestions, item_id):
	try:
		return hard_coded_suggestions.index(item_id)
	except ValueError:
		return num_recs

def sort_recommendations(user):
	get_dict()
	(recommended_list, hard_coded_suggestions) = get_recommendations(user)
	sorted_list = sorted(recommended_list+hard_coded_suggestions, 
		key = lambda item_id: (get_index_in_ML_list(recommended_list, item_id) + get_index_in_hard_coded_list(hard_coded_suggestions, item_id))/2, reverse=True)[:num_recs]
	print(sorted_list)
	return [{'charityName': all_charity_data[item_id]['charityName'], 'mission': all_charity_data[item_id]['mission']} 
	for item_id in sorted_list 
	if item_id in all_charity_data.keys()]



#print(sort_recommendations('user1'))










