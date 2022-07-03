import re

p = re.compile("ca.e")

def print_match(m):
    if m:
        print("m.group():", m.group()) # 일치하는 문자열 반환
        print("m.string:", m.string) # 입력받은 문자열
        print("m.start():", m.start()) # 일치하는 문자열의 시작 인덱스
        print("m.end():", m.end()) # 일치하는 문자열의 끝 인덱스
        print("m.span():", m.span()) # 일치하는 문자열의 시작, 끝 인덱스
    else:
        print("Not matched")

m = p.match("careless") # 주어진 문자열의 처음부터 일치하는지 확인
print_match(m)

m = p.search("careless") # 주어진 문자열 중에 일치하는 게 있는지 확인. 한 개 
print_match(m)
m = p.search("good care")
print_match(m)

m = p.findall("good care cafe") # findall : 일치하는 모든 것을 리스트 형태로 반환
print(m)
# findall은 그냥 리스트 형태로 반환한다. 따라서 m.group(), m.string... 등 사용 불가

# 1. p = re.compile("원하는 정규식")
# 2. m = p.match("비교할 문자열") (또는 search, findall)
#
# 정규식 문법 : .(한개 문자), ^(시작), $(끝)
# w3schools.com에서 내려서 Learn python - Python RegEx
# 또는 python re 검색해서 docs에서 확인할 수 있음.