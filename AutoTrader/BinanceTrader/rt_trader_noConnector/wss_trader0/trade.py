import requests
import hmac
import hashlib
import datetime
from pprint import pprint

from cert import binanceKey
from cert import myvars
from cert import myfuncs

rest_test = myvars.rest_test
rest_base = myvars.rest_base
webs_test = myvars.webs_test
webs_base = myvars.webs_base

API_KEY = binanceKey.API_KEY
SECRET_KEY = binanceKey.SECRET_KEY

serverTime = myfuncs.dt2ms(datetime.datetime.now())

def account_info():
    serverTime = myfuncs.dt2ms(datetime.datetime.now())
    url = rest_base + "/fapi/v2/account"
    totalParams = f"timestamp={serverTime}"

    h = hmac.new(SECRET_KEY.encode('utf-8'), totalParams.encode('utf-8'), hashlib.sha256)
    tp = h.hexdigest()

    headers = {
        "X-MBX-APIKEY":API_KEY
    }

    params ={
        "timestamp":serverTime,
        "signature":tp
    }

    req = requests.get(url, headers=headers, params=params)
    if req.status_code==200:
        res = req.json()
        del res['assets']
        del res['positions']
        pprint(res)
        return res
    else:
        print("something wrong in 'account_info()'")
        print(req.status_code)


def buy(current_price, percentage):
    serverTime = myfuncs.dt2ms(datetime.datetime.now())
    user_data = account_info()
    available = user_data['availableBalance']
    amount = round(available*percentage/current_price, 5)

    url = rest_base + "/fapi/v1/order"

    totalParams = f"symbol=BTCUSDT&side=BUY&type=MARKET&quantity={amount}&timestamp={serverTime}"
    h = hmac.new(SECRET_KEY.encode('utf-8'), totalParams.encode('utf-8'), hashlib.sha256)
    tp = h.hexdigest()

    headers = {
        "X-MBX-APIKEY":API_KEY
    }
    params = {
        "symbol":"BTCUSDT",
        "side":"BUY",
        "type":"MARKET",
        "quantity":amount,
        "timestamp":serverTime,
        "signature":tp
    }

    req = requests.post(url, headers=headers, params=params)
    if req.status_code==200:
        pprint(req.json())
        return req.json()
    else:
        print("something wrong in 'buy()'")
        print(req.status_code)




def sell(current_price, percentage):
    serverTime = myfuncs.dt2ms(datetime.datetime.now())
    user_data = account_info()
    available = user_data['availableBalance']
    amount = round(available*percentage/current_price, 5)

    url = rest_base + "/fapi/v1/order"

    totalParams = f"symbol=BTCUSDT&side=SELL&type=MARKET&quantity={amount}&timestamp={serverTime}"
    h = hmac.new(SECRET_KEY.encode('utf-8'), totalParams.encode('utf-8'), hashlib.sha256)
    tp = h.hexdigest()

    headers = {
        "X-MBX-APIKEY":API_KEY
    }
    params = {
        "symbol":"BTCUSDT",
        "side":"SELL",
        "type":"MARKET",
        "quantity":amount,
        "timestamp":serverTime,
        "signature":tp
    }

    req = requests.post(url, headers=headers, params=params)
    if req.status_code==200:
        pprint(req.json())
        return req.json()
    else:
        print("something wrong in 'sell()'")
        print(req.status_code)