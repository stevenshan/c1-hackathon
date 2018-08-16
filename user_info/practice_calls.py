import accounts

API_key = "5843532b7d4678ebf648c08c09c61d81"
customers = accounts.get_customers(API_key)
customers_id = accounts.get_customers_id(customers, "Jamey's Account")
client = accounts.make_client(API_key, customers_id)
customer_accounts = accounts.get_customers_accounts(API_key, client)

# accounts.add_account(API_key, client)
# accounts.delete_account(API_key, client)

# accounts.get_account_balance(API_key, client)
accounts.add_charity_balance(API_key, client)
# accounts.withdraw_from_balance()
