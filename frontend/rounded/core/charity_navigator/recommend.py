from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *
from .find_charity import *
from .user_data import *
import json
import redis
from .. import firebase 
import os

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

	db = connect_to_db()

	url = "redis://h:p633e4fabfec649572dc5def69168418c21558611dc98ed1f1bf848198c5ba8b0@ec2-52-5-241-209.compute-1.amazonaws.com:15939"
	db = redis.from_url(url)

	data = {}
	for item_id in all_charity_data:
		data_key = all_charity_data[item_id]['charityName']
		data[data_key] = all_charity_data[item_id]

		temp = data[data_key]
		temp["charityName"] = data_key
		db.hmset(data_key, temp)
		# for key in data[data_key]:
		# 	data[data_key][u'{:}'.format(key)] = data[data_key][key]

	# with open('data.json', 'w+') as outfile:
	# 	ujson.dump(all_charity_data, outfile)
	return db

def get_dict():
	global all_charity_data
	path = os.path.join(
    	os.getcwd(),
    	os.path.dirname(__file__),
        'data.json'
    )
	with open(path, 'r') as infile:
		all_charity_data = json.load(infile)


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

def get_recommendations(user, db):
	recommended = client.send(RecommendItemsToUser(user, num_recs, min_relevance='medium'))
	ids = []
	for rec in recommended['recomms']:
	 	ids.append(rec['id'])
	recommended_list = ids
	hard_coded_suggestions = access_suggestions(db)
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

def get_sorted_recommendations(user, db):
	get_dict()
	(recommended_list, hard_coded_suggestions) = get_recommendations(user, db)
	sorted_list = sorted(recommended_list+hard_coded_suggestions, 
		key = lambda item_id: (get_index_in_ML_list(recommended_list, item_id) + get_index_in_hard_coded_list(hard_coded_suggestions, item_id))/2, reverse=True)[:num_recs]
	print(sorted_list)
	return [{'charityName': all_charity_data[item_id]['charityName'], 'mission': all_charity_data[item_id]['mission']} 
		for item_id in sorted_list 
		if item_id in all_charity_data.keys()]

def write_final_rec(user):
	db = firebase.getDB() #connect_to_db()
	rec_list = get_sorted_recommendations(user, db)
	write_current_suggestion(db, rec_list[0])
	return [r['charityName'] for r in rec_list]

#output_dict()
#get_dict()
#print('got dict')
#write_final_rec('user1')










