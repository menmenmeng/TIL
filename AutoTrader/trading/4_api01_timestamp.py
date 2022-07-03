import requests
import datetime

r = requests.get("https://api.korbit.co.kr/v1/ticker/detailed?currency_pair=btc_krw")
bitcoin = r.json() # r.text : str, r.json() : json포맷을 dict포맷으로 변환

# Unix timestamp
# timestamp를 1000으로 나눠야 하는 이유는 무야? 일단 외워놔
timestamp = bitcoin['timestamp']
date = datetime.datetime.fromtimestamp(timestamp/1000)
print(date)