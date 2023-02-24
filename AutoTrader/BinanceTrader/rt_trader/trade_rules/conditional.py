import numpy as np
import pandas as pd
from cert.myfuncs import *
import logging

class KlineConditional():
    def __init__(self):
        # 1 minute candle chart
        self.ohlcv = None
        self.opens = None
        self.highs = None
        self.lows = None
        self.closes = None
        self.volumes = None

        # 250ms candlestick realTime update
        self.rt_ohlcv = None
        self.rt_open = None
        self.rt_high = None
        self.rt_low = None
        self.rt_close = None
        self.rt_volume = None


class BBConditional(KlineConditional):
    '''
    BB와 관련된 condition들을 반환하는 class
    '''
    def __init__(self):
        super().__init__()

        # Bollinger band indicator
        self.upperBand = None
        self.upperInter = None
        self.centerLine = None
        self.lowerInter = None
        self.lowerBand = None


    def _calculateInds(self, ohlcv, rt_ohlcv, window): # callback안에서 실행되어야 함.
        # 1 minute candle chart
        self.ohlcv = ohlcv[:-1]
        self.opens = self.ohlcv['open']
        self.highs = self.ohlcv['high']
        self.lows = self.ohlcv['low']
        self.closes = self.ohlcv['close']
        self.volumes = self.ohlcv['volume']

        # 250ms candlestick realTime update
        self.rt_ohlcv = rt_ohlcv
        self.rt_open = float(rt_ohlcv['open'][-1:])
        self.rt_high = float(rt_ohlcv['high'][-1:])
        self.rt_low = float(rt_ohlcv['low'][-1:])
        self.rt_close = float(rt_ohlcv['close'][-1:])
        self.rt_volume = float(rt_ohlcv['volume'][-1:])

        # calculate BB
        ma_ = self.closes.rolling(window).mean()
        std_ = self.closes.rolling(window).std()
        self.upperBand = ma_ + 2 * std_
        self.upperInter = ma_ + std_
        self.centerLine = ma_
        self.lowerInter = ma_ - std_
        self.lowerBand = ma_ - 2 * std_

    
    def _updateCondition(self, ohlcv, rt_ohlcv, window):
        self._calculateInds(ohlcv, rt_ohlcv, window)

        # for debugging.
        print()
        
        print("- upperBand   :", end=' ')
        upperBandDisplay = np.round(np.array(self.upperBand[-5:]), 3)
        print("{:<10}  {:<10}  {:<10}  {:<10}  {:<10}".format(upperBandDisplay[0], upperBandDisplay[1], upperBandDisplay[2], upperBandDisplay[3], upperBandDisplay[4]))

        print("- upperInter  :", end=' ')
        upperInterDisplay = np.round(np.array(self.upperInter[-5:]), 3)
        print("{:<10}  {:<10}  {:<10}  {:<10}  {:<10}".format(upperInterDisplay[0], upperInterDisplay[1], upperInterDisplay[2], upperInterDisplay[3], upperInterDisplay[4]))
        
        print("- closePrice  :", end=' ')
        closePriceDisplay = np.round(np.array(self.closes[-5:]), 3)
        print("{:<10}  {:<10}  {:<10}  {:<10}  {:<10}".format(closePriceDisplay[0], closePriceDisplay[1], closePriceDisplay[2], closePriceDisplay[3], closePriceDisplay[4]))

        print("- lowerInter  :", end=' ')
        lowerInterDisplay = np.round(np.array(self.lowerInter[-5:]), 3)
        print("{:<10}  {:<10}  {:<10}  {:<10}  {:<10}".format(lowerInterDisplay[0], lowerInterDisplay[1], lowerInterDisplay[2], lowerInterDisplay[3], lowerInterDisplay[4]))

        print("- lowerBand   :", end=' ')
        lowerBandDisplay = np.round(np.array(self.lowerBand[-5:]), 3)
        print("{:<10}  {:<10}  {:<10}  {:<10}  {:<10}".format(lowerBandDisplay[0], lowerBandDisplay[1], lowerBandDisplay[2], lowerBandDisplay[3], lowerBandDisplay[4]))

        print("- currentPrice:", end=' ')
        print(" "*48 + "{:<10}".format(np.round(np.array(self.rt_close), 3)))
        
        ## Return values
        PASTcloses_gt_upperInter_5t = self.closes[-5:] > self.upperInter[-5:]
        PASTcloses_gt_upperBand_5t = self.closes[-5:] > self.upperBand[-5:]

        PASTcloses_lt_lowerInter_5t = self.closes[-5:] < self.lowerInter[-5:]
        PASTcloses_lt_lowerBand_5t = self.closes[-5:] < self.lowerBand[-5:]

        CURRclose_gt_upperInter = self.rt_close > float(self.upperInter[-1:])
        CURRclose_gt_upperBand = self.rt_close > float(self.upperBand[-1:])

        CURRclose_lt_lowerInter = self.rt_close < float(self.lowerInter[-1:])
        CURRclose_lt_lowerBand = self.rt_close < float(self.lowerBand[-1:])

        '''
        u1 = np.all(self.closes[-4:] < self.upperInter[-4:]) # 5분전 ~ 2분전 분봉에서는 close가 upperInter 아래에 있었다.
        if u1:
            u1_arrow = "<"
        else:
            u1_arrow = ">"
        print(f"## UpperInter Condition 1 {u1} : Close {u1_arrow} UpperInter 2~3 mins ago.")
        
        u2 = self.rt_close > float(self.upperBand[-1:]) # 지금은 upperInter보다 위에 있다.
        if u2:
            u2_arrow = ">"
        else:
            u2_arrow = "<"
        print(f"## UpperInter Condition 2 {u2} : Close {u2_arrow} UpperInter now.")

        is_upperInterUpBt = (u1 and u2)
        
        

        # u1, u2가 동시에 이뤄지는 경우, close가 upperInter를 하행돌파했다고 가정

        u1 = np.all(self.highs[-1:] > self.upperBand[-1:]) # 2분전 분봉에서는 high가 upperBand 위에 있다
        if u1:
            u1_arrow = ">"
        else:
            u1_arrow = "<"
        print(f"## UpperBand Condition 1 {u1} : Close {u1_arrow} UpperBand 2 mins ago.")

        u2 = self.rt_close < float(self.upperBand[-1:]) # 지금은 upperInter보다 아래에 있다.
        if u2:
            u2_arrow = "<"
        else:
            u2_arrow = ">"
        print(f"## UpperBand Condition 2 {u2} : Close {u2_arrow} UpperBand now.")

        is_upperBandDwBt = (u1 and u2)
        '''

        return (
            PASTcloses_gt_upperInter_5t, 
            PASTcloses_gt_upperBand_5t,
            PASTcloses_lt_lowerInter_5t,
            PASTcloses_lt_lowerBand_5t,
            CURRclose_gt_upperInter,
            CURRclose_gt_upperBand,
            CURRclose_lt_lowerInter,
            CURRclose_lt_lowerBand
        )



    def callback(self, ohlcv, rt_ohlcv, window=20) -> tuple:
        '''
        return values (8 values above)
        '''
        return self._updateCondition(ohlcv, rt_ohlcv, window)



class RVConditional():
    '''
    RV와 관련된 각종 condition들을 반환하는 class
    '''
    def __init__(self):
        # RV
        self.rvs = None


    def _calculateInds(self, ohlcv, window):
        self.closes = ohlcv[:-1]['close']
        _realized_volatility = log_return(self.closes).rolling(window).apply(realized_volatility)
        self.rvs = _realized_volatility
        

    def _updateCondition(self, ohlcv, window):
        self._calculateInds(ohlcv, window)
        is_aboveFrv = None
        is_belowFrv = None

        # for debugging.
        print()
        print("- currentRVs  :", end=' ')
        currentRVsDisplay = np.round(np.array(self.rvs[-5:]), 5)
        print("{:<10}  {:<10}  {:<10}  {:<10}  {:<10}".format(currentRVsDisplay[0], currentRVsDisplay[1], currentRVsDisplay[2], currentRVsDisplay[3], currentRVsDisplay[4]))

        '''
        # rv가 former RV 위에 있다.
        u1 = np.all(self.formerRvs[-1:] < self.rvs[-1:])
        if u1:
            u1_arrow = ">"
        else:
            u1_arrow = "<"
        print(f"## RV Condition 1 {u1} : currentRv {u1_arrow} formerRv") # 아래꺼는 이것과 똑같으므로 Debug printing X
        is_aboveFrv = u1
        is_belowFrv = (not u1)
        '''
        
        return self.rvs


    def callback(self, ohlcv, window=10) -> tuple:
        return self._updateCondition(ohlcv, window)