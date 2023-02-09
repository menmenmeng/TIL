import numpy as np
import pandas as pd
import logging
from binance.error import ClientError

class Decision():
    '''
    openLong, openShort, closeLong, closeShort를 반환하는 class
    '''
    def __init__(self, UMclient, positionAmt=0, entryPrice=0):
        self.client = UMclient
        self.is_upperInterUpBt = None
        self.is_upperBandDwBt = None
        self.is_aboveFrv = None
        self.is_belowFrv = None
        
        # AccountUpdate 및 초기에 전달받아야 함. 초기 전달은 일단 처음에는 안 받을 예정, 0.
        self.positionAmt = positionAmt
        self.entryPrice = entryPrice

        self.tradeAmt = 0.05
        # self.tradePrice = 0

        self.ableTradeFlag = False # trade를 할 조건이 갖추어졌는가?
        self.nearLastTrade = False # 이전의 trade에서부터 꽤 멀어졌는가. 
    

    def trade(self, currentPrice, **kwargs):
        is_upperInterUpBt = kwargs['is_upperInterUpBt']
        is_upperBandDwBt = kwargs['is_upperBandDwBt']
        is_aboveFrv = kwargs['is_aboveFrv']
        is_belowFrv = kwargs['is_belowFrv']
        
        is_long = self.positionAmt > 0
        is_np = self.positionAmt == 0
        self.update_trade_flag(is_aboveFrv, is_belowFrv)

        # Trade한 지 시간이 좀 지났다면(is_belowFrv형태가 되었다면)
        if not self.nearLastTrade:
            # 1. No position
            if is_np:

                if is_upperInterUpBt and is_aboveFrv:
                    self.trade_limit("BUY", price=round(self.entryPrice*1.001, 1), amount=self.tradeAmt)
                
                else:
                    pass

            # 2. Long position
            elif is_long: # positionAmt 가 있다는 얘기는 곧, entryPrice도 존재한다는 얘기.

                if is_upperBandDwBt:
                    self.trade_limit("SELL", price=round(self.entryPrice*0.999, 1), amount=self.tradeAmt)
                
                elif (currentPrice < self.entryPrice*0.97) or (currentPrice > self.entryPrice*1.04):
                    self.trade_limit("SELL", price=round(self.entryPrice*0.999, 1), amount=self.tradeAmt)


    def trade_limit(self, side, price, amount):
        try:
            response = self.client.new_order(
                symbol="BTCUSDT",
                side=side,
                type="LIMIT",
                quantity=amount,
                timeInForce="GTC",
                price=price,
            )
            logging.info(response)
            self.nearLastTrade = True

        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    
    def update_trade_flag(self, is_aboveFrv, is_belowFrv):
        # Frv보다 rv가 내려가면, nearLastTrade는 False가 됨. 그럼 다시 Trade를 할 수 있는 조건을 찾아볼 수 있게 된다!
        # 그 전에는 무슨 수를 쓰더라도 Trade는 불가함.
        if is_belowFrv:
            self.nearLastTrade = False

