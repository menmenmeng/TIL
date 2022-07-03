# daum.net - 검색창에 "영화" 검색
# 각 연도마다 역대 관객 순위 Top 5의 영화 포스터들을 자동으로 다운받기

import requests
from bs4 import BeautifulSoup

years = range(2021, 2010, -1)

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

for year in years:
    url = f"https://search.daum.net/search?w=tot&q={year}%EB%85%84%EC%98%81%ED%99%94%EC%88%9C%EC%9C%84&DA=MOR&rtmaxcoll=MOR"
    res = requests.get(url, headers=headers)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    images = soup.find_all("img", attrs={"class":"thumb_img"})

    for idx, img in enumerate(images):
        image_url = img['src']
        if image_url.startswith('//'):
            image_url = "https:" + image_url
        
        print(image_url)
        image_res = requests.get(image_url)
        image_res.raise_for_status()

        with open(f"movie_{year}_{idx+1}.jpg", "wb") as f:
            f.write(image_res.content)

        if idx >= 4: # 상위 5개만 다운로드
            break