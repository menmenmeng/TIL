# walk, eat은 Human도 Dog도 똑같다!
# 사람, 개는 많은 걸 공유한다. 동물이기 때문에, 이런 겹치는 개념들을 일일이 따로 만드는 건 비효율적이다.
# 고양이, 닭, ... 많은 동물들이 있을 텐데 얘네 만들 때마다 하나씩 walk, eat을 만드는 건 비효율적
# 거기다 더해서, 만약. 모든 동물에게 walk, eat뿐만 아니라 poop라는 새로운 함수가 추가된다고 가정해 보자.
# 모든 동물 클래스에 poop을 넣는 건 진짜 비효율적임. 복붙을 몇 번 해야 되는 거야

# 자식 클래스는 부모 클래스가 가진 메소드를 그대로 사용할 수 있다.

class Animal():
    def walk(self):
        print("걷는다")
    
    def eat(self):
        print("먹는다")


class Human(Animal):
    def wave(self):
        print("손을 흔든다")


class Dog(Animal):
    def wag(self):
        print("꼬리를 흔든다")

person = Human()
person.walk()
person.eat()
person.wave()

dog = Dog()
dog.walk()
dog.eat()
dog.wag()

