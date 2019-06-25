import client
import pdb
import time
account = client.Account("trade-1", "password", "8093")
full = account.get_full_account("trade-1")
for item in full["limit_orders"]:
	print("cancel ", item['id'])
	time.sleep(0.2)
	account.cancel_order(item['id'])

