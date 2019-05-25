import requests
import json
import math


def post(method, params, port):
	url = "http://127.0.0.1:" + port + "/rpc"
	headers = {'content-type': 'application/x-www-form-urlencoded'}

	payload = {
	"method": method,
	"params": params,
	"jsonrpc": "2.0",
	"id": 1,
	}
	return requests.post(url, data=json.dumps(payload), headers=headers).json()



def my_round(num, bit):
	return math.floor(num * 10 ** bit) / 10 ** bit


def compare_id(a, b):
	f_a = int(a.split(".")[2])
	f_b = int(b.split(".")[2])
	if f_a > f_b :
		return 1
	elif f_a == f_b:
		return 0
	elif f_a < f_b:
		return -1


	
