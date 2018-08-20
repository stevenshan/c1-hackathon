import rounded

# setup app and request context
app = rounded.create_app()
ctx = app.test_request_context()
ctx.push()

from rounded.core.user_info import accounts
from config import Config
import time

def timer(duration):
    start = time.time()
    current = start

    print("\n")
    while current - start < duration:
        current = time.time()
        time.sleep(0.5)
        print(duration - (current - start), end="\r")
    print("\n")

API_key = Config.NESSIE_KEY
CUSTOMER = Config.CUSTOMER

CHARITY_ACCT_ID = accounts.get_charity_account_id()
CHECKING_ACCT_ID = accounts.get_checking_account_id()

client = accounts.get_client()
customer_accounts = accounts.get_customers_accounts(client)

checking_balance = accounts.get_account_balance(CHECKING_ACCT_ID)
print(checking_balance)
charity_balance = accounts.get_account_balance(CHARITY_ACCT_ID)
print(charity_balance)

accounts.add_charity_balance()

timer(50)

final_checking_balance = accounts.get_account_balance(CHECKING_ACCT_ID)
print(final_checking_balance)
final_charity_balance = accounts.get_account_balance(CHARITY_ACCT_ID)
print(final_charity_balance)
# accounts.withdraw_from_balance()
