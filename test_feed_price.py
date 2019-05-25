import market
import client
import blockchain

def publish_feedprice(account_name, feed_price, wallet_port):
        bts_amount = 100
        cny_amount = bts_amount * feed_price
        ret =market.publish_cny_feed_price(account_name, bts_amount * 100000, cny_amount * 10000, wallet_port)
        print(ret)

#################### start ##############################
# 
# wallet port which cli_wallet opened  
wallet_port = "8093"
# feed price you want to feed
feed_price = 0.01
# account name which you publish your feed price
account_name = "account"
password = "password"
#######################################################

account = client.Account(account_name, password, wallet_port)
account.unlock

cny_supply = market.get_asset_supply("CNY", wallet_port)
print("CNY SUPPLY IS ", cny_supply)

cts_supply = market.get_asset_supply("CTS", wallet_port)
print("CTS total supply is ", cts_supply)

cts_in_collateral = market.get_collateral_amount("CNY", 100, wallet_port)
print("CTS IN COLLATERAL ", cts_in_collateral)

#publish_feedprice(account_name, feed_price, wallet_port)

