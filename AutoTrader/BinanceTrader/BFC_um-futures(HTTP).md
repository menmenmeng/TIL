용어에 대한 정리 : https://www.binance.us/en/trading-rules

**선물 가격은 어떻게 정해질까**
현물의 가격에 더해, 자본조달비용, 이자비용, 보관비용 등 여러 금액들을 더해서 선물이론가격이 형성.
거기서, 현물이 더 상승할 것이라고 생각되면 선물이론가격에 프리미엄이 붙어서 더 높아지고
(현물이 상승 : 선물을 지금 사 놓는다(롱) --> 만기에 선물을 사서, 현물을 비싸게 판다.)
현물이 하락할 것이라고 생각되면 선물이론가격에 마이너스가 붙는다.
(현물이 하락 : 선물을 지금 팔아 놓는다(숏) --> 만기에 선물을 팔아, 현물을 싸게 산다.)

**차익거래**
매수차익거래 : 선물가가 비싸고, 현물가가 싼 상황(비정상적으로)
- 가격이 싼 현물을 사서, 선물을 비싸게 판다(숏). 
- 선물가는 언젠가 현물가와 같아지게 될 것이기 때문에(현물가가 오르거나, 선물가가 떨어짐) --> 뭐가 됐든 이득!
매도차익거래 : 선물가가 싸고, 현물가가 비싼 상황(비정상적으로, 마찬가지)
- 가격이 비싼 현물을 팔고, 선물을 싸게 산다(롱).
- 선물가가 오르거나 현물가가 떨어진다. 뭐가 되었든 이득

**Bull, Bear Market**
매수세가 강해 주가가 상승하는 강세시장 --> Bull market
매도세가 강해 주가가 하락하는 약세시장 --> Bear market

**달러 강세, 약세**
왜 달러 강세, 약세를 얘기하냐면 주식시장에 비해 조금 다른 얘기인가? 싶어서..
달러 강세 : 다른 통화보다 가치가 더 높아졌다.
원화와 달러 간 환율로 따지면, 어제 원달러환율이 1달러에 1000원 --> 오늘 1달러에 1200원이라면.
1달러를 사기 위해 필요한 원화가 더 비싸졌다. 즉, 달러의 가치가 더 높아졌다는 것. 이런 경우 달러 강세라고 한다.

**펀딩비율**
특수한 경우인 무기한 선물 계약에서 선물가격과 현물가격의 차이를 줄이는 것을 강제하기 위해 만든 것.
선물가가 현물가보다 높다는 얘기는 즉 상승장. 현물가가 상승할 것이라는 예측을 한 거다.
그래서 롱 포지션의 사람이 많고, 숏 포지션이 적다. 선물가와 현물가의 차이가 커질 수 있다..? 왜? 이게 지속되는 걸 방지하기 위해 롱 포지션이 숏 포지션에게 일정 비용(펀딩금리)를 지불한다.
숏 포지션은 펀딩금리를 보고, 상승장에서도 숏 포지션에 들어갈 수 있다. --> 가격 안정화.
거래자는 변동성이 낮은 시장에서도 펀딩 비율과 이익을 활용하는 거래 전략을 개발할 수 있다.

**Volume(거래량)과 Open Interest와의 차이?**
liquidity and activity를 묘사할 수 있는 가장 중요한 두 가지 지표이다.
Volume : 주어진 시간 동안 trade된 contract의 수. Open, Close transaction이 모두.. 여기에 포함된다.
- Volume이 크고 살짝 상승할 기미가 보이는 것 --> trend가 상승할 수 있다. 주가랑 거래량밖에 없는 그 상황에서, 거래량이 많다면 trend가 진행되고 있다고 생각할 수도 있음.
- 더 많은 volume은 더 많은 유동성을 뜻한다. 단타 매매에 있어 volume이 크다는 건 좋은 것. buyer, seller가 많기 때문에 원하는 전략을 의도대로 실행 가능하기 때문임.

Open Interest : active이거나 , not settled contract의 수. Ready to be traded. NOT TRADED. 아직 청산/거래되지 않은 거래들의 수.
- Open Interest를 마켓 트렌드의 강함 정도로 판단 가능하다. Open Interest가 증가했다 --> 곧, market trend를 믿어도 된다. 사람이 많이 들어왔다. 라는 뜻으로 받아들일 수도 있다는 것.

**Base Asset, Quote Asset**
용어에 대한 정리 : https://www.binance.us/en/trading-rules
BTC/USDT 라는 fiat을 다룬다면 여기서 Base asset = BTC, Quote asset = USDT.
Base Asset은 order book(호가창) 상에서 실제로 trade되고 있는 asset을 말한다.


**HTTP와 Websocket의 차이점**
https://www.geeksforgeeks.org/what-is-web-socket-and-how-it-is-different-from-the-http/
HTTP는 unidirectinal, 한 번 데이터를 주고받으면 connection은 닫힌다.
Websocket은 bidirectional, connection이 끊어지는 기준에 도달하지 않으면 닫히지 않고 계속해서 정보를 주고받음, connection을 열 때 들이는 비용이 최초 한번만 들어감.
Data Stream은 그냥 실시간 처리, 실시간으로 데이터를 받아오는 데에 용이하기에 stream이라는 단어를 사용하는 듯.


# binance/um_futures/market.py
- ping(self):
 - Test connectivity to the REST API.
 - API : GET /fapi/v1/ping
 - 여기서는 query라는 메소드를 사용한다. binance/api.py에 자세한 내용 존재

- time(self):
 - Test connectivity + Server time
 - API : Get /fapi/v1/time

- exchange_info(self):
 - trading rules, symbol information
 - API : GET /fapi/v1/exchangeInfo

- depth(self, symbol:str, **kwargs)
 - Get Orderbook...?  : 호가창을 가져온다.
 - 구매자, 판매자의 수요 및 공급을 기록하는 데 사용하는 주문창.
 - 명령 실행해서 한번 확인해보기. --> bidPrice, bidSize가 'bids' 키에, askPrice, askSize가 'asks' 키에 있는 상태로 반환됨

- trades(self, symbol, **kwargs)
 - 현재 거래 현황 가져옴
 - price, qty : 가격과 거래량. quoteQty : 가격 * 거래량(거래된 금액 합)
 - isBuyerMaker : 바이어인가 아닌가. Maker인가 아닌가..? Maker는 뭐져
 - * maker : 시장가격에 물건을 내놓는 게 아니라 훨씬 싸게 사려는(bid) 또는 훨씬 비싸게 팔려는(ask) 사람들을 의미
 - 그래서 이게 maker랑 무슨 상관 --> Link : https://money.stackexchange.com/questions/90686/what-does-buyer-is-maker-mean
 - buyerMaker : buy side의 가격을 형성하고 있었다(buyer가 maker이다). 이 거래가 성사되었다는 얘기는 누군가가 coin을 SELL한 것 --> taker
 - isBuyerMaker = True : SELL contract인 거래라고 보면 됨 Buy거래 요청이 있었다가(Maker) Sell을 함으로써(Taker) 주문이 체결됨.

- agg_trades(self, symbol, **kwargs)
 - Compressed/Aggregate Trades List
 - Market trades that fill at the time, from the same order, with the same price will have the quantity aggregated.
 - GET /fapi/v1/aggTrades
 - 이거도 한번 명령을 해봐야 알겠습니다. 해보자
 - parameter에 대한 설명이 들어가 있음. startTime, endTime은 조금 중요할 듯? 나중에 백테스팅을 위해서
 - a : Aggregate tradeId
 - p : price, q : quantity, f : first tradeId, l : last tradeId, T : Timestamp, m : buyer로서의 maker이었는지 여부

- klines(self, symbol, interval, **kwargs)
 - kline, Candlestick 데이터
 - kline은 open time으로 구분된다..? 일단 건너뛰고

- continuous klines(self, pair, contractType, interval, **kwargs)
 - 이것과 그냥 kline의 차이? continuous kline은 <pair>_<contractType> 을 인자로 받고 kline은 symbol을 인자로 받고..?
 - 그냥 pair_contractType말고는 다른 점 없음. 결과값이 똑같다.

- index_price_klines(self, pair, interval, **kwargs)
 - index price of a pair.

- mark_price_klines(self, symbol, interval, **kwargs)
 - mark price of a symbol.

- mark_price(self, symbol)
 - 현재의 mark price...
 - mark price(시장평균가) : 강제청산가격의 기준이 되는 가격. 거래소 내 체결가격을 기준으로 하지 않는다.
 - 거래소 내 체결가격은 그냥 kline을 통해 얻을 수 있는 듯

- funding_rate(self, symbol, **kwargs)
 - funding rate의 변화 기록을 보여줌

- ticker_24hr_price_change(self, symbol)
 - symbol을 꼭 넣을 것을 주문하고 있음.
 - 24시간 기준 symbol이 어떻게 변화했는지 OHLC로 나타냄

- ticker_price(self, symbol)
 - 그냥 가장 최신 가격(현재 가격)

- book_ticker(self, symbol)
 - Best price/qty on the order book.
 - 현재 호가창에서 가장 BEST인 bid price, bid size, ask price, ask size.

- open_interest(self, symbol)
 - 현재의 open interest를 보여준다.

- open_interest_hist(self, symbol, period, **kwargs)
 - open interest의 history를 보여줌. **kwargs에 startTime, endTime을 넣어줄 수 있다.

- top_long_short_position_ratio(self, symbol: str, period: str, **kwargs)
 - Top 20%의 유저들에 대해, long position의 수 대비 short position의 수.

- top_long_short_account_ratio(self, symbol, period, **kwargs)
 - Top 20%의 유저들에 대해, long account의 수 대비 short account의 수. 여기서 account는 한 번만 포함된다.

 --> position ratio를 아는 것이 조금 더 시장에 대한 일반적인 정보가 아닐까 싶습니다.

- long_short_account_ratio(self, symbol, period, **kwargs)
 - 전체 유저의 account수. 이것 또한 시장에 대한 일반적 정보가 될 듯.

- taker_long_short_ratio(self, symbol, period, **kwargs)
 - taker의 buy volume과 sell volume을 가져온다.

- index_info(self, symbol)
 - 여러 개 symbol을 조합하여 전체 시장 상태를 나타낼 수 있도록 한 것인듯?

- asset_Index(self, symbol)
 - 멀티에셋 모드에서 asset index를 가져온다...? 필요 없는듯.


# binance/api.py
- init : key, secret, base_url, timeout, proxies .. 
- requests의 Session이라는 클래스로, 세션 관리
- query(url_path, payload=None)
 - self.send_request를 호출함
 - send_request(http_method, url_path, payload, special)
 - query라는 메소드는 결국 send_request 메소드를 GET 방식으로 호출한다는 것과 동일


# binance/um_futures/portfolio_margin.py
- pm_exchange_info(self, symbol: str = None):
    """
    |
    | **Portfolio Margin Exchange Information**
    | *Current Portfolio Margin exchange trading rules.*
    :API endpoint: ``GET /fapi/v1/pmExchangeInfo``
    :API doc: https://binance-docs.github.io/apidocs/futures/en/#portfolio-margin-endpoints
    :parameter symbol: string; the trading pair.
    |
    """

    params = {"symbol": symbol}
    return self.query("/fapi/v1/pmExchangeInfo", params)


