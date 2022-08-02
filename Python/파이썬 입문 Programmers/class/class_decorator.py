def add(x, y):
    print('Calling add') # 비슷한 구문
    return x + y

def sub(x, y):
    print('Calling sub') # 비슷한 구문
    return x - y

# logging을 위해 비슷한 모양의 print 함수가 반복해서 나타난다. 이와 비슷한 많은 함수를 짜야 함.
# 매번 print문을 조금씩 수정해서 다 복붙해야 되고, 비슷한 함수를 계속해서 짤 필요성이 있음
# 귀찮은 일을 계속해서 해야 한다. 이런 반복 작업을 간단하게 만들 수 있는 방법이 바로 데코레이터

# 먼저 함수에 logging을 추가해 주는 함수, logged를 만든다.
def logged(func):
    def wrapper(*args, **kwargs):  # func(*args, **kwargs)는 parameter의 어떠한 조합도 받을 수 있다.
        print('Calling', func.__name__)
        return func(*args, **kwargs)
    return wrapper

# 이게 뭘 하는 함수인가? 원래 함수를 대입하면, wrapper 함수를 내놓는다.
# logged 함수 내에서 wrapper라는 logging함수를 생성해서, 이를 리턴함.
# wrapper는 자신이 해야 할 것은 하고, 원래 함수 func를 호출.

def add(x, y):
    return x + y

logged_add = logged(add)  # wrapper 함수를 만든다. logged_add(parameter)와 같이 사용해야 하는 것.
k = logged_add(3, 4)
print(k)

# 위의 과정이 파이썬에서는 매우 흔하기 때문에 전용 구문이 있다.

@logged
def add(x, y):
    return x + y
# ==
# def add(x, y):
#     return x + y
# add = logged(add)

m = add(5, 4)
print(m)


# 빌트인 데코레이터(데코레이트된 메서드)

# @staticmethod # : function을 정적 클래스 메서드로 바꾼다. 이게 무슨 뜻?


class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    @classmethod
    def fromTuple(cls, tup):
        return cls(tup[0], tup[1])

    @classmethod
    def fromDictionary(cls, dic):
        return cls(dic["email"], dic["password"])


# 1. User 정의 그대로
user1 = User('aaaa@gmail.com', 'aaa111')

# 2. fromTuple 메소드를 이용
user2_tup = ('bbbb@naver.com', 'bbb222')
user2 = User.fromTuple(user2_tup)

# 3. fromDictionary 메소드를 이용
user3_dict = {'name':'C', 'email':'cccc@hanmail.net', 'password':'ccc333'}
user3 = User.fromDictionary(user3_dict)

print(user1.email, user1.password)
print(user2.email, user2.password)
print(user3.email, user3.password)