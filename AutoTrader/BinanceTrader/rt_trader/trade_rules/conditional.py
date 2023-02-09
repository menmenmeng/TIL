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
        self.ohlcv = ohlcv
        self.opens = ohlcv['open']
        self.highs = ohlcv['high']
        self.lows = ohlcv['low']
        self.closes = ohlcv['close']
        self.volumes = ohlcv['volume']

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
        # is_upperBandUpBt = None # close가 upperBand를 상행돌파
        # is_upperInterDwBt = None # close가 upperInter를 하행돌파

        is_upperInterUpBt = None # close가 upperInter를 상행돌파
        is_upperBandDwBt = None # close가 upperBand를 하행돌파

        is_lowerBandDwBt = None # close가 lowerBand를 하행돌파
        is_lowerInterUpBt = None # close가 lowerInter를 상행돌파

        # for debugging.
        print()
        print("- closePrice")
        print(np.round(np.array(self.closes[-5:]), 3))
        print("- upperBand")
        print(np.round(np.array(self.upperBand[-5:]), 3))
        print("- upperInter")
        print(np.round(np.array(self.upperInter[-5:]), 3))
        print("- currentPrice")
        print(np.round(np.array(self.rt_close), 3))

        # u1, u2가 동시에 이뤄지는 경우, close가 upperBand를 상행돌파했다고 가정

        u1 = np.all(self.closes[-3:-1] < self.upperInter[-3:-1]) # 3분전 ~ 2분전 분봉에서는 close가 upperInter 아래에 있었다.
        if u1:
            u1_arrow = "<"
        else:
            u1_arrow = ">"
        print(f"## UpperInter Condition 1 : Close {u1_arrow} UpperInter 2~3 mins ago.")
        
        u2 = self.rt_close > float(self.upperBand[-1:]) # 지금은 upperInter보다 위에 있다.
        if u2:
            u2_arrow = ">"
        else:
            u2_arrow = "<"
        print(f"## UpperInter Condition 2 : Close {u2_arrow} UpperInter now.")

        is_upperInterUpBt = (u1 and u2)
        
        

        # u1, u2가 동시에 이뤄지는 경우, close가 upperInter를 하행돌파했다고 가정

        u1 = np.all(self.closes[-2:-1] > self.upperBand[-2:-1]) # 2분전 분봉에서는 close가 upperBand 위에 있다
        if u1:
            u1_arrow = ">"
        else:
            u1_arrow = "<"
        print(f"## UpperBand Condition 1 : Close {u1_arrow} UpperBand 2 mins ago.")

        u2 = self.rt_close < float(self.upperBand[-1:]) # 지금은 upperInter보다 아래에 있다.
        if u2:
            u2_arrow = "<"
        else:
            u2_arrow = ">"
        print(f"## UpperBand Condition 2 : Close {u2_arrow} UpperBand now.")

        is_upperBandDwBt = (u1 and u2)

        return is_upperInterUpBt, is_upperBandDwBt


    def callback(self, ohlcv, rt_ohlcv, window=20) -> tuple:
        '''
        return values

        - is_upperInterUpBt,
        - is_upperBandDwBt
        '''
        return self._updateCondition(ohlcv, rt_ohlcv, window)



class RVConditional():
    '''
    RV와 관련된 각종 condition들을 반환하는 class
    '''
    def __init__(self):
        # RV
        self.rvs = None
        self.formerRvs = None


    def _calculateInds(self, ohlcv, window):
        self.closes = ohlcv['close']
        log_return_ = log_return(self.closes)
        realized_volatility_ = log_return_.rolling(window).apply(realized_volatility)
        self.rvs = realized_volatility_
        self.formerRvs = realized_volatility_.shift(10)
        

    def _updateCondition(self, ohlcv, window):
        self._calculateInds(ohlcv, window)
        is_aboveFrv = None
        is_belowFrv = None

        # for debugging.
        print()
        print('- formerRvs')
        print(np.round(np.array(self.formerRvs[-5:]), 3))
        print('- currentRvs')
        print(np.round(np.array(self.rvs[-5:]), 3))

        # rv가 former RV 위에 있다.
        u1 = np.all(self.formerRvs[-1:] < self.rvs[-1:])
        if u1:
            u1_arrow = ">"
        else:
            u1_arrow = "<"
        print(f"## RV Condition 1 : currentRv {u1_arrow} formerRv") # 아래꺼는 이것과 똑같으므로 Debug printing X
        is_aboveFrv = u1

        # rv가 former RV 아래에 있다.
        u1 = np.all(self.formerRvs[-1:] > self.rvs[-1:])
        is_belowFrv = u1

        return is_aboveFrv, is_belowFrv


    def callback(self, ohlcv, window=10) -> tuple:
        return self._updateCondition(ohlcv, window)