from blockchain import *

def publish_feed_price(account, cts_amount, asset_name, asset_id, asset_amount, port):
        feed = {"settlement_price" : {
                    "base": {
                         "amount":int(asset_amount),
                         "asset_id": asset_id,
                         },
                    "quote":{
                         "amount":int(cts_amount),
                         "asset_id":"1.3.0"
                         }
                    },
                    "maintenance_collateral_ratio" : 1750,
                    "maximum_short_squeeze_ratio" : 1100,
                    "core_exchange_rate": {
                         "base":{
                              "amount":int(asset_amount),
                              "asset_id": asset_id,
                          },
                          "quote":{
                              "amount":int(cts_amount * 1.05),
                              "asset_id":"1.3.0"
                          }
                    }
               }
        return post('publish_asset_feed', [account, asset_name, feed, True], port)


