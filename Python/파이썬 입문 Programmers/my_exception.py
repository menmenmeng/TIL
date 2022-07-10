from UnexpectedRSPValue import UnexpectedRSPValue, BadUserName, PasswordNotMatched
value = '가'
try:
    if value not in ['가위', '바위', '보']:
        raise UnexpectedRSPValue

except UnexpectedRSPValue:
    print("에러 발생했습니다.")

# ValueError는 굉장히 흔한 에러다. 즉, ValueError가 일어나도 이게 어디서 일어난 건지 모를 수 있다는 것.


def sign_up(name):
    print(name)
    '''회원가입 함수'''

# 여러 에러를 분기로 나눠서 처리 가능하다.
try:
    name = '바보'
    sign_up(name)
    if name in ['바보', '병신']:
        raise BadUserName('너무하잖어')
except BadUserName:
    print("이름으로 사용할 수 없는 입력입니다.")
except PasswordNotMatched:
    print("입력한 패스워드가 서로 일치하지 않습니다.")

