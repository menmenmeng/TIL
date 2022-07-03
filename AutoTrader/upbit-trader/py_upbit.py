import requests
import json
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
from cert import cert # certification key module

# market code 알아오는 코드
# market_info_url = "https://api.upbit.com/v1/market/all"
# market_codes = requests.get(market_info_url).json()
# print(market_codes) # 비트코인 : KRW-BTC, 이더리움 : KRW-ETH

# market codes list
kr_bit = 'KRW-BTC'
kr_eth = 'KRW-ETH'

# keys
access_key = cert.access_key
secret_key = cert.secret_key

# url
server_url = 'https://api.upbit.com/'

# ticker : 현재 시세
def ticker(market_code):
    ticker_url = server_url + f'v1/ticker?markets={market_code}'
    res = requests.get(ticker_url).json()
    print(json.dumps(res, indent=2))
    return res

# candle : 분봉 정보
def candle(marketCode=kr_bit, candleType='minutes', candleUnit=5, candleCount=3):
    candle_url = server_url + f'v1/candles/{candleType}/{candleUnit}?market={marketCode}&count={candleCount}'
    res = requests.get(candle_url).json()
    print(json.dumps(res, indent=2))
    return res

# account : 계정 정보
def account(access_key, secret_key):
    account_url = server_url + 'v1/accounts'

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(account_url, headers=headers).json()
    print(json.dumps(res, indent=2))
    return res

# 주문 가능 정보 확인
def orders_chance(market_code, access_key, secret_key):
    query = {
        'market': market_code,
    }
    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.get(server_url + "/v1/orders/chance", params=query, headers=headers)

    print(json.dumps(res.json(), indent=2))
    return res

# 일정 기간 동안의 시세를 가져오기(시, 고, 저, 종)



# 주문하기
# side : 'bid'(매수), 'ask'(매도) 중 하나
# volume : 주문량. 지정가, 시장가 매도 시 필수
# price : 지정가 시 1btc당 가격, 시장가 매수 시 얼마 살 건지
# ord_type : 'limit'(지정가 주문), 'price'(시장가 매수), 'market'(시장가 매도)
def orders(marketCode, side, ord_type, volume=None, price=None):
    query = {
        'market': marketCode,
        'side': side,
        'ord_type': ord_type,
    }
    if volume:
        query['volume'] = volume
    if price:
        query['price'] = price

    query_string = urlencode(query).encode()

    m = hashlib.sha512()
    m.update(query_string)
    query_hash = m.hexdigest()

    payload = {
        'access_key': access_key,
        'nonce': str(uuid.uuid4()),
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }

    jwt_token = jwt.encode(payload, secret_key)
    authorize_token = 'Bearer {}'.format(jwt_token)
    headers = {"Authorization": authorize_token}

    res = requests.post(server_url + "/v1/orders", params=query, headers=headers)
    print(json.dumps(res.json(), indent=2))
    return res


# 실험용 function
def run_func():
    n = 'running'
    while n!='n':
        print('Function lists.')
        print('-- ticker:t, candle:c, account:a, orders_chance:oc, price(bid):price, market(ask):market')
        n = str(input('Function you want to run(quit:input "n"):'))
        if n == 't':
            ticker(kr_bit)
        elif n == 'c':
            candle()
        elif n == 'a':
            acc = account(access_key, secret_key)
            btc_bal = float(acc[1]['balance'])
            print(btc_bal)
        elif n == 'oc':
            orders_chance(kr_bit, access_key, secret_key)
        elif n == 'market':
            # bid - ask
            # limit - price - market
            # volume(시장가 매도 시 필수, market 시)
            # price(시장가 매수 시 필수, price 시)
            acc = account(access_key, secret_key)
            btc_bal = float(acc[1]['balance'])
            print(btc_bal)
            orders(kr_bit, 'ask', 'market', volume=btc_bal)
        elif n == 'price':
            orders(kr_bit, 'bid', 'price', price=5000)
        elif n != 'n':
            print('Input valid text.')
        else:
            break

# if __name__ == '__main__':
#     run_func()