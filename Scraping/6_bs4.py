import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")  # res.text : html 문서, lxml : 파서.
# 우리가 가져온 html문서를 lxml 파서를 통해서 BeautifulSoup 객체로 만든 것이다.
# soup이라는 녀석이 모든 정보를 다 가지고 있다.

# print(soup.title) # title 태그
# print(soup.title.get_text()) # title 태그의 text 부분만
# print(soup.a) # a 태그. 모든 html문서 중 첫 번째로 발견되는 a 태그를 가져다 달라.
# print(soup.a.attrs) # 처음으로 발견되는 a 태그의 attrs, 즉 속성들을 다 가져다 달라.(dict 반환)
# print(soup.a["href"]) # 속성 중 href 속성"값"정보를 프린트
# 근데 여기까지는 페이지에 대한 이해가 충분할 때. 잘 알고 있을 때 사용할 수 있는 것
# 잘 모를 때 쓸 수 있는 게 find.

# print(soup.find('a', attrs={"class":"Nbtn_upload"})) # class = Nbtn_upload인 a element를 찾아줘
# print(soup.find(attrs={"class":"Nbtn_upload"})) # class = Nbtn_upload인 어떤 element를 찾아줘

# print(soup.find('li', attrs={"class":"rank01"})) # class=rank01인 li태그 내용물 전부
rank1 = soup.find('li', attrs={"class":"rank01"}) # soup.find 한 게 다시 BS객체가 된다.
# print(rank1.a)


## 참고 :: soup 객체의 type
# print(type(soup))
# print(type(soup.a))
# print(type(soup.a['href']))
# print(type(rank1))
## result
# <class 'bs4.BeautifulSoup'>
# <class 'bs4.element.Tag'>
# <class 'str'>
# <class 'bs4.element.Tag'>
# BeautifulSoup 객체랑 element.Tag 객체랑, 같은 용도로 쓰일 수 있음. find를 사용하든 태그를 찾든

# 형제 사이를 왔다갔다 하기 : next_sibling, previous_sibling
# print(rank1.a.get_text())
# rank2 = rank1.next_sibling.next_sibling # 형제 사이에 개행부호 같은 게 있으면 두개 해주면 됨
# rank3 = rank2.next_sibling.next_sibling
# print(rank3.a.get_text())
# rank2 = rank3.previous_sibling.previous_sibling
# print(rank2.a.get_text())
# 형제 사이를 태그 조건을 줘서 왔다갔다 하기 : find_next_sibling("tag"), find_previous_sibling("tag")
# rank2 = rank1.find_next_sibling("li") # rank1 다음 sibling중에 li 태그만 가져온다.
# print(rank2.a.get_text())
# rank3 = rank2.find_next_sibling("li")
# print(rank3.a.get_text())
# rank2 = rank3.find_previous_sibling("li")
# print(rank2.a.get_text())

# 부모자식 사이 왔다갔다 하기 : 
# print(rank1.parent)

# 한 번에 모든 형제들 찾기 : find_next_siblings("tag") : s가 붙습니다
# print(rank1.find_next_siblings("li")) # rank 1 기준으로 다음 sibling들을 찾는다.

webtoon = soup.find("a", text="1초-154화 팀 대항 구조작전 (1)") # text가 저거고 element가 a인 것
print(webtoon)