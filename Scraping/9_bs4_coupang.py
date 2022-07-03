## HTTP Method: get, post
# GET : URL에 적어서 보내는 방식
# POST : HTTP Body에 적어서 보내는 방식
# URL 뒤에 물음표 뒤에부터 적혀져 나오는 값들은 GET으로 하는 것. URL을 자유롭게 변경하면서 쉽게쉽게.
# GET은 데이터가 양이 크면 안됨, 비밀스러운 값이 아님.
# 아이디, 패스워드 입력해서 URL에 보내면 안됨. 쉽게 노출됨, 이런 건 POST 방식으로 숨겨서 보낸다.
# POST는 데이터 크기 제한이 없음.
# GET 방식은 URL만 조작해서 쉽게 스크레이핑 가능, POST는 페이지 변화는 있는데 URL변화는 없는 경우.
# 쿠팡은 GET방식이라 쉽게 Scraping가능.

import requests
import re
from bs4 import BeautifulSoup

page_number = 1
url = f"https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page={page_number}&rocketAll=false&searchIndexingToken=&backgroundColor="
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

items = soup.find_all("li", attrs={"class":re.compile("^search-product")}) # re를 쓰는 법.
print(items[0].find("div", attrs={"class":"name"}).get_text())
for item in items:
    # 광고 제품은 제외
    ad_badge = item.find("span", attrs={"class":"ad-badge-text"})
    if ad_badge:
        print("<광고 상품 제외>")
        continue

    # 이름, 가격 정보, 평점, 리뷰 수
    name = item.find("div", attrs={"class":"name"}).get_text()

    # 애플 제품 제외
    if re.match("^Apple", name):
        print("<Apple 상품 제외>")
        continue

    price = item.find("strong", attrs={"class":"price-value"}).get_text()

    # 리뷰 100개 이상, 평점 4.5 이상 되는 것만 조회하기
    rating_star = item.find("div", attrs={"class":"rating-star"})
    if rating_star:
        rate = rating_star.em.get_text()
        rate_cnt = rating_star.find("span", attrs={"class":"rating-total-count"}).get_text()
        rate_cnt = rate_cnt[1:-1]
    else:
        print("<평점, 리뷰 없는 상품 제외>")
        continue
        rate = "No Data"
        rate_cnt = "No Data"
    if float(rate) >= 4.5 and int(rate_cnt) >= 100:
        print("\t <상품>", name)
        print("\t---- <가격>", price, ', <평점>', rate, ', <리뷰 수>', rate_cnt)
    else:
        print("<기준 충족 못 하는 상품 제외>")
