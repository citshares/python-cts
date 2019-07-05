from util import *
import pdb

def get_object(o, port):
        return post('get_object', o, port)


def get_account(account_id, port):
        return post("get_account", [account_id], port)

def get_full_account(account, port):
	return post("get_full_account", [account], port)


def get_asset(asset_name, port):
        return post('get_asset', [asset_name],port)['result']

def get_asset_precision(asset_name,port):
        asset_info = get_asset(asset_name, port)
        if "precision" in asset_info.keys():
                return int(asset_info['precision'])
        else:
                return Null

def propose_parameter_change(proposing_account, exiration_time, changed_values , port):
        return post('propose_parameter_change', [proposing_account, exiration_time, changed_values, True], port)

def propose_change_worker_budget_per_day(proposing_account, budget_per_day, exiration_time, port):
        budget_per_day = budget_per_day * 100000
        info  = { "worker_budget_per_day": str(budget_per_day) }
        return propose_parameter_change(proposing_account, exiration_time, info, port)

def list_account_balances(account, port):
        return post("list_account_balances", [account], port)

def list_witness(count, port):
	return post("list_witnesses", [1, count], port)['result']

def get_vesting_balances(name, port):
	return post("get_vesting_balances", [name], port)['result']



