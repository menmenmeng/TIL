from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time

# Library 설명
## urllib.parse.quote_plus
### url에 한글이 포함될 때, 한글을 유니코드로 변환하고 urlencoding해야 한다. 이 과정을
### 간단하게 처리해주는 기능. quote_plus('한글') 과 같이 사용하면 됨.

## selenium.webdriver
### 일반적으로 javascript가 포함된 웹페이지들
### beautifulsoup 하나만으로는 자바스크립트를 읽어들일 수 없다. -> selenium webdriver 사용


# 예시 URL
# https://www.instagram.com/explore/tags/%EC%95%84%EC%9D%B4%EC%9C%A0/

baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input('검색할 태그 입력 : ')
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome()
driver.get(url)
# 여기까지, 원하는 태그를 입력하고 + 그 url을 가져오는 것까지 가능.

# driver get 하는 것과, page source를 가져오는 것 사이에 time을 가져다 놓으면 좋다.
# driver가 url을 get하는 시간이 오래 걸림. 그래서 driver가 아직 다 로드되지 않았는데
# html로 읽어들이게 될 수가 있는 듯. selenium은 보통 이렇게 한다고 함. 다음 페이지 넘어가기 전까지
# 기다리는 과정.

time.sleep(3)

html = driver.page_source # 현재 driver의 페이지 소스를 가져와서 html에 담는다.
soup = BeautifulSoup(html)

# 태그는 programmer로 해 보겠습니다.

insta = soup.select('.v1Nh3.kIKUG._bz0w') # v1Nh3 kIKUG _bz0w 가 class. 근데 이건 html 문법이고
# 공백을 전부 .으로 바꿔 줘야 한다
# soup 안에서 찾는거죠? soup.select 해야 함

# print(insta[0])

# 여기서 src 태그...? src 클래스를 가져와야 한다.

n = 1
for i in insta:
    # 게시물의 원 주소, 게시물의 이미지를 가져오겠다.
    print('https://www.instagram.com' + i.a['href'])
    imgUrl = i.select('.KL4Bh').img['src']
    # 여기서 urlopen 사용
    with urlopen(imgUrl) as f:
        with open('./img/' + plusUrl + str(n) + '.jpg', 'wb') as h:
            img = f.read()
            h.write(img)
    n += 1
    print(imgUrl)

driver.close()