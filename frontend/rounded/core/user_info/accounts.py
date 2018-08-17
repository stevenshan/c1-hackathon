import json
import requests

class Client(object):
    firstName = ""
    lastName = ""
    state = ""
    city = ""
    zip = ""
    id = ""
    charity_account_id = ""

    def __init__(self, firstName, lastName, zip, state, city, id):
        self.firstName = firstName
        self.lastName = lastName
        self.state = state
        self.city = city
        self.zip = zip
        self.id = id
        self.charity_account_id = ""

def make_client_object(firstName, lastName, zip, state, city, id):
    client = Client(firstName, lastName, zip, state, city, id)
    return client

# returns list of all customers
def get_customers(key):
    url = "http://api.reimaginebanking.com/accounts"

    querystring = {"key":key}

    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "cbbebf39-ce47-4d89-9ee6-65a6a5049ba8"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)
    # print(json.dumps(response, indent=2))

    return response;

#returns customer id
def get_customers_id(response, user_nickname):
    user_nickname = "Jamey's Account"
    for customer in response:
        if customer["nickname"] == user_nickname:
            customer_id = customer["customer_id"]

    return customer_id;

# returns customer object
def make_client(key, customer_id):
    url = "http://api.reimaginebanking.com/customers/" + customer_id

    querystring = {"key":key}

    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "fee9e27b-939d-4b52-8428-365532f8b223"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)
    client = make_client_object(response["first_name"], response["last_name"], response["address"]["zip"], response["address"]["state"], response["address"]["city"], response["_id"])
    return client;

# gets customer accounts
def get_customers_accounts(key, client):
    url = "http://api.reimaginebanking.com/customers/" + client.id + "/accounts"

    querystring = {"key":key}

    headers = {
        'Cache-Control': "no-cache",
        'Postman-Token': "e6a97f1b-82b2-43f0-82a9-8cf323b1adee"
        }

    customer_accounts = requests.request("GET", url, headers=headers, params=querystring)
    customer_accounts = json.loads(customer_accounts.text)
    # print(json.dumps(customer_accounts, indent=2))

    return customer_accounts;

# adds charity account
def add_account(key, client):
    url = "http://api.reimaginebanking.com/customers/" + client.id + "/accounts"

    querystring = {"key":key}

    payload = "{\n  \"type\": \"Checking\",\n  \"nickname\": \"Charity Account\",\n  \"rewards\": 0,\n  \"balance\": 0,\n  \"account_number\": \"8888888888888888\"\n}"
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "1ed1a184-f90c-4257-815b-0daffe14761f"
        }

    account = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    account = json.loads(account.text)
    client.charity_account_id = account["objectCreated"]["_id"]

    return;

# deletes account
def delete_account(key, client):
    url = "http://api.reimaginebanking.com/accounts/" + client.charity_account_id

    querystring = {"key":key}

    payload = "{\n  \"type\": \"Checking\",\n  \"nickname\": \"Charity Account\",\n  \"rewards\": 0,\n  \"balance\": 0,\n  \"account_number\": \"0000000000000000\"\n}"
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "631eb2c9-e8bd-4540-a2ed-9da03568d4b1"
        }

    response = requests.request("DELETE", url, data=payload, headers=headers, params=querystring)

    return;

# gets account balance for either charity or checking
def get_account_balance(key, client):
    url = "http://api.reimaginebanking.com/accounts/5b75bbddf0cec56abfa436a6"

    querystring = {"key":key}

    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "2adf0288-3d14-4b72-8cb8-fbd7abcb4d83"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)

    def floatPrecision(val):
        return float("{0:.2f}".format(val))

    amount = floatPrecision(response["balance"])
    amount = amount - int(amount)

    return floatPrecision(amount);

# adds to charity balance
def add_charity_balance(key, client):
    amount = get_account_balance(key, client)

    if (0.001 < amount and amount != 1.0):
        # withdraw money from main account
        withdraw_from_balance(key, amount, "5b75bbddf0cec56abfa436a6")

        url = "http://api.reimaginebanking.com/accounts/5b75bb6ef0cec56abfa436a7/deposits"

        querystring = {"key":key}

        payload = "{\n  \"medium\": \"balance\",\n  \"amount\": " + str(amount) + "\n}"
        headers = {
            'Content-Type': "application/json",
            'Cache-Control': "no-cache",
            'Postman-Token': "a665b30c-4d8f-4c8b-b838-3eb30c026bd3"
            }

        response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    return;

# deletes amount from balance
def withdraw_from_balance(key, amount, account_id):
    url = "http://api.reimaginebanking.com/accounts/" + account_id + "/withdrawals"

    querystring = {"key":key}

    payload = "{\n  \"medium\": \"balance\",\n  \"amount\": " + str(amount) + "\n}"
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "9ba7e0d9-39c6-4ee0-94ec-42c7714dcaf1"
        }

    response = requests.request("POST", url, data=payload, headers=headers, params=querystring)

    return;
