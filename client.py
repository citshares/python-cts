from util import *
from blockchain import *
import pdb

class Account(object):
	def __init__(self,name, password, port):
		self.name = name
		self.password = password
		self.port = port
		self.id = post("get_account_id", [name], port)['result']
	def get_name(self):
		return self.name
	def get_id(self):
		return self.id

	def unlock(self):
		post("unlock", [self.password], self.port)
	def get_full_account(self, account):
		return post("get_full_account", [account], self.port)['result']
	def cancel_order(self, order_id):
		return post("cancel_order", [order_id, True], self.port)

	def buy(self, asset, money, price, amount, timeout):
		return post("sell_asset", 	
			[			
				self.name, 	
				str(my_round(price * amount, get_asset_precision(money, self.port))), 
				money,         
				str(my_round(amount, get_asset_precision(asset, self.port))), 
				asset, 
				timeout, "false", "true"
			], self.port)

	def sell(self, asset, money, price, amount, timeout):
		return post("sell_asset", 
			[
				self.name,
				str(my_round(amount, get_asset_precision(asset, self.port))),  
				asset, 
				str(my_round(price * amount, get_asset_precision(money, self.port))),
				money, 
				timeout, "false", "true"
			], self.port)
	def balance(self):
		return list_account_balances(self.name, self.port)['result']
	def balance_asset(self, asset):
		ret = self.balance()
		for item in ret:
			if item['asset_id'] == asset:
				return int(item["amount"])
		return -1

	def get_most_recent(self, op):
		return post("get_object", [op], self.port)

	def get_opertion(self, op):
		return post("get_object", [op], self.port)	

	def read_memo(self, memo):
		return post("read_memo", [memo], self.port)	
	# when call this func, amout should be str
	def transfer2(self, to, amount, asset, memo):
		return post("transfer2", [self.name, to, amount, asset, memo], self.port)
	
	def find_account(self, account):
		ret = post("get_account", [account], self.port)	
		if "error" in ret.keys():
			ret = False
		else:
			pass
		return 	ret
	def get_activity_history(self, counts):
		full_account = get_full_account(self.name, self.port)
		ret = []
		if "error" in full_account.keys():
			return ret
		statistics = full_account['result']["statistics"]
		most_recent_op = self.get_most_recent(statistics["most_recent_op"])
		for i in range(counts):
			if not most_recent_op['result'][0]:
				return ret
			opertion_id = most_recent_op['result'][0]["operation_id"]
			opertion = self.get_opertion(opertion_id)
			if "result" in opertion.keys():
				ret.append(opertion["result"][0])
			else:
				return ret		

			most_recent_op = self.get_most_recent(most_recent_op['result'][0]['next'])


		return ret
