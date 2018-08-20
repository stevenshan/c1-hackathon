import json
import requests
from flask import current_app as app

key = app.config.get("NESSIE_KEY")
CUSTOMER = app.config.get("CUSTOMER")

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

def get_client():
    customers = get_customers()
    customerID = get_customers_id(customers, CUSTOMER)
    client = make_client(customerID)
    return client

# returns list of all customers
def get_customers():
    url = "http://api.reimaginebanking.com/accounts"

    querystring = {"key":key}

    response = requests.request("GET", url, params=querystring)
    response = json.loads(response.text)
    # print(json.dumps(response, indent=2))

    return response

#returns customer id
def get_customers_id(response, user_nickname):
    customer_id = None
    for customer in response:
        if customer["nickname"] == user_nickname:
            customer_id = customer["customer_id"]

    return customer_id

# returns customer object
def make_client(customer_id):
    url = "http://api.reimaginebanking.com/customers/" + customer_id

    querystring = {"key":key}

    headers = {
        'Content-Type': "application/json",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)
    client = make_client_object(response["first_name"], response["last_name"], response["address"]["zip"], response["address"]["state"], response["address"]["city"], response["_id"])
    return client

# gets customer accounts
def get_customers_accounts(client):
    url = "http://api.reimaginebanking.com/customers/" + client.id + "/accounts"

    querystring = {"key":key}

    customer_accounts = requests.request("GET", url, params=querystring)
    customer_accounts = json.loads(customer_accounts.text)
    #print(json.dumps(customer_accounts, indent=2))

    return customer_accounts

# adds charity account
def add_account(client):
    url = "http://api.reimaginebanking.com/customers/" + client.id + "/accounts"

    querystring = {"key":key}

    payload = "{\n  \"type\": \"Checking\",\n  \"nickname\": \"Charity Account\",\n  \"rewards\": 0,\n  \"balance\": 0,\n  \"account_number\": \"8888888888888888\"\n}"
    headers = {
        'Content-Type': "application/json",
    }

    account = requests.request("POST", url, data=payload, headers=headers, params=querystring)
    account = json.loads(account.text)
    client.charity_account_id = account["objectCreated"]["_id"]

    return

# deletes account
def delete_account(client):
    url = "http://api.reimaginebanking.com/accounts/" + client.charity_account_id

    querystring = {"key":key}

    payload = "{\n  \"type\": \"Checking\",\n  \"nickname\": \"Charity Account\",\n  \"rewards\": 0,\n  \"balance\": 0,\n  \"account_number\": \"0000000000000000\"\n}"
    headers = {
        'Content-Type': "application/json",
    }

    response = requests.request("DELETE", url, headers=headers, data=payload, params=querystring)

    return

def get_accounts():
    client = get_client()
    return get_customers_accounts(client)

def get_charity_account_id():
    accounts = get_accounts()
    for account in accounts:
        if account.get("nickname") == "Charity Account":
            return account.get("_id")

def get_checking_account_id():
    accounts = get_accounts()
    for account in accounts:
        if (account.get("type") == "Checking" and 
            account.get("nickname") != "Charity Account"):
            return account.get("_id")

# gets account balance for either charity or checking
def get_account_balance(account_id):
    url = "http://api.reimaginebanking.com/accounts/" + account_id

    querystring = {"key":key}

    headers = {
        'Content-Type': "application/json",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)

    return response["balance"]

# gets account balance for either charity or checking
def get_account_difference(client):
    url = "http://api.reimaginebanking.com/accounts/" + get_checking_account_id()

    querystring = {"key":key}

    headers = {
        'Content-Type': "application/json",
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    response = json.loads(response.text)

    def floatPrecision(val):
        return float("{0:.2f}".format(val))

    amount = floatPrecision(response["balance"])
    amount = amount - int(amount)

    return floatPrecision(amount)

# adds to charity balance
def add_charity_balance():
    client = get_client()
    amount = get_account_difference(client)

    if (0.001 < amount and amount != 1.0):
        # withdraw money from main account
        withdraw_from_balance(amount, get_checking_account_id())

        url = ("http://api.reimaginebanking.com/accounts/" + 
               get_charity_account_id() + 
               "/deposits")

        querystring = {"key":key}

        payload = "{\n  \"medium\": \"balance\",\n  \"amount\": " + str(amount) + "\n}"
        headers = {
            'Content-Type': "application/json",
        }

        response = requests.request("POST", url, headers=headers, data=payload, params=querystring)

    return

# deletes amount from balance
def withdraw_from_balance(amount, account_id):
    url = "http://api.reimaginebanking.com/accounts/" + account_id + "/withdrawals"

    querystring = {"key":key}

    payload = "{\n  \"medium\": \"balance\",\n  \"amount\": " + str(amount) + "\n}"
    headers = {
        'Content-Type': "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload, params=querystring)

    return

def make_payment(amount):
    url = ("http://api.reimaginebanking.com/accounts/" + 
           get_checking_account_id() + 
           "/withdrawals")

    querystring = {"key":key}

    payload = "{\n  \"medium\": \"balance\",\n  \"amount\": " + str(amount) + "\n}"
    headers = {
        'Content-Type': "application/json",
    }
    
    response = requests.request("POST", url, headers=headers, data=payload, params=querystring)


