from email import feedparser
import numpy as np

class BackTester():
    def __init__(self, asset=1000, maxLimit=1000): # default _varsDict['_asset'] : 1000 dollars
        # dictionary to store information about long, short position.
        # you may use variables below for your strategy. --> use text.
        # example) if you want to use long_amount for your strategy, you just use text "_long_amount" in your condition.
        self._varsDict = dict()
        # vars for long position
        self._varsDict['_long_amount'] = 0
        self._varsDict['_long_meanPrice'] = 0
        self._varsDict['_long_flag'] = False
        # vars for short position
        self._varsDict['_short_amount'] = 0
        self._varsDict['_short_meanPrice'] = 0
        self._varsDict['_short_flag'] = False
        # vars for asset and max Limit of long, short position
        self._varsDict['_asset'] = asset
        self._varsDict['_maxLimit'] = maxLimit
        # var for basis of your wallet.
        self.PRINCIPAL = asset
        # num of trading
        self.trFreq = 0
        # if your wallet busted, when did you busted?
        self.bustedIndex = 0

        # store final return
        self.finalReturn = 0

        # var for backdata
        self.df = None

    # How much coin do you buy/sell for your position?
    ## every positioning, your buy/sell amount will be half of former positioning's amount.
    def _get_tradeAmount(self, tradePrice):
        tradeAmount = round(self._varsDict['_maxLimit']/tradePrice/2, 4)
        return tradeAmount

    # long positioning
    def set_long(self, tradePrice):
        tradeAmount = self._get_tradeAmount(tradePrice)
        self._varsDict['_maxLimit'] -= tradeAmount * tradePrice + self.get_fee(tradeAmount, tradePrice)
        self._varsDict['_long_meanPrice'] = (self._varsDict['_long_meanPrice']*self._varsDict['_long_amount'] + tradePrice*tradeAmount)/(self._varsDict['_long_amount'] + tradeAmount) # 이거 맞아?
        self._varsDict['_long_amount'] += tradeAmount
        self._varsDict['_long_flag'] = True
        self.trFreq += 1
        return

    # short positioning
    def set_short(self, tradePrice):
        tradeAmount = self._get_tradeAmount(tradePrice)
        self._varsDict['_maxLimit'] -= tradeAmount * tradePrice + self.get_fee(tradeAmount, tradePrice)
        self._varsDict['_short_meanPrice'] = (self._varsDict['_short_meanPrice']*self._varsDict['_short_amount'] + tradePrice*tradeAmount)/(self._varsDict['_short_amount'] + tradeAmount)
        self._varsDict['_short_amount'] += tradeAmount
        self._varsDict['_short_flag'] = True
        self.trFreq += 1
        return

    # clearing. 
    def set_clear(self, tradePrice):
        shortAmount = self._varsDict['_short_amount']
        longAmount = self._varsDict['_long_amount']
        self._varsDict['_asset'] -= shortAmount * (tradePrice - self._varsDict['_short_meanPrice'])
        self._varsDict['_asset'] -= self.get_fee(shortAmount, tradePrice) # calculate fee.
        self._varsDict['_asset'] += longAmount * (tradePrice - self._varsDict['_long_meanPrice'])
        self._varsDict['_asset'] -= self.get_fee(longAmount, tradePrice) # calculate fee.
        self._varsDict['_short_amount'] = self._varsDict['_long_amount'] = self._varsDict['_short_meanPrice'] = self._varsDict['_long_meanPrice'] = 0
        self._varsDict['_long_flag'] = self._varsDict['_short_flag'] = False
        self._varsDict['_maxLimit'] = self._varsDict['_asset']
        self.trFreq += 1
        return

    # long positioning : Dismiss fee calculating.
    def set_long_NOTFEE(self, tradePrice):
        tradeAmount = self._get_tradeAmount(tradePrice)
        self._varsDict['_maxLimit'] -= tradeAmount * tradePrice
        self._varsDict['_long_meanPrice'] = (self._varsDict['_long_meanPrice']*self._varsDict['_long_amount'] + tradePrice*tradeAmount)/(self._varsDict['_long_amount'] + tradeAmount) # 이거 맞아?
        self._varsDict['_long_amount'] += tradeAmount
        self._varsDict['_long_flag'] = True
        self.trFreq += 1
        return

    # short positioning : Dismiss fee calculating.
    def set_short_NOTFEE(self, tradePrice):
        tradeAmount = self._get_tradeAmount(tradePrice)
        self._varsDict['_maxLimit'] -= tradeAmount * tradePrice
        self._varsDict['_short_meanPrice'] = (self._varsDict['_short_meanPrice']*self._varsDict['_short_amount'] + tradePrice*tradeAmount)/(self._varsDict['_short_amount'] + tradeAmount)
        self._varsDict['_short_amount'] += tradeAmount
        self._varsDict['_short_flag'] = True
        self.trFreq += 1
        return

    # clearing.  : Dismiss fee calculating.
    def set_clear_NOTFEE(self, tradePrice):
        self._varsDict['_asset'] -= self._varsDict['_short_amount'] * (tradePrice - self._varsDict['_short_meanPrice'])
        self._varsDict['_asset'] += self._varsDict['_long_amount'] * (tradePrice - self._varsDict['_long_meanPrice'])
        self._varsDict['_short_amount'] = self._varsDict['_long_amount'] = self._varsDict['_short_meanPrice'] = self._varsDict['_long_meanPrice'] = 0
        self._varsDict['_long_flag'] = self._varsDict['_short_flag'] = False
        self._varsDict['_maxLimit'] = self._varsDict['_asset']
        self.trFreq += 1
        return

    # check asset positive. if asset < 0, you will receive "Busted" message.
    def check_asset_positive(self, tradePrice):
        tmpAsset = self._varsDict['_asset'] - (self._varsDict['_short_amount'] * (tradePrice - self._varsDict['_short_meanPrice']))
        tmpAsset = self._varsDict['_asset'] + (self._varsDict['_long_amount'] * (tradePrice - self._varsDict['_long_meanPrice']))
        if tmpAsset < 0:
            return False
        else:
            return True

    # for testing, 
    def get_log(self, index, stateTxt):
        print(f'#########################')
        print(f'## index {index}, {stateTxt}')
        print(f'#########################')

        if stateTxt != 'Busted':
            print('long amount:', self._varsDict['_long_amount'])
            print('long meanPrice:', self._varsDict['_long_meanPrice'])
            print('short amount:', self._varsDict['_short_amount'])
            print('short meanPrice:', self._varsDict['_short_meanPrice'])
            print('asset:', self._varsDict['_asset'])
            print('maxLimit:', self._varsDict['_maxLimit'])
            self.bustedIndex = index

    def get_current_return(self):
        # print('**current return : ', self._varsDict['_asset']/self.PRINCIPAL*100, '%')
        return self._varsDict['_asset'] / self.PRINCIPAL

    def get_fee(self, tradeAmount, tradePrice, TB = 'T'):
        market = 0.04
        limit = 0.02
        if TB == 'T':
            rate = market
        else:
            rate = limit
        fee = tradeAmount * rate * tradePrice
        return fee

    # backtesting code with own strategy
    ## strategy Instance, DataGen Instance가 전부 정의되어 있어야 함.

    # 이 아래의 것은, GenBackData 파일이 잘 만들어졌을 때 기능함.
    # def backtest(self, strategyInstance, dataInstance):
    #     strategy = strategyInstance
    #     data = dataInstance
    #     self.df = data.backdata

    # GenBackData 파일이 아직 만들어지지 않았으므로 아래의 메소드를 사용
    def backtest_tmp(self, strategyInstance, df, printLog=True, saveProfit=True):
        strategy = strategyInstance
        self.df = df

        for currentIdx in range(strategy.oldest, len(self.df)-strategy.newest):
            currentPrice = self.df['Close'][currentIdx]

            # clear position
            realClearAndConditions = []
            for clear_and_conditions in strategy.clear_conditions:
                realClearAndConditions.append(all(self._make_conditions(currentIdx, clear_and_conditions)))
            if any(realClearAndConditions) and (self._varsDict['_long_flag'] or self._varsDict['_short_flag']):
                self.set_clear(currentPrice)
                if printLog:
                    self.get_log(currentIdx, 'clear')

            # long position
            realLongAndConditions = []
            for long_and_conditions in strategy.long_conditions:
                realLongAndConditions.append(all(self._make_conditions(currentIdx, long_and_conditions)))
            if any(realLongAndConditions):
                self.set_long(currentPrice)
                if printLog:
                    self.get_log(currentIdx, 'long')

            # short position
            realShortAndConditions = []
            for short_and_conditions in strategy.short_conditions:
                realShortAndConditions.append(all(self._make_conditions(currentIdx, short_and_conditions)))
            if any(realShortAndConditions):
                self.set_short(currentPrice)
                if printLog:
                    self.get_log(currentIdx, 'short')

            if not self.check_asset_positive(currentPrice):
                self.get_log(currentIdx, 'Busted')

        self.finalReturn = self.get_current_return()

    # convert pseudo-condition to REAL condition(usable in python)
    ## make conditions list
    def _make_conditions(self, currentIdx, conditions):
        real_conditions = []
        for p_cond in conditions:
            real_cond = self._make_real_condition(currentIdx, p_cond)
            real_conditions.append(real_cond)
        return real_conditions

    ## make a pseudo-condition to one real condition
    def _make_real_condition(self, currentIdx, p_cond):
        indc1, indc2, op, func1, func2, pastIdx = p_cond

        # making data1
        if indc1 in self._varsDict.keys():
            data1 = self._varsDict[indc1]
        elif type(indc1) in [type(1), type(0.5), type(True)]:
            data1 = indc1
        else:
            if func1:
                data1 = func1(self.df[indc1][currentIdx-pastIdx])
            else:
                data1 = self.df[indc1][currentIdx-pastIdx]

        # making data2
        if indc2 in self._varsDict.keys():
            data2 = self._varsDict[indc2]
        elif type(indc2) in [type(1), type(0.5), type(True)]:
            data2 = indc2
        else:
            if func2:
                data2 = func2(self.df[indc2][currentIdx-pastIdx])
            else:
                data2 = self.df[indc2][currentIdx-pastIdx]

        # making condition using data1, data2 and comparing operator.
        if op=='<':
            return data1<data2
        elif op=='<=':
            return data1<=data2
        elif op=='>':
            return data1>data2
        elif op=='>=':
            return data1>=data2
        elif op=='==':
            return data1==data2

    # methods for making indicators.
    ## 이 아래의 메소드들은 BackTester가 아니라, 일반적인 indicator를 만드는 새로운 class를 정의해서 그 안에 넣어야 하지 않을까?
    ## 또는 그냥 numpy method에 대한 이해가 있으면 numpy만으로도 충분할 것 같음.
    def get_MA(self, window, closePrice): # closePrice는 데이터프레임에서 만들어져야 하니까. 데이터프레임....이 있어야 하니까. 실제 데이터를 쓰는 BackTester에 있어야?
        indicator = closePrice.astype(np.float64).rolling(window).mean()
        # self.ma[f'MA{window}'] = indicator
        return indicator

    def get_std(self, window, closePrice):
        indicator = closePrice.astype(np.float64).rolling(window).std()
        # self.std[f'std{window}'] = indicator
        return indicator

    ## make indicator for yourself.
    '''
    이거 정말 필요할까? 안 필요할지도.
    '''
    ## you have to use your data from DataGen
    def get_own_indicator(self, indicatorName, indicator):
        self.ownInd[indicatorName] = indicator
        return indicator