class ConditionGenerator():
    def __init__(self, oldest=4, newest=0): # oldest일 전꺼 부터, newest일 전 것 까지. 여기서는, 4일전 데이터 부터 0일 전 데이터까지 사용한다. 는 뜻
        # How many data will you use?
        self.oldest = oldest  # index는 0부터 시작이므로, 4일 전 것부터 라는 말은 즉 0, 1, 2, 3, 4. 4에서부터 계산이 시작된다는 것.
        self.newest = newest

        # save your conditions.
        self.tmp_conditions = []

        self.long_conditions = []
        self.short_conditions = []
        self.clear_conditions = []

    # methods for making conditions.
    ## method for making conditions which are connected with "AND"
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
            if indices>self.oldest:
                print("oldest index modified.")
                self.oldest = indices
            elif indices<self.newest:
                print("newest index modified.")
                self.newest = indices  

            self.tmp_conditions.append([indc1Name, indc2Name, compareOperator, func1, func2, indices])

        else:
            if max(indices)>self.oldest:
                print("oldest index modified.")
                self.oldest = max(indices)
            if min(indices)<self.newest:
                print("newest index modified.")
                self.newest = min(indices)

            for idx in range(min(indices), max(indices)+1):
                self.tmp_conditions.append([indc1Name, indc2Name, compareOperator, func1, func2, idx])

    ## method to add "OR" condition to long, short, and clear conditions.
    def add_condition(self, LSC):
        if LSC=='long':
            self.long_conditions.append(self.tmp_conditions)
        elif LSC=='short':
            self.short_conditions.append(self.tmp_conditions)
        elif LSC=='clear':
            self.clear_conditions.append(self.tmp_conditions)       

        self.tmp_conditions = []