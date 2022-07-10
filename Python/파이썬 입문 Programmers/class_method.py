class Human():
    '''인간'''
    def __init__(self, name, weight):
        '''
        초기화 함수
        인스턴스를 만드는 순간에 자동으로 호출이 되는 함수이다. 기존의 create함수를 대체 가능.
        '''
        self.name = name
        self.weight = weight

    def __str__(self):
        '''
        문자열화 함수
        인스턴스가 문자열로 어떻게 표현될지를 결정
        Human을 string으로 표현할 때(print 등) 어떻게 표현할 것인가.
        '''
        return f"{self.name}(몸무게 {self.weight}kg)"

    '''양쪽에 모두 언더바 두 개 : 파이썬에서 특별한 함수이다.'''

    # def create(name, weight):
    #     person = Human()
    #     person.name = name
    #     person.weight = weight
    #     return person

    def eat(self):
        self.weight += 0.1
        print(f"{self.name}가 먹어서 {self.weight}kg이 되었습니다.")

    def walk(self):
        self.weight -= 0.1
        print(f"{self.name}가 걸어서 {self.weight}kg이 되었습니다.")

    def speak(self, message):
        print(message)


person = Human('사람', 60.5)
print(person)