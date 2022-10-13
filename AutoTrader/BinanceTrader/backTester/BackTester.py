import numpy as np

class BackTester():
    def __init__(self, asset=1000, maxLimit=1000): # default _varsDict['_asset'] : 1000 dollars
        self._varsDict = dict()
        self._varsDict['_long_amount'] = 0
        self._varsDict['_long_meanPrice'] = 0
        self._varsDict['_long_flag'] = False

        self._varsDict['_short_amount'] = 0
        self._varsDict['_short_meanPrice'] = 0
        self._varsDict['_short_flag'] = False

        self._varsDict['_asset'] = asset
        self.PRINCIPAL = asset
        self._varsDict['_maxLimit'] = maxLimit
        self.bustedIndex = 0
        # var for backdata
        self.df = None
        # vars for BackTester variables
        self._vars = ['_long_amount',
                      '_long_meanPrice', 
                      '_long_flag', 
                      '_short_amount', 
                      '_short_meanPrice', 
                      '_short_flag',
                      '_asset',
                      '_maxLimit']

        '''
        # vars for long position
        self._varsDict['_long_amount'] = 0
        self._varsDict['_long_meanPrice'] = 0
        self._varsDict['_long_flag'] = False
        # vars for short position
        self._varsDict['_short_amount'] = 0
        self._varsDict['_short_meanPrice'] = 0
        self._varsDict['_short_flag'] = False
        # vars for base _varsDict['_asset']
        self._varsDict['_asset'] = _varsDict['_asset']
        self.PRINCIPAL = _varsDict['_asset'] # constant
        self._varsDict['_maxLimit'] = _varsDict['_maxLimit']
        # var for busted (when did you bust?)
        self.bustedIndex = 0
        # var for backdata
        self.df = None
        # vars for BackTester variables
        self._vars = ['_long_amount',
                      '_long_meanPrice', 
                      '_long_flag', 
                      '_short_amount', 
                      '_short_meanPrice', 
                      '_short_flag',
                      '_asset',
                      '_maxLimit']
        '''

    def _get_tradeAmount(self, tradePrice):
        tradeAmount = round(self._varsDict['_maxLimit']/tradePrice/2, 4)
        return tradeAmount

    def set_long(self, tradePrice):
        tradeAmount = self._get_tradeAmount(tradePrice)
        self._varsDict['_maxLimit'] -= tradeAmount * tradePrice
        self._varsDict['_long_meanPrice'] = (self._varsDict['_long_meanPrice']*self._varsDict['_long_amount'] + tradePrice*tradeAmount)/(self._varsDict['_long_amount'] + tradeAmount) # 이거 맞아?
        self._varsDict['_long_amount'] += tradeAmount
        self._varsDict['_long_flag'] = True
        return

    def set_short(self, tradePrice):
        tradeAmount = self._get_tradeAmount(tradePrice)
        self._varsDict['_maxLimit'] -= tradeAmount * tradePrice
        self._varsDict['_short_meanPrice'] = (self._varsDict['_short_meanPrice']*self._varsDict['_short_amount'] + tradePrice*tradeAmount)/(self._varsDict['_short_amount'] + tradeAmount)
        self._varsDict['_short_amount'] += tradeAmount
        self._varsDict['_short_flag'] = True
        return

    def set_clear(self, tradePrice):
        self._varsDict['_asset'] -= self._varsDict['_short_amount'] * (tradePrice - self._varsDict['_short_meanPrice'])
        self._varsDict['_asset'] += self._varsDict['_long_amount'] * (tradePrice - self._varsDict['_long_meanPrice'])
        self._varsDict['_short_amount'] = self._varsDict['_long_amount'] = self._varsDict['_short_meanPrice'] = self._varsDict['_long_meanPrice'] = 0
        self._varsDict['_long_flag'] = self._varsDict['_short_flag'] = False
        self._varsDict['_maxLimit'] = self._varsDict['_asset']
        return

    def check_asset_positive(self, tradePrice):
        tmpAsset = self._varsDict['_asset'] - (self._varsDict['_short_amount'] * (tradePrice - self._varsDict['_short_meanPrice']))
        tmpAsset = self._varsDict['_asset'] + (self._varsDict['_long_amount'] * (tradePrice - self._varsDict['_long_meanPrice']))
        if tmpAsset < 0:
            return False
        else:
            return True

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

    def get_current_return(self, index):
        print('**current return : ', self._varsDict['_asset']/self.PRINCIPAL*100, '%')
        return self._varsDict['_asset'] / self.PRINCIPAL

    def get_commission(self):
        pass

    # backtesting code with own strategy
    ## strategy Instance, DataGen Instance가 전부 정의되어 있어야 함.

    # 이 아래의 것은, GenBackData 파일이 잘 만들어졌을 때 기능함.
    # def backtest(self, strategyInstance, dataInstance):
    #     strategy = strategyInstance
    #     data = dataInstance
    #     self.df = data.backdata

    # GenBackData 파일이 아직 만들어지지 않았으므로 아래의 메소드를 사용
    def backtest_tmp(self, strategyInstance, df):
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
                self.get_log(currentIdx, 'clear')

            # long position
            realLongAndConditions = []
            for long_and_conditions in strategy.long_conditions:
                realLongAndConditions.append(all(self._make_conditions(currentIdx, long_and_conditions)))
            if any(realLongAndConditions):
                self.set_long(currentPrice)
                self.get_log(currentIdx, 'long')

            # short position
            realShortAndConditions = []
            for short_and_conditions in strategy.short_conditions:
                realShortAndConditions.append(all(self._make_conditions(currentIdx, short_and_conditions)))
            if any(realShortAndConditions):
                self.set_short(currentPrice)
                self.get_log(currentIdx, 'short')

            '''
            # long position
            long_conditions = self._make_conditions(currentIdx, strategy.long_conditions)
            if all(long_conditions):
                self.set_long(currentPrice)
                self.get_log(currentIdx, 'long')

            # short position
            short_conditions = self._make_conditions(currentIdx, strategy.short_conditions)
            if all(short_conditions):
                self.set_short(currentPrice)
                self.get_log(currentIdx, 'short')

            # clear position
            clear_conditions = self._make_conditions(currentIdx, strategy.clear_conditions)
            if all(clear_conditions):
                self.set_clear(currentPrice)
                self.get_log(currentIdx, 'clear')

            # 왜 이렇게 어렵냐.... 위의 거는 OR 조건에 대한 생각 없이 만든 것. 혹시 몰라서 남겨놓습니다.
            '''

            # takeProfit OR stopLoss clearing : not updated yet
            #
            #
            #
            #
            #
            #

        if not self.check_asset_positive(currentPrice):
            self.get_log(currentIdx, 'Busted')

    # convert pseudo-condition to REAL condition(usable in python)
    ## make conditions list
    def _make_conditions(self, currentIdx, conditions):
        real_conditions = []
        for p_cond in conditions:
            real_cond = self._make_real_condition(p_cond, currentIdx)
            real_conditions.append(real_cond)
        return real_conditions

    ## make a pseudo-condition to one real condition
    def _make_real_condition(self, p_cond, currentIdx):
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


    ## make a pseudo-condition to one real condition
    ### 
    '''
    def _make_real_condition_DONOTUSE(self, p_cond, currentIdx):
        func1, indc1, op, func2, indc2, pastIdx = p_cond
        if indc1=='_varsDict['_short_amount']':
            data1 = self._varsDict['_short_amount']
        elif indc1=='_varsDict['_long_amount']':
            data1 = self._varsDict['_long_amount']
        elif type(indc1)==type(""):
            data1 = func1(self.df[indc1][currentIdx-pastIdx])
        elif type(indc1)==type(0.5):
            data1 = indc1

        if indc2=='_varsDict['_short_amount']':
            data2 = self._varsDict['_short_amount']
        elif indc2=='_varsDict['_long_amount']':
            data2 = self._varsDict['_long_amount']
        elif type(indc2)==type(""):
            data2 = func2(self.df[indc2][currentIdx-pastIdx])
        elif type(indc2)==type(0.5):
            data2 = indc2

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

    '''

    # methods for making indicators.
    def get_MA(self, window, closePrice): # closePrice는 데이터프레임에서 만들어져야 하니까. 데이터프레임....이 있어야 하니까. 실제 데이터를 쓰는 BackTester에 있어야?
        indicator = closePrice.astype(np.float64).rolling(window).mean()
        # self.ma[f'MA{window}'] = indicator
        return indicator

    def get_std(self, window, closePrice):
        indicator = closePrice.astype(np.float64).rolling(window).std()
        # self.std[f'std{window}'] = indicator
        return indicator

    ## make indicator for yourself.
    ## you have to use your data from DataGen
    def get_own_indicator(self, indicatorName, indicator):
        self.ownInd[indicatorName] = indicator
        return indicator