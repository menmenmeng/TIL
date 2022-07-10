# init에서 이러한 super()를 가장 많이 사용한다.

class Animal():
    def __init__(self, name):
        self.name = name
    
    def walk(self):
        print("걷는다")
    
    def eat(self):
        print("먹는다")

    def greet(self):
        print(f"{self.name}이/가 인사한다")

class Human(Animal):
    # 왼손잡이인지, 오른손잡이인지도 알 수 있지 않을까?!
    def __init__(self, name, hand):
        super().__init__(name)
        self.hand = hand

    def wave(self):
        print(f"{self.hand}을 흔들면서")

    def greet(self):
        self.wave()
        super().greet()

person = Human("사람", "오른손")
person.greet()
