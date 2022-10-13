import numpy as np


# def get_MA(dataDf, window, CloseName='Close'):
#     return dataDf[CloseName].astype(np.float64).rolling(window).mean()

# def get_std(dataDf, window, CloseName='Close'):
#     return dataDf[CloseName].astype(np.float64).rolling(window).std()


class StrategyArchive():
    def __init__(self, oldest=4, newest=0):
        # How many data will you use?
        self.oldest = oldest
        self.newest = newest

        # save your conditions.
        self.tmp_conditions = []

        self.long_conditions = []
        self.short_conditions = []
        self.clear_conditions = []

        # for building deeper strategy (not essential)
        ## take Profit conditions
        self.takeProfit_long_conditions = []
        self.takeProfit_short_conditions = []
        ## stop Loss conditions
        self.stopLoss_long_conditions = []
        self.stopLoss_short_conditions = []

        # Moving Average lists
        self.ma = dict()
        
        # StdDev lists
        self.std = dict()

        # own indicators
        self.ownInd = dict()

    # methods for making indicators.
    def get_MA(self, window, closePrice): # closePrice는 데이터프레임에서 만들어져야 하니까. 데이터프레임....이 있어야 하니까. 실제 데이터를 쓰는 BackTester에 있어야?
        indicator = closePrice.astype(np.float64).rolling(window).mean()
        self.ma[f'MA{window}'] = indicator
        return indicator

    def get_std(self, window, closePrice):
        indicator = closePrice.astype(np.float64).rolling(window).std()
        self.std[f'std{window}'] = indicator
        return indicator

    ## make indicator for yourself.
    ## you have to use your data from DataGen
    def get_own_indicator(self, indicatorName, indicator):
        self.ownInd[indicatorName] = indicator
        return indicator

    # method for making condition.
    def add_condition(self, LSC, func1, indc1, compareOperator, func2, indc2, indices):
        # if index exceeded using_indices, modify oldest/newest index automatically.
        if max(indices)>self.oldest:
            print("oldest index modified.")
            self.oldest = max(indices)
        if min(indices)<self.newest:
            print("newest index modified.")
            self.newest = min(indices)
        
        '''
        아래 문장은 무시하기. 여기에 column data를 저장하는 방식은 좋지 않은 듯.
        # 이 부분에서 df에서 column1, column2를 가져와서 column1data, column2data를 만드는 과정이 필요함
        '''
        conditions = []
        for idx in indices:
            conditions.append = [func1, indc1, compareOperator, func2, indc2, idx]

        if LSC=='long':
            self.long_conditions += conditions
        elif LSC=='short':
            self.short_conditions += conditions
        elif LSC=='clear':
            self.clear_conditions += conditions

        # if you want to build deeper strategy.
        elif LSC=='takeProfit_long':
            self.takeProfit_long_conditions += conditions
        elif LSC=='takeProfit_short':
            self.takeProfit_short_conditions += conditions
        elif LSC=='stopLoss_long':
            self.stopLoss_long_conditions += conditions
        elif LSC=='stopLoss_short':
            self.stopLoss_short_conditions += conditions

    def add_andCondition(self, indc1Name, indc2Name, compareOperator, indices, **funcs):
        '''
        Condition 작성 방법 :
        indicator1, indicator2, compare_operator, indices, **funcs
        indicator1, indicator2 : 비교하고 싶은 지표
        compare_operator : indicator1과 indicator2의 사이에 들어갈 비교연산자
        indices : n(=int)를 넣으면 현재시점-n번째의 데이터를 이용해 조건을 생성
                : l(=list)를 넣으면 현재시점-l0 ~ 현재시점-l1까지의 데이터를 모두 사용해 여러 조건을 생성
        **funcs : indicator1, indicator2에 임의로 조정을 가하여 조건을 만들고 싶을 때 사용.
                : func1, func2의 인자 이름으로 들어가야 함. 만약 인자로 들어온다면, indicator1, indicator2는
                : func1(indicator1), func2(indicator2)의 값으로서 비교될 것.
        '''
        try:
            func1 = funcs['func1']
        except:
            func1 = None
        
        try:
            func2 = funcs['func2']
        except:
            func2 = None

        if type(indices)==type(1):
            self.tmp_conditions.append([indc1Name, indc2Name, compareOperator, func1, func2, indices])
        else:
            for idx in range(indices[0], indices[1]+1):
                self.tmp_conditions.append([indc1Name, indc2Name, compareOperator, func1, func2, idx])

    def add_Condition(self, LSC):
        if LSC=='long':
            self.long_conditions.append(self.tmp_conditions)
        elif LSC=='short':
            self.short_conditions.append(self.tmp_conditions)
        elif LSC=='clear':
            self.clear_conditions.append(self.tmp_conditions)       

        self.tmp_conditions = []

    def get_saved_indicators(self):
        return self.ma, self.std, self.ownInd