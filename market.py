from util import *
from blockchain_cts import *
from blockchain import *
import pdb
def get_order_book(money, asset, depth, port):
        return post("get_order_book", [money, asset, depth], port)['result']


def get_cny_settlement_price(port):
        result = get_object(["2.4.0"], port)["result"]
        cny = result[0]["current_feed"]['settlement_price']['base']['amount']
        bts = result[0]["current_feed"]['settlement_price']['quote']['amount']
        return float(cny) * 10  / float(bts)


def publish_cny_feed_price(account, cts_amount, cny_amount, port):
	return publish_feed_price(account, cts_amount, 'CNY', '1.3.1',cny_amount, port)

def get_asset_supply(asset_name, port):
        dyn = get_asset(asset_name, port)['dynamic_asset_data_id']
        supply = int(post("get_object", [dyn], port)['result'][0]['current_supply'])
        precision = int(get_asset_precision(asset_name, port))
        return (supply / 10 ** precision)



def get_call_orders(asset_name, count, port):
	orders = post("get_call_orders", [asset_name, count], port)
	return orders['result']
	

def get_collateral_amount(asset_name, count, port):
	orders = get_call_orders(asset_name, count, port)
	cts_in_collateral = 0
	for item in orders:
		cts_in_collateral = cts_in_collateral + int(item['collateral'])
	precision = get_asset_precision("CTS", port)
	cts_in_collateral = (cts_in_collateral / 10 ** precision)
	return cts_in_collateral

