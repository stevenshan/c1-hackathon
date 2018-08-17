import accounts
import time
from flask import current_app as app

API_key = "5843532b7d4678ebf648c08c09c61d81"
customers = accounts.get_customers(API_key)
customers_id = accounts.get_customers_id(customers, app.config.get("CUSTOMER"))
client = accounts.make_client(API_key, customers_id)
customer_accounts = accounts.get_customers_accounts(API_key, client)

checking_balance = accounts.get_account_balance(API_key, "5b75bbddf0cec56abfa436a6")
print(checking_balance)
charity_balance = accounts.get_account_balance(API_key, "5b76712cf0cec56abfa437c1")
print(charity_balance)

# accounts.add_account(API_key, client)
# accounts.delete_account(API_key, client)

# accounts.get_account_balance(API_key, client)
accounts.add_charity_balance(API_key, client)
time.sleep(50)

final_checking_balance = accounts.get_account_balance(API_key, "5b75bbddf0cec56abfa436a6")
print(final_checking_balance)
final_charity_balance = accounts.get_account_balance(API_key, "5b76712cf0cec56abfa437c1")
print(final_charity_balance)
# accounts.withdraw_from_balance()
