import numpy as np
import pandas as pd
import logging
import time
from cert.myfuncs import *
from binance.error import ClientError

class Decision():
    '''
    openLong, openShort, closeLong, closeShort를 반환하는 class
    '''
    def __init__(self, UMclient, positionAmt=0, entryPrice=0):
        self.tradeClient = UMclient
        self.tradeAmt = 0.01
        # self.tradePrice = 0

        # custom conditions
        self.bbCondition = None
        self.rvCondition = None

        # current position state
        self.is_long = None
        self.is_short = None
        self.is_np = None
        
        # AccountUpdate 및 초기에 전달받아야 함. 초기 전달은 일단 처음에는 안 받을 예정, 0.
        self.positionAmt = positionAmt
        self.entryPrice = entryPrice

        # trade flags
        self.tradeFlag = True
        self.tradeTime = None
    

    def update_trade_flag(self):
        '''
        self.tradeFlag를 True로 만드는 조건에 따라, self.tradeFlag를 True로 만듦.

        1. RV가 너무 크거나 너무 낮다면, True로 만들지 않는다. (우선)

        2. trade한 지 5분이 지났다면, 다시 True로 만든다.
        '''
        timeNow = time.time()*1000
        rvs = self.rvCondition
        currentRV = float(rvs[-1:])
        maxRV = float(max(rvs[-20:]))
        minRV = float(min(rvs[-20:]))

        # 1.
        if (currentRV > maxRV) or (currentRV < minRV) :
            self.tradeFlag = False

        # 2.
        elif (timeNow - self.tradeTime) > 300_000 :
            self.tradeFlag = True
        
        print(f"currentRV:{currentRV}, maxRV:{maxRV}, minRV:{minRV}, timeNow:{ms2dt(timeNow)}")
        print(f"tradeFlag : {self.tradeFlag}")


    def trade(self, currentPrice, **conditions):

        ## bb Condition
        self.bbCondition = conditions['bbCondition']
        PASTcloses_gt_upperInter_5t = self.bbCondition[0]
        PASTcloses_gt_upperBand_5t = self.bbCondition[1]
        PASTcloses_lt_lowerInter_5t = self.bbCondition[2]
        PASTcloses_lt_lowerBand_5t = self.bbCondition[3]
        CURRclose_gt_upperInter = self.bbCondition[4]
        CURRclose_gt_upperBand = self.bbCondition[5]
        CURRclose_lt_lowerInter = self.bbCondition[6]
        CURRclose_lt_lowerBand = self.bbCondition[7]           

        ## rv Condition
        self.rvCondition = conditions['rvCondition']
        rvs = self.rvCondition
        
        ## position state
        self.is_long = self.positionAmt > 0
        self.is_np = self.positionAmt == 0

        self.update_trade_flag()
        if not self.tradeFlag:
            return


        '''
        Buy/Sell condition check and execute trade methods.
        '''
        if self.is_np:

            '''
            1. take Long Position
                - 2분전, 1분전 close가 upperInter보다 낮은데, 현재 close는 upperInter보다 높아야 함
            
            2. take Short Position
                - 2분전, 1분전 close가 lowerInter보다 높은데, 현재 close는 lowerInter보다 낮아야 함
            '''
            # 1.
            if (np.all(PASTcloses_gt_upperInter_5t[-2:] == False)) and CURRclose_gt_upperInter:
                # get long position. (buy)
                pass

            # 2.
            if (np.all(PASTcloses_lt_lowerInter_5t[-2:] == False)) and CURRclose_lt_lowerInter:
                # get short position. (sell)
                pass



        elif self.is_long:
            '''
            1. stop Loss
                - currentPrice가 entryPrice * 0.97 이하가 되었을 때

            2. take Profit
                - currentPrice가 entryPrice * 1.05 이상이 되었을 때

            3. 기타 custom 조건
                - 1분전 close가 upperBand보다 높은데, 현재 close는 upperBand보다 낮아야 함
            '''
            # 1.
            if currentPrice <= self.entryPrice*0.97:
                # stop Loss (clear long position, sell)
                pass

            elif currentPrice >= self.entryPrice*1.05:
                # take Profit (clear long position. sell)
                pass

            elif bool(PASTcloses_gt_upperBand_5t[-1:]) and bool(CURRclose_gt_upperBand == False):
                # take Profit (clear long position. sell)
                pass



        elif self.is_short:
            '''
            1. stop Loss
                - currentPrice가 entryPrice * 1.03 이상이 되었을 때

            2. take Profit
                - currentPrice가 entryPrice * 0.95 이하가 되었을 때

            3. 기타 custom 조건
                - 1분전 close가 lowerBand보다 낮은데, 현재 close는 lowerBand보다 높아야 함
            '''
            # 1.
            if currentPrice >= self.entryPrice*1.03:
                # stop Loss (clear short position, buy)
                pass

            elif currentPrice <= self.entryPrice*0.95:
                # take Profit (clear short position, buy)
                pass

            elif bool(PASTcloses_lt_lowerBand_5t[-1:]) and bool(CURRclose_lt_lowerBand == False):
                # take Profit (clear short position, buy)
                pass



        # Trade한 지 시간이 좀 지났다면(is_belowFrv형태가 되었다면)
        if not self.nearLastTrade:
            # 1. No position
            if is_np:
                ## for debug
                print("is_np:", is_np)
                ##

                if is_upperInterUpBt and is_aboveFrv:
                    ## for debug
                    print("is_upperInterUpBt:", is_upperInterUpBt)
                    ##
                    self.trade_limit("BUY", price=round(self.entryPrice*1.001, 1), amount=self.tradeAmt)

            # 2. Long position
            elif is_long: # positionAmt 가 있다는 얘기는 곧, entryPrice도 존재한다는 얘기.
                ## for debug
                print("is_long:", is_long)
                ##

                if is_upperBandDwBt:
                    ## for debug
                    print("is_upperBandDwBt:", is_upperBandDwBt)
                    ##
                    self.trade_limit("SELL", price=round(self.entryPrice*0.999, 1), amount=self.tradeAmt)
                
                elif (currentPrice < self.entryPrice*0.97) or (currentPrice > self.entryPrice*1.04):

                    ## for debug
                    if (currentPrice < self.entryPrice*0.97) : print("stopLoss")
                    else: print("takeProfit")
                    ##

                    self.trade_limit("SELL", price=round(self.entryPrice*0.999, 1), amount=self.tradeAmt)


    def trade_limit(self, side, price, amount):

        ## for debug
        print("trade method triggered.")
        ##

        try:
            response = self.tradeClient.new_order(
                symbol="BTCUSDT",
                side=side,
                type="LIMIT",
                quantity=amount,
                timeInForce="GTC",
                price=price,
            )
            logging.info(response)
            self.tradeFlag = False

            ## for debug
            print("tried trade method")
            ##

        except ClientError as error:
            logging.error(
                "Found error. status: {}, error code: {}, error message: {}".format(
                    error.status_code, error.error_code, error.error_message
                )
            )

    
