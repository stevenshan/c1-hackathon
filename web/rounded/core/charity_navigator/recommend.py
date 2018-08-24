import recombee_api_client
from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *
from .find_charity import *
from .user_data import *
import json
from rounded.core import redis
from .. import firebase 
import os
from flask import current_app as app

num_recs = 10
user = 'user1'

client = RecombeeClient(*app.config.get("RECOMBEE"))

global all_charity_data

# client.send(AddItemProperty('cause', 'string'))
# client.send(AddItemProperty('rating', 'int'))
# client.send(AddItemProperty('state', 'string'))

# def output_dict():
# 	return 
	
# 	all_charity_data = output_all()
# 	print('done getting charities')

# 	# db = connect_to_db()

# 	db = redis.from_url(url)

# 	data = {}
# 	for item_id in all_charity_data:
# 		data_key = all_charity_data[item_id]['charityName']
# 		data[data_key] = all_charity_data[item_id]

# 		temp = data[data_key]
# 		temp["charityName"] = data_key
# 		db.hmset(data_key, temp)
# 		# for key in data[data_key]:
# 		# 	data[data_key][u'{:}'.format(key)] = data[data_key][key]

# 	# with open('data.json', 'w+') as outfile:
# 	# 	ujson.dump(all_charity_data, outfile)
# 	return db

def get_dict():
	global all_charity_data
	# path = os.path.join(
 #    	os.getcwd(),
 #    	os.path.dirname(__file__),
 #        'data.json'
 #    )

	# with open(path, 'r') as infile:
	# 	all_charity_data = json.load(infile)

	class redisJSON:
		def __getitem__(self, field):
			key = redis.hget("idMap", field)

			if key == None:
				return None

			return redis.hgetall(key)

		def __iter__(self):
			self._iterator = (0, self.keys())
			return self

		def __next__(self):
			index, keys = self._iterator
			if index < len(keys):
				index += 1
				return keys[index]
			else:
				raise StopIteration

		def keys(self):
			return redis.hkeys("idMap")

	all_charity_data = redisJSON()

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
	flag = False
	try:
		recommended = client.send(RecommendItemsToUser(user, num_recs, min_relevance='medium'))
	except recombee_api_client.exceptions.ApiTimeoutException as e:
		flag = True
	else:
		ids = []
		for rec in recommended['recomms']:
		 	ids.append(rec['id'])
		recommended_list = ids

	hard_coded_suggestions = access_suggestions()
	if flag:
		recommended_list = hard_coded_suggestions
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

def get_sorted_recommendations(user):
	get_dict()
	(recommended_list, hard_coded_suggestions) = get_recommendations(user)
	sorted_list = sorted(recommended_list+hard_coded_suggestions, 
		key = lambda item_id: (get_index_in_ML_list(recommended_list, item_id) + get_index_in_hard_coded_list(hard_coded_suggestions, item_id))/2, reverse=True)
	sorted_list = [r for r in sorted_list if r in all_charity_data.keys()][:num_recs]
	return [{'charityName': all_charity_data[item_id]['charityName'], 'mission': all_charity_data[item_id]['mission']} 
		for item_id in sorted_list ]

def write_final_rec(user):
	# db = firebase.getDB() #connect_to_db()
	rec_list = get_sorted_recommendations(user)
	write_current_suggestion(rec_list[0])
	return [r['charityName'] for r in rec_list]

#output_dict()
#get_dict()
#print('got dict')
#write_final_rec('user1')










