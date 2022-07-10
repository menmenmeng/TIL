class Human():
    '''
    사람
    '''

person1 = Human()
person2 = Human()

person1.language = "한국어"
person2.language = "English"

person1.name = '서울시민'
person2.name = '인도인'

# 클래스를 왜 쓰는 걸까?
# 코드를 만드는 데 꼭 필요하지는 않은 인위적인 도구.
# 그러나 클래스, 인스턴스를 이용하면 데이터를 사람이 알아보기 쉽게 포장할 수 있다
# language, name뿐 아니라 인간의 행동도 class안에 넣을 수 있다.

def speak(person):
    print(f'{person.name}이 {person.language}로 말을 합니다.')

speak(person1)
speak(person2)

# 함수가 클래스 안에 들어갈 수 있단..건데.
# 클래스 안에 어떻게 만들 수 있는가?

Human.speak = speak # Human 안의 speak를 기존의 speak로 만들겠다.
person1.speak()
person2.speak()