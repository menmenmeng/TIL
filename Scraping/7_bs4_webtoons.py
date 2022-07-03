import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")  # res.text : html 문서, lxml : 파서.

# 네이버 웹툰 전체 목록 가져오기
cartoons = soup.find_all("a", attrs={"class":"title"}) # 조건에 해당하는 모든 element
# class 속성이 title인 모든 a element 반환
for cartoon in cartoons:
    print(cartoon.get_text())

