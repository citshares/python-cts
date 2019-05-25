import client
import pdb
from util import *
from datetime import datetime
import csv



def get_current_transfer(history, index, last):
	if index > len(history) - 1:
		return -1
		
	for i in range(index, -1, -1):
		if history[i]['op'][0] == 0:
			if compare_id(history[i]['id'], last) > 0:
				return i
				
	return -1
def analyse_transfer(info):
	from_account = info["op"][1]["from"]
	amount = info['op'][1]["amount"]
	memo_info = {}
	if "memo" in info['op'][1].keys():
		memo = info['op'][1]['memo']
		memo_info = bts_charge_account.read_memo(memo)["result"]
	return {"from": from_account, "amount": amount, "memo": memo_info}



def is_correct_transfer(order, min_charge_amount, cts_charge_account, max_charge_amount, bts_charge_account):
	if order['from'] == bts_charge_account.get_id():
		return -6
	if order["amount"]["asset_id"] != "1.3.113":
		return -1
	if order["amount"]["amount"] < min_charge_amount:
		return -2
	if order['amount']['amount'] > cts_charge_account.balance_asset("1.3.1"):
		return -3
	if order['amount']['amount'] > max_charge_amount:
		return -5
	if not cts_charge_account.find_account(order["memo"]):
		return -4
	return 0

def handle_charge_order(order, min_charge_amount, cts_charge_account, FEE, bts_charge_account, max_charge_amount): 
	ret = is_correct_transfer(order, min_charge_amount, cts_charge_account, max_charge_amount, bts_charge_account)
	if ret < 0:
		print(ret)
		if ret == -3:
			r = bts_charge_account.transfer2(order["from"], str(order['amount']['amount'] / 10000), "CNY", "Do Not Have Enought CTSCNY")
			print(r)
		if ret == -5:
			r = bts_charge_account.transfer2(order["from"], str(order['amount']['amount'] / 10000), "CNY", "Max Limit is {} CNY".format(max_charge_amount/10000) )
			print(r)
		return ret
	print("send cts")
	amt = (order['amount']['amount'] * (1 - FEE) ) / 10000
	ret = cts_charge_account.transfer2(order["memo"], str(amt), "CNY", "{} amount - FEE = {} - {} = {}   ".format(order['memo'], order['amount']['amount']/10000, FEE, amt))
	if "result" in ret.keys():
		tx = ret['result'][0]
		amt2 = order['amount']['amount'] / 10000
		ret2 = bts_charge_account.transfer2("cts-chongzhi-cold", str(amt2), "CNY", "{}:{} {} {}".format(order["from"], order["memo"], amt, tx))
	return ret	




cts_charge_account = client.Account("cts-chongzhi", "password", "8090")
cts_charge_account.unlock()
bts_charge_account = client.Account("cts-chongzhi", "password", "8091")
bts_charge_account.unlock()
history = bts_charge_account.get_activity_history(100)

min_charge_amount = 1  * 10000
max_charge_amount = 100 * 10000
FEE = 0

index = len(history) - 1

recoder_file = open("charge.csv", "r")
reader = csv.reader(recoder_file)
for row in reader:
	last = row[0]
	print(last)

if not "last" in locals().keys():
	last = "1.11.873394504"


recoder_file.close()

recoder_file = open("charge.csv", "a")
writer = csv.writer(recoder_file)


	

while index >= 0:
	print("index ",index)
	index = get_current_transfer(history, index, last)
	print("after index ",index)
	if index < 0:
		break
	last = history[index]['id']
	print("last ",last)
	order = analyse_transfer(history[index])
	print("order ", order)
	ret = handle_charge_order(order, min_charge_amount, cts_charge_account, FEE, bts_charge_account, max_charge_amount)
	writer.writerow([last,  ret, datetime.now()])
	index = index - 1


recoder_file.close()

