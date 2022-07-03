# 사칙연산 클래스
# 클래스 상속
# 메소드 오버라이딩(SafeFourCal) : ZeroDivisionError를 방지하는 FourCal
# 클래스 변수(!=객체 변수)

# 사칙연산 클래스
class FourCal:
    def __init__(self):
        self.result = 0

    def setdata(self, first, second):
        self.first = first
        self.second = second
    
    def add(self):
        self.result = self.first + self.second
        return self.result

    def sub(self):
        self.result = self.first - self.second
        return self.result
    
    def mul(self):
        self.result = self.first * self.second
        return self.result

    def div(self):
        self.result = self.first / self.second
        return self.result
        


# 클래스 상속 : FourCal의 모든 메소드가 여기에 이미 다 들어있다고 볼 수 있음
class MoreFourCal(FourCal):
    def pow(self):
        self.result = self.first ** self.second
        return self.result

print("--클래스 상속")
a = MoreFourCal()
a.setdata(4, 2)
print(a.add())
print(a.pow())


# 클래스 메소드 오버라이딩
class SafeFourCal(FourCal):
    def div(self):
        if self.second == 0:
            return 0
        else:
            return self.first / self.second

print('--메소드 오버라이딩')
b = SafeFourCal()
b.setdata(4, 0)
print(b.div())
b.setdata(4, 2)
print(b.div())


# 모든 클래스 인스턴스에 적용되는, 클래스 변수 (객체변수와 다름)
class Family:
    lastname = '김'

print('--클래스 변수')
a = Family()
b = Family()
print(a.lastname)
print(b.lastname)

Family.lastname = '박'
print(a.lastname)
print(b.lastname)


# 클래스 상속 - 상속받아서 새로 만들어진 클래스는 이전 클래스의 변수도 가지고 있다.
class MyClass:
	def __init__(self):
		self.name = 'Myeonghyeon'

class MyClass2(MyClass):
    def newmethod(self, x, y):
        print(x, y)
        return x+y

newclass = MyClass2()
print('--클래스 상속이 변수도 상속')
print(newclass.name)


# 수학을 위한 메서드
class NewString:
    def __init__(self, string):
        self.string = string
    
    def __add__(self, other_string_class):
        new_string = self.string + other_string_class.string
        return new_string
    
    def __sub__(self, other_string_class):
        other_string = other_string_class.string

        if len(self.string) > len(other_string):
            return self.string[len(other_string):]

        elif len(self.string) == len(other_string):
            return ''

        else :
            return '-'+other_string[len(self.string):]


one = NewString('Son Myeonghyeon')
two = NewString('Crawdads')
thr = NewString('data_analysis is fun')

print('--수학을 위한 특수 메서드')
print(one + two)
print(one - two)
print(one - thr)
print(one - one)