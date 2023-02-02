import numpy as np
import time
from cert.myfuncs import *

class Conditional():
    def __init__(self):
        self.openLong = False
        self.openShort = False
        self.closeLong = False
        self.closeShort = False


    def cutArray(self, array, timeLimit):
        try:
            res = array[len(array)-timeLimit:]
        except:
            res = array
        return res


    def returnConds(self):
        return self.openLong, self.openShort, self.closeLong, self.closeShort
    


class BBConditional(Conditional):
    '''
    Bollinger Band breakthrough condition.
    '''
    def __init__(self):
        super().__init__()
        self.markPrices = None
        self.upperBand = None
        self.upperInter = None
        self.centerLine = None
        self.lowerInter = None
        self.lowerBand = None


    def _calculateInds(self, markPriceDf, window):
        markPrices = markPriceDf['markPrice']
        _std = markPrices.rolling(window).std()
        centerLine = markPrices.rolling(window).mean()

        '''
        Lines which will be used in this strategy.
        '''
        upperBand = centerLine + 2*_std
        upperInter = centerLine + _std
        # centerLine
        lowerInter = centerLine - _std
        lowerBand = centerLine - 2*_std

        self.markPrices = markPrices
        self.upperBand = upperBand
        self.upperInter = upperInter
        self.centerLine = centerLine
        self.lowerInter = lowerInter
        self.lowerBand = lowerBand
        return markPrices, upperBand, upperInter, centerLine, lowerInter, lowerBand


    def _checkTradeInds(self, markPriceDf, window, timeLimit):
        markPrices, upperBand, upperInter, centerLine, lowerInter, lowerBand = self._calculateInds(markPriceDf, window)
        '''
        Buy Indicator is composed of two indicators.
        One is Open Long Indicator, The other is Close Short Indicator.
        vice versa, to Sell Indicator.
        '''
        # Open indicators
        openLongIndicator = (markPrices > upperBand)[-timeLimit:]
        openShortIndicator = (markPrices < lowerBand)[-timeLimit:]

        # Close indicators
        closeLongIndicator = (markPrices < upperInter)[-timeLimit:]
        closeShortIndicator = (markPrices > lowerInter)[-timeLimit:]

        return openLongIndicator, closeShortIndicator, openShortIndicator, closeLongIndicator
        

    def getTradeConds(self, markPriceDf, window, openThr):
        openLongIndicator, closeShortIndicator, openShortIndicator, closeLongIndicator = self._checkTradeInds(markPriceDf, window)
        if openLongIndicator.sum() >= openThr:
            self.openLong = True
        else:
            self.openLong = False

        if openShortIndicator.sum() >= openThr:
            self.openShort = True
        else:
            self.openShort = False

        '''
        When using Trailing_Stop Trade, no need to use closeIndicator.
        '''
        if list(closeShortIndicator)[-1]:
            self.closeShort = True
        else:
            self.closeShort = False

        if list(closeLongIndicator)[-1]:
            self.closeLong = True
        else:
            self.closeLong = False



class RVConditional(Conditional):
    def __init__(self):
        super().__init__()
        self.rv1 = None
        self.rv2 = None

    
    def _calculateInds(self, markPriceDf, window1, window2):
        markPrices = markPriceDf['markPrice']
        rv1 = log_return(markPrices).rolling(window1).apply(realized_volatility)
        rv2 = log_return(markPrices).rolling(window2).apply(realized_volatility)
        self.rv1, self.rv2 = rv1, rv2
        return rv1, rv2


    def getTradeConds(self, markPriceDf, window1, window2, timeLimit):
        rv1, rv2 = self._calculateInds(markPriceDf, window1, window2)
        rv1_timeLimit, rv2_timeLimit = rv1[-timeLimit:], rv2[-timeLimit:]

        self.openLong = np.all(rv1_timeLimit > rv2_timeLimit)
        self.openShort = np.all(rv1_timeLimit > rv2_timeLimit)

        self.closeLong = True
        self.closeShort = True

        
        






'''

class MAConditional(Conditional):

    def __init__(self):
        super().__init__()
        self.ma1 = None
        self.ma2 = None
        self.breakthrough_up = []
        self.breakthrough_down = []


    def _calculate_indicators(self, markPriceDf, window1, window2):
        ma1 = markPriceDf['markPrice'].rolling(window1).mean()
        ma2 = markPriceDf['markPrice'].rolling(window2).mean()
        self.ma1, self.ma2 = ma1, ma2
        return ma1, ma2

    
    def _check_conditions(self, markPriceDf, window1, window2):
        ma1, ma2 = self._calculate_indicators(markPriceDf, window1, window2)
        
            
            

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


    def checkCondition(self):
        # this method will be executed in Final callback function.
        pass

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

'''