class UnexpectedRSPValue(Exception):
    '''가위 바위 보 가운데 하나가 아닌 경우에 발생하는 에러'''

class BadUserName(Exception):
    '''유저 이름이 이상할 때 발생하는 에러'''
    
class PasswordNotMatched(Exception):
    '''패스워드가 일치하지 않을 때 발생하는 에러'''