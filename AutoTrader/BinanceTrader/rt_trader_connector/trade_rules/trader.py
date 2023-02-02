import numpy as np
import pandas as pd
import time
import logging
from binance.lib.utils import config_logging
from binance.error import ClientError

from cert.myfuncs import *
from trade_rules.data_processor import DataCollector

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Trader(DataCollector):
    def __init__(self, UMclient, current_asset, listenKey, **streams): # some data is needed.
        super().__init__(current_asset, listenKey, **streams)

        self.client = UMclient

        self.callback_num = 0
        self.now = time.time()
        self.ma1_downup_ma2 = [0]
        self.ma1_updown_ma2 = [0]
        self.flag_ma1_ma2 = None
        
        self.buy_condition1 = False
        self.sell_condition1 = False

        self.buy_decision = False
        self.sell_decision = False

        self.current_price = None


        # 사용되고 나면 다시 initiated 되어야 함.
        self.standard_trade_quantity = 0.1
        self.quantity = self.standard_trade_quantity

    # 1. 그래프 그리는 메소드들
    def draw_graph_RV(self):
        pass


    # 2. 기본 메소드들
    def volatility(self, window):
        dt_markPrice = self.df_store['markPriceUpdate'] ###
        sr_markPrice = dt_markPrice['p'].astype(float)
        sr_markPrice_rv = log_return(sr_markPrice).rolling(window=window).apply(realized_volatility)

        return sr_markPrice_rv


    def ma(self, window):
        dt_markPrice = self.df_store['markPriceUpdate'] ###
        sr_markPrice = dt_markPrice['p'].astype(float)
        sr_markPrice_ma = sr_markPrice.rolling(window=window).mean()

        return sr_markPrice_ma


    # # 3. 구매조건 체크하는 메소드들
    def _draw_graph_MAs(self, ma1, ma2):
        try:
            plt.clf()
        except:
            pass
        plt.figure(figsize=(14, 3))
        # plt.subplot(2, 1, 1)
        # plt.plot(np.arange(999), markPrice, c='r')
        plt.plot(ma1, c='b')
        plt.plot(ma2, c='y')
        plt.show()


    def _get_2_MAs(self, window1, window2):
        ma1 = self.ma(window1)
        ma2 = self.ma(window2)
        return ma1, ma2


    def _update_compare_mas(self, ma1, ma2):
        if list(ma1)[-1] > list(ma2)[-1]:
            flag = True
        else:
            flag = False
        self.flag_ma1_ma2 = flag
        return flag


    def _update_ma_bt_index(self, ma1, ma2):
        former_flag = self.flag_ma1_ma2
        current_flag = self._update_compare_mas(ma1, ma2) # 이걸 쓰면서 바로 갱신됨.

        if former_flag!=current_flag: # 만약 달라졌다면.
            if former_flag:
                self.ma1_updown_ma2.append(self.now)
                if len(self.ma1_updown_ma2)>=3:
                    self.ma1_updown_ma2.pop(0)

            else:
                self.ma1_downup_ma2.append(self.now)
                if len(self.ma1_downup_ma2)>=3:
                    self.ma1_downup_ma2.pop(0)


    def _update_ma_buysell_condition(self):
        if len(self.ma1_updown_ma2)==2:
            first, second = self.ma1_updown_ma2[0], self.ma1_updown_ma2[1]
            if second-first<50:
                self.sell_condition1 = True
            else:
                self.sell_condition1 = False

        elif len(self.ma1_downup_ma2)==2:
            first, second = self.ma1_downup_ma2[0], self.ma1_downup_ma2[1]
            if second-first<50:
                self.buy_condition1 = True
            else:
                self.buy_condition1 = False


    def _update_buysell_decision(self):
        if self.current_amt==0:
            if self.buy_condition1:
                self.buy_decision = True
            elif self.sell_condition1:
                self.sell_decision = True
        
        elif self.current_amt>0: # Long position
            if self.buy_condition1:
                if self.current_price>self.entry_price:
                    self.buy_decision = True
                    self.quantity = self.quantity/2
                else:
                    self.buy_decision = False
            
            elif self.sell_condition1:
                self.sell_decision = True
                self.quantity = self.current_amt
            
        elif self.current_amt<0:
            if self.sell_condition1:
                if self.current_price<self.entry_price:
                    self.sell_decision = True
                    self.quantity = self.quantity/5
                else:
                    self.sell_decision = False

            elif self.buy_condition1:
                self.buy_decision = True
                self.quantity = -self.current_amt


    def _placing_order_test(self):
        # buy decision
        if self.buy_decision==True:

            config_logging(logging, logging.DEBUG)
            buy_price = round(0.999 * float(self.current_price), 1)
            print("BUY  : ", buy_price, self.quantity)
            try:
                response = self.client.new_order_test(
                    symbol="BTCUSDT",
                    side="BUY",
                    type="LIMIT",
                    quantity=self.quantity,
                    timeInForce="GTC",
                    price=buy_price,
                )
                logging.info(response)
                self.buy_decision = False
                self.quantity = self.standard_trade_quantity
            except ClientError as error:
                print('buy error')
                print(error)
                # logging.error(
                #     "Found error. status: {}, error code: {}, error message: {}".format(
                #         error.status_code, error.error_code, error.error_message
                #     )
                # )

        # sell decision
        elif self.sell_decision==True:

            config_logging(logging, logging.DEBUG)
            sell_price = round(1.001 * float(self.current_price), 1)
            print("SELL : ", sell_price, self.quantity)
            try:
                response = self.client.new_order_test(
                    symbol="BTCUSDT",
                    side="SELL",
                    type="LIMIT",
                    quantity=self.quantity,
                    timeInForce="GTC",
                    price=sell_price,
                )
                logging.info(response)
                self.sell_decision = False
                self.quantity = self.standard_trade_quantity
            except ClientError as error:
                print('sell error')
                print(error)
                # logging.error(
                #     "Found error. status: {}, error code: {}, error message: {}".format(
                #         error.status_code, error.error_code, error.error_message
                #     )
                # )


    # 4. 실시간 콜백 함수
    def my_callback(self, message):
        
        self.callback_num += 1

        self.data_stream_proc(message) # update dfs.
        try:
            self.current_price = float(list(self.df_store['markPriceUpdate']['p'])[-1])
        except Exception as e:
            print("current price error")
            print(e)

        try:
            ma1, ma2 = self._get_2_MAs(12, 26)
        except Exception as e:
            print('ma calculating error')
            print(e)

        try:
            self._update_ma_bt_index(ma1, ma2)
        except Exception as e:
            print('update ma bt index error')
            print(e)

        try:
            self._update_ma_buysell_condition()
        except Exception as e:
            print('update ma buysell condition error')
            print(e)

        try:
            self._update_buysell_decision()
        except Exception as e:
            print('update buysell decision error')
            print(e)
        
        try:
            self._placing_order_test()
        except Exception as e:
            print('placing order test error')
            print(e)

        
        if self.callback_num%100==0:
            print('callback_num : ', self.callback_num)
        return