import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/list?titleId=675554"
res = requests.get(url)
res.raise_for_status()

soup = BeautifulSoup(res.text, "lxml")  # res.text : html 문서, lxml : 파서.
cartoons = soup.find_all("td", attrs={"class":"title"})
# title = cartoons[0].a.get_text()
# link = cartoons[0].a["href"]
# print(title, ',', "https://comic.naver.com" + link)

# 만화 제목과 링크 가져오기
for cartoon in cartoons:
    title = cartoon.a.get_text()
    link = "https://comic.naver.com" + cartoon.a["href"]
    # 여기부터 score
    score = cartoon.find_next_sibling("td").div.strong.get_text()
    print(title, ',', link)
    print('score:', score)


# 평균 평점 계산하기
total_rates = 0
ratings = soup.find_all("div", attrs={"class":"rating_type"})
for rating in ratings:
    score = rating.find("strong").get_text()
    print(score)
    total_rates += float(score)
print("Total:", total_rates)
print("Average:", total_rates/len(ratings))


## @@ 좋은 팁 : 인터프리팅 방식으로 하는 게 웹 스크래이핑에 더 좋을 수 있습니다.
# 터미널에서 python을 치면 인터프리터가 나옵니다.
# beatifulsoup 구글에 쳐서 공식문서 -> 한국어 번역