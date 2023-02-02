import numpy as np
import pandas as pd
import time
from binance.error import ClientError
from cert.myfuncs import *

class Callback():
    '''
    * message 종류
    1. markPriceUpdate
    2. user data
    '''
    def __init__(self, UMclient, current_asset, current_amt=0, **streams):
        # for trade method.
        self.client = UMclient
        self.current_price = None # 현재의 price, markPrice_row_df 함수에서 업데이트함.

        # 나의 현재 상태 : 이거 밖에서 restAPI를 통해 미리 가져온다.
        self.INITIAL_ASSET = current_asset # 초기자금은 얼마였는지?
        self.current_asset = current_asset

        # 현재 position과 관련 있음, trade와 관련 있음.
        self.current_amt = current_amt # 지금 내가 가지고 있는 position의 amount, 아마 0일 것.
        self.entry_price = 0
        self.standard_quantity = 0.1 # 기본적으로 얼마나 매수/매도할 것인가? test가 아니라 실제로 들어갈 시에는 0.1로 하면 죽는다.
        self.additional_trade = 0 # 추매를 몇 번 했는가? 추가매매할 때마다 +1 되고, 청산 시 0이 된다.


        # message의 Type이 userData라면, stream Name이 listenKey로 나오기 때문에 listenKey를 알아야 함.
        # 마찬가지로, stream Name을 알기 위해 streams도 받음.
        # streams의 형식 : dict(listenKey = <listenKey>, aggTrade='btcusdt@aggTrade', markPrice='btcusdt@markPrice', ...)
        self.stream = list(streams.keys())
        self.streamName = list(streams.values())
        # self.listenKey, self.stream_aggTrade, self.stream_markPrice로 message의 Type을 구분하기.

        # 활용할 dataframe들.
        self.markPrice_df = pd.DataFrame()

        # ma 변수 : 실시간 그래프 그리기 위해 따로 지정해 놓음
        self.ma1 = None
        self.ma2 = None

        # ma와 관련된 buysell condition
        self.ma1_greater_ma2 = None
        self.bt_down = []
        self.bt_up = []
        ##
        self.buy_condition1 = False
        self.sell_condition1 = False


        # rv와 관련된 buysell condition(미구현)
        self.rv = None
        self.rv_ma = None
        self.trade_condition2 = False

        # decision vars.
        self.buy_decision = False
        self.sell_decision = False

        # 디버깅용.
        self.callback_num = 0 # 전체적으로 message를 몇 개나 받았는지 표시
        self.markPrice_callback_num = 0 # markPrice message를 몇 개나 받았는지 표시
        self.virtual_amt = 0 # trade test 하지 말고, 일단 decision flag가 어떻게 움직이는지만 확인하려고 virtual_amt를 설정했음.
        self.trade_num = 0


    # messageType 저장하는 함수
    def get_messageType(self, message):
        # multiple stream 가정
        try:
            index = self.streamName.index(message['stream'])
            messageType = self.stream[index]
        except:
            print("message : \n", message)
            messageType = None
        return messageType

    def account_info(self):
        print(f"callback {self.markPrice_callback_num}:", round(self.INITIAL_ASSET, 4), round(self.current_asset, 4), self.current_amt, round(self.entry_price, 4))

            

    def callback(self, message):
        self.callback_num += 1
        # print(f"** Callback {self.callback_num} Executed. **")
        # markPrice callback
        ## markPrice callback이 들어왔을 때, trade callback도 실행(매매할지 말지)

        messageType = self.get_messageType(message)
        # 2개의 stream(listenKey, markPrice) 만 들어온다고 가정.

        # message가 markPrice인 경우
        if messageType == 'markPrice':
            self.markPrice_callback_num += 1
            # print(f"*** markPrice Callback {self.markPrice_callback_num} Executed. ***")
            # markPrice df를 업데이트(데이터 정리) 하는 콜백 수행
            self.markPrice_data_callback(message) # markPrice df가 업데이트됨., 매번 들어올 때마다 current price를 가져오게끔 하자.

            self.callback_condition1() # buy/sell condition1이 업데이트됨
            self.callback_condition2() # trade condition2 이 업데이트됨
            self.callback_decision() # decision 이 업데이트됨.

            # 실시간 그래프 그리는 callback
            # self.graph_callback()

            # 디버깅을 위해.
            # print("## DEBUG : buy/sell condition1:", self.buy_condition1, self.sell_condition1)
            # print("## DEBUG : trade condition2:", self.trade_condition2)
            # print("## DEBUG : buy/sell decision:", self.buy_decision, self.sell_decision)

            # trade하는 callback 수행
            self.trade_callback()
            self.account_info()
            # print("## DEBUG :")
            # print("--- RESULT ---")
            # print("--- Initial Asset  :", self.INITIAL_ASSET)
            # print("--- Current Asset  :", self.current_asset)
            # print("--- Current Amount :", self.current_amt)
            # print("--- Entry Price    :", self.entry_price)
            # print("--- Trade Number   :", self.trade_num)
            


        # message가 User-Data인 경우
        elif messageType == 'listenKey':
            self.userData_callback(message)
        
        else:
            print("loading...")

        # print("** Callback End. **")
        # print()






    # markPrice 관련 callback
    ## markPrice 전체 프로세스
    def markPrice_data_callback(self, message):
        row_df = self._markPrice_row_df(message)
        self.markPrice_df = pd.concat([self.markPrice_df, row_df], axis=0)
        self.markPrice_df.reset_index(drop=True, inplace=True)

    # markPrice 한 번 왔을 때, row를 하나 만들어주는 작업
    def _markPrice_row_df(self, message):
        data = message['data']

        eventType = data['e']
        eventTime = data['E']
        markPrice = float(data['p'])
        self.current_price = markPrice
        indexPrice = float(data['i'])

        row_dict = dict(
            eventType = eventType,
            eventTime = eventTime,
            markPrice = markPrice,
            indexPrice = indexPrice,
        )

        row_df = pd.DataFrame(row_dict, index=[0])
        # print("## DEBUG : markPrice 1 received row")
        # print(row_df)
        return row_df




    # ma 관련 condition을 갱신

    # markPrice가 올 때마다 ma를 갱신하는 프로세스
    ## markPrice message가 올 때마다, 이걸 수행해야 함.
    def calculate_ma(self, window):
        try:
            ma = self.markPrice_df['markPrice'].rolling(window).mean()
        except Exception as e:
            print(f"## ERROR : ma with window {window} wasn't created.") # 만약 window가 전체 row 길이보다 크다면 어떻게 create되는가?
            ma = None
        return ma

    ## markPrice마다.
    def calculate_two_ma(self, window1, window2):
        ma1 = self.calculate_ma(window1)
        ma2 = self.calculate_ma(window2)
        self.ma1, self.ma2 = ma1, ma2
        return ma1, ma2

    # ma condition을 업데이트하는 callback
    def update_ma_condition(self, ma1, ma2):
        ma1_last = list(ma1)[-1]
        ma2_last = list(ma2)[-1]
        if (not np.isnan(ma1_last)) and (not np.isnan(ma2_last)):
            ma1_greater_ma2 = (ma1_last > ma2_last)   # NaN과의 비교는 어떻게 되는가?
            # print("## DEBUG : ma1_last, ma2_last : ", ma1_last, ma2_last)
        else:
            # print("## ERROR : update_ma_condition is not triggered.")
            ma1_greater_ma2 = None
        
        self.ma1_greater_ma2 = ma1_greater_ma2  # instance var update.
        return ma1_greater_ma2

    # update_bt_append 이후에 무조건 update_bt_remove가 와야 한다.
    # update_bt condition은 함께 묶여야 함.
    def update_bt_append_condition(self, ma1, ma2):
        former_ma1_greater_ma2 = self.ma1_greater_ma2
        current_ma1_greater_ma2 = self.update_ma_condition(ma1, ma2)
        
        # None과 관련된 부등식, 더 줄일 방법 없을지 찾아보기.
        # 둘 다 None이 아니라는 가정 하에.
        if (former_ma1_greater_ma2!=None) and (current_ma1_greater_ma2!=None):

            # 두 개가 다르고, ma1이 ma2를 아래로 돌파
            if former_ma1_greater_ma2!=current_ma1_greater_ma2:
                if former_ma1_greater_ma2:
                    self.bt_down.append(time.time())
                else:
                    self.bt_up.append(time.time())

    def update_bt_remove_condition(self, remove_threshold):
        # remove_threshold : 몇 초 동안 breakthrough 기록을 남겨놓을지. 디폴트는 50
        bt_down = [bt_rec for bt_rec in self.bt_down if bt_rec>(time.time()-remove_threshold)]
        bt_up = [bt_rec for bt_rec in self.bt_up if bt_rec>(time.time()-remove_threshold)]
        self.bt_down = bt_down
        self.bt_up = bt_up

    def update_bt_condition(self, ma1, ma2, remove_threshold=50):
        self.update_bt_append_condition(ma1, ma2)
        self.update_bt_remove_condition(remove_threshold)

    # ma와 관련된 buysell condition을 체크하는 함수.
    # 만약 buy/sell signal이 있다면, instance var의 buysell condition을 갱신한다.
    # bt_up 또는 bt_down을 전부 없애고 빈 리스트로 만드는 작업을 담은 function이 필요함. 향후에 만들어주기로.
    def check_buysell_condition1(self):
        if len(self.bt_up)>=2:
            self.buy_condition1 = True
        else: # buy하고 나면, self.bt_up이 빈 리스트가 되는 작업이 필요함 (아직 완료 안함, 완료하면 여기에 함수이름 쓰기로 -- trade 함수에 같이 써 주었음.)
            self.buy_condition1 = False

        if len(self.bt_down)>=2:
            self.sell_condition1 = True
        else: # sell하고 나면, self.bt_down이 빈 리스트가 되는 작업이 필요함
            self.sell_condition1 = False

    # markPrice가 들어왔을 때, ma를 활용해서 bt condition을 갱신하는 callback.
    def callback_condition1(self):
        ma1, ma2 = self.calculate_two_ma(12, 26)
        self.update_bt_condition(ma1, ma2, 50)
        self.check_buysell_condition1()



    # rv condition과 함께, rv 관련 condition2를 갱신하는 callback 추가.
    def calculate_rv(self, window):
        try:
            rv = log_return(self.markPrice_df['markPrice']).rolling(window).apply(realized_volatility)
        except Exception as e:
            # print(f"## ERROR : rv with window {window} wasn't created.") # 만약 window가 전체 row 길이보다 크다면 어떻게 create되는가? -- 그냥 NaN의 리스트로 리턴됨. 오류안남
            rv = None
        return rv

    def calculate_rv_ma(self, window, rv):
        try:
            rv_ma = rv.rolling(window).mean()
        except:
            # print(f"## ERROR : rv_ma with window {window} wasn't created.")
            rv_ma = None
        return rv_ma

    def update_rv_condition(self, window_rv, window_rvma):
        self.rv = self.calculate_rv(window_rv)
        self.rv_ma = self.calculate_rv_ma(window_rvma, self.rv)

    def check_buysell_condition2(self):
        rv_last = list(self.rv)[-1]
        rv_ma_last = list(self.rv_ma)[-1]

        if (not np.isnan(rv_last)) and (not np.isnan(rv_ma_last)):
            # print("## DEBUG : rv_last, rvma_last : ", rv_last, rv_ma_last)
            if rv_last > rv_ma_last:
                self.trade_condition2 = True
            else:
                self.trade_condition2 = False
        else:
            # print("## ERROR : update_rv_condition is not triggered.")
            self.trade_condition2 = False


    def callback_condition2(self):
        self.update_rv_condition(12, 26)
        self.check_buysell_condition2()



    def callback_decision(self):
        if self.buy_condition1 and self.trade_condition2:
            self.buy_decision = True
        else:
            self.buy_decision = False

        if self.sell_condition1 and self.trade_condition2:
            self.sell_decision = True
        else:
            self.sell_decision = False


    # def callback_decision(self):
    #     if self.buy_condition1:
    #         self.buy_decision = True
    #     else :
    #         self.buy_decision = False

    #     if self.sell_condition1:
    #         self.sell_decision = True
    #     else:
    #         self.sell_decision = False






    # trade callback.
    def trade_callback(self):
        if self.buy_decision:

            if self.current_amt == 0: # no position
                quantity = self.standard_quantity
                self.trade(is_buy=True, quantity=quantity)

            elif self.current_amt > 0: # Long position. 추가매수
                quantity = self.current_amt*(1/2)**(self.additional_trade+1)
                self.trade(is_buy=True, quantity=quantity)
                self.additional_trade += 1

            elif self.current_amt < 0: # Short position. 청산하고 다시
                quantity = -self.current_amt + self.standard_quantity
                self.trade(is_buy=True, quantity=quantity)
                self.additional_trade = 0

            # self.bt_up = []

        if self.sell_decision:

            if self.current_amt == 0:
                quantity = self.standard_quantity
                self.trade(is_buy=False, quantity=quantity)

            elif self.current_amt > 0: # Long position. 청산하고 다시
                quantity = self.current_amt + self.standard_quantity
                self.trade(is_buy=False, quantity=quantity)
                self.additional_trade = 0

            elif self.current_amt < 0: # Short position. 추가매도
                quantity = (-self.current_amt)*(1/2)**(self.additional_trade+1)
                self.trade(is_buy=False, quantity=quantity)
                self.additional_trade += 1

            # self.bt_down = []


    def trade(self, is_buy, quantity):
        client = self.client

        if is_buy:
            price = round(self.current_price * 1.001, 1)
            side = "BUY"
        else:
            price = round(self.current_price * 0.999, 1)
            side = "SELL"

        try:
            # print("## DEBUG : Trying TRADE")
            # print("SIDE:", side)
            # print("PRICE:", price)
            # if is_buy:
                
            # 실제로 Trade를 하고 싶다면, 아래의 코드를 주석해제.
            # test든 아니든, 그냥 new_order 쓰면 됨...
            response = client.new_order(
                symbol="BTCUSDT",
                side=side,
                type="LIMIT",
                quantity=quantity,
                timeInForce="GTC",
                price=price
            )
            print(response)
            print("## DEBUG : Trade Price :", price)
            self.trade_num += 1
            print("## DEBUG : Trade number :", self.trade_num)

            if is_buy:
                self.bt_up = []
            else:
                self.bt_down = []

        except ClientError as error:
            print(
                "## ERROR : Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )





    



    # userData 관련 callback
    def userData_callback(self, message):
        data = message['data']
        eventType = data['e']

        if eventType == "ACCOUNT_UPDATE":
            self.check_account_update(message)
            print("USER_ISSUE : ACCOUNT_UPDATE")
            print(data)
        
        elif eventType == "ORDER_TRADE_UPDATE":
            print("USER ISSUE : ORDER_TRADE_UPDATE")
            print(data)

    def check_account_update(self, message):
        for data in message['data']['a']['B']:
            if data['a']=='USDT':
                balance_USDT = data
            elif data['a']=='BUSD':
                balance_BUSD = data
        
        for data in message['data']['a']['P']:
            if data['s']=='BTCUSDT' and data['ps']=='BOTH':
                position_BOTH = data
            elif data['s']=='BTCUSDT' and data['ps']=='LONG':
                position_LONG = data
            elif data['s']=='BTCUSDT' and data['ps']=='SHORT':
                position_SHORT = data
        
        self.current_amt = float(position_BOTH['pa'])
        self.entry_price = float(position_BOTH['ep'])
        self.current_asset = float(balance_USDT['wb'])
        
        return balance_USDT, position_BOTH

        # for One-way mode.
        # profit = self.current_asset - balance_USDT['wb']
        # profit_ratio = profit/balance_USDT['wb']
        # profit_wo_extraFee = balance_USDT['bc']

        # self.current_asset = balance_USDT['wb']
        # return profit, profit_ratio, profit_wo_extraFee