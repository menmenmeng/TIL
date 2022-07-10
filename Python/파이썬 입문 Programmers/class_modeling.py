# 현실의 개념을 더 쉽게 코드에서 표현하기 위해 클래스를 사용한다.
# Human 클래스를 더 풍부하게 만들어 보자.

# 사람을, 먹으면 살이 찌고 걸으면 살이 빠지는 존재라는 걸 class로 표현하겠다.
class Human():
    '''
    인간에 대한 클래스
    '''

# person = Human()
# person.name = '철수'
# person.weight = 60.5

def create_human(name, weight):
    person = Human()
    person.name = name
    person.weight = weight
    return person

Human.create = create_human

person = Human.create('철수', 60.5)

def eat(person):
    person.weight += 0.1
    print(f"{person.name}가 먹어서 {person.weight}kg이 되었습니다.")

def walk(person):
    person.weight -= 0.1
    print(f"{person.name}가 걸어서 {person.weight}kg이 되었습니다.")

Human.eat = eat
Human.walk = walk

person.walk()
person.eat()
person.walk()

# 이렇게, 클래스로 현실을 표현하는 걸 Modeling이라고 한다. !!!!