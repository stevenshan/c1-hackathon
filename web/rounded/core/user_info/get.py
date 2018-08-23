from rounded.core.user_info import accounts

from flask import current_app as app

NAME = app.config.get("CUSTOMER")

CUSTOMERS = None
CUSTOMER_ID = None
CLIENT = None
ACCOUNTS = None

def refresh():
    global CUSTOMERS, CUSTOMER_ID, CLIENT, ACCOUNTS
    CUSTOMERS = accounts.get_customers()
    CUSTOMER_ID = accounts.get_customers_id(CUSTOMERS, NAME)
    CLIENT = accounts.make_client(CUSTOMER_ID)
    ACCOUNTS = accounts.get_customers_accounts(CLIENT)

refresh()