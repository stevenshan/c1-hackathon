import json
import requests

url = "http://api.reimaginebanking.com/accounts"

querystring = {"key":"5843532b7d4678ebf648c08c09c61d81"}

headers = {
    'Cache-Control': "no-cache",
    'Postman-Token': "cbbebf39-ce47-4d89-9ee6-65a6a5049ba8"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
response = json.loads(response.text)
print(json.dumps(response, indent=2))

user_nickname = "Jamey's Account"
for customer in response:
    if customer["nickname"] == user_nickname:
        customer_id = customer["customer_id"]

print customer_id

url = "http://api.reimaginebanking.com/customers/" + customer_id + "/accounts"

querystring = {"key":"5843532b7d4678ebf648c08c09c61d81"}

headers = {
    'Cache-Control': "no-cache",
    'Postman-Token': "e6a97f1b-82b2-43f0-82a9-8cf323b1adee"
    }

customer_accounts = requests.request("GET", url, headers=headers, params=querystring)
customer_accounts = json.loads(customer_accounts.text)
print(json.dumps(customer_accounts, indent=2))
