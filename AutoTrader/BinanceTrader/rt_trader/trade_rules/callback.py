import time
import numpy as np
import pandas as pd

from trade_rules.prelim import *
from trade_rules.collector import *
from trade_rules.conditional import *
from trade_rules.decision import * # Trader

class Callback(Collector):
    def __init__(self, UMclient, walletBalance, currentAsset, positionAmt, entryPrice, lastKlines, **streamDict):
        super().__init__(**streamDict)
        # streamDict, streamDict_inverse를 Collector에게서 상속해옴.
        self.klineCollector = KlineCollector(lastKlines, **streamDict)
        self.rtKlineCollector = RealTimeKlineCollector(**streamDict)
        self.markPriceCollector = MarkPriceCollector(**streamDict)
        self.orderUpdateCollector = OrderUpdateCollector(**streamDict)
        self.accountUpdateCollector = AccountUpdateCollector(currentAsset, **streamDict)

        self.bbConditonal = BBConditional()
        self.rvConditional = RVConditional()

        self.decider = Decision(UMclient, positionAmt=positionAmt, entryPrice=entryPrice)


        self.callbackNum = 0

        # current Account information
        self.currentAmt = 0
        self.currentAsset = currentAsset
        self.entryPrice = 0
        self.balanceChange = 0

    def callback(self, message):
        '''
        1. message가 어떤 stream 및, 어떤 eventType의 message인지 판별
        2. 그 stream/eventType의 callback을 실행
            2.1. markPrice일 경우
                markPrice collector를 업데이트
                trade 조건을 판별
                조건이 참일 경우 trade를 실행
            2.2. userData일 경우
                2.2.1. orderUpdate일 경우
                    orderUpdate collector를 업데이트
                2.2.2. accountUpdate일 경우
                    accountUpdate collector를 업데이트
                    최종 asset 출력
                    ** 전체 asset 변화 + commission 제외한 asset 변화 둘 다 출력하기.
        '''
        self.callbackNum += 1
        print(f"******* Callback {self.callbackNum} *******")
        print()

        streamKey, eventType = self.getEventType(message) # 상속받은 메소드
        
        if streamKey == None:
            return

        if streamKey.startswith("markPrice"):
            markPrice = self.markPriceCollector.getDataFrame(message)

        elif streamKey.startswith("kline"):
            ohlcv = self.klineCollector.getDataFrame(message)
            rt_ohlcv = self.rtKlineCollector.getDataFrame(message)
            rt_close = float(rt_ohlcv['close'][-1:])
            bbCondition = self.bbConditonal.callback(ohlcv, rt_ohlcv, 20)
            rvCondition = self.rvConditional.callback(ohlcv, 10)

            self.decider.trade(
                currentPrice = rt_close,
                bbCondition = bbCondition,
                rvCondition = rvCondition,
            )

            # trade_flag를 반환하는 방법이 필요함, self.decider.trade()에 이런 기능을 넣어도 되고. 여기다가 추가해도 되고..
            # trade_flag를 내렸다가, 다시 올리려면? 어떻게 해야 하는가? trade_flag를 변경하는 방법에 대해서도 생각해보기.


        elif streamKey == "userData":
            if eventType == "ORDER_TRADE_UPDATE":
                print("eventType : ORDER_TRADE_UPDATE")
                self.orderUpdateCollector.getDataFrame(message)
                print(self.orderUpdateCollector.realizedProfit)
                with open("orderTradeUpdate.txt", "a") as f:
                    f.write(message)
                    f.write("\n")

            elif eventType == "ACCOUNT_UPDATE":
                print("eventType : ACCOUNT_UPDATE")
                self.accountUpdateCollector.getDataFrame(message)
                accountInfo = [
                    self.accountUpdateCollector.currentAmt,
                    self.accountUpdateCollector.currentAsset,
                    self.accountUpdateCollector.entryPrice,
                    self.accountUpdateCollector.balanceChange,
                ]
                print("## Account Updated.")
                self.currentAmt = accountInfo[0]
                self.currentAsset = accountInfo[1]
                self.entryPrice = accountInfo[2]
                self.balanceChange += accountInfo[3]
                
                self.decider.positionAmt = accountInfo[0]
                self.decider.entryPrice = accountInfo[2]
                self.decider.tradeTime = self.accountUpdateCollector.eventTime
                with open("accountUpdate.txt", "a") as f:
                    f.write(message)
                    f.write("\n")

        print()
        print("## Overall Evaluation.")
        print(f"- Asset : {self.currentAsset}, currentAmt : {self.currentAmt}, entryPrice : {self.entryPrice}, balanceChange(except Commission) : {self.balanceChange}")
        print()
        print(f"******* Callback {self.callbackNum} Ends. *******")
        print("\n\n")