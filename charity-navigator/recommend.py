from recombee_api_client.api_client import RecombeeClient
from recombee_api_client.api_requests import *
from find_charity import *


db_name = "team-2"
secret_token = "SFgtcueq51BZqYNKN8QMm9HuuWCN0lPOtUTZpwjg8uquAQ1ggzLtrEMaBceN9AD9"

client = RecombeeClient(db_name, secret_token)

# client.send(AddItemProperty('cause', 'string'))
# client.send(AddItemProperty('rating', 'int'))
# client.send(AddItemProperty('state', 'string'))


def add_items():
	results = client.send(ListItems())
	print(results)
	for item_id in results:
		client.send(DeleteItem(item_id))
	# return

	all_charities_dict = output_all()
	for id in all_charities_dict.keys():
		org = all_charities_dict[id]
		client.send(AddItem(id))
		values = {'cause': org['cause'], 'rating': org['rating'], 'state': org['state']}
		client.send(SetItemValues(id, values)) #optional parameters:cascade_create=<boolean>))


def add_donation(user, charity_navigator_url):
	r = AddPurchase(user, charity_navigator_url)
	client.send(r)

def get_recommendations(user):
	recommended = client.send(RecommendItemsToUser(user, 5))
	return recommended

def add_rejection(user, item):
	client.send(AddRating(user, item, 1))


#add_items()
# d = output_all()
# add_donation('user1', '201612161')
# recs = get_recommendations('user1')
# ids = []
# for rec in recs['recomms']:
# 	ids.append(rec['id'])
# print([d[item_id]['charityName'] for item_id in ids])









