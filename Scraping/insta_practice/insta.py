from urllib.request import urlopen
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By # find_element_by_XXX() 가 아니라. 이걸 사용
import time

loginUrl = 'https://www.instagram.com/accounts/login/'
baseUrl = 'https://www.instagram.com/explore/tags/'
plusUrl = input('검색할 태그 입력 : ')
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome()
driver.get(loginUrl)

time.sleep(0.5)
driver.find_element(By.NAME, 'username').send_keys('men_men_meng')
time.sleep(0.5)
driver.find_element(By.NAME, 'password').send_keys('IamYourEnergy49!')
time.sleep(0.5)
driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]/button').click()
time.sleep(2)

driver.get(url)
time.sleep(3)

import datetime

start = datetime.datetime.now()
end = start + datetime.timedelta(seconds=5) # 5초 동안 scroll 내려줌

while True :
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(0.5)
    if datetime.datetime.now() > end:
        break

'''
for _ in range(3):
    driver.execute_script('window.scrollTo(0, document.body.scorllHeight);')
    time.sleep(1.5)
'''

html = driver.page_source
soup = BeautifulSoup(html, 'lxml')

insta = soup.select('.v1Nh3.kIKUG._bz0w')

# 클래스 따로, 태그 따로, 속성 따로.
# div class = XXXX , a href = XXXX 이런식일 때
# class 자체가 select의 기준이 될 수 있고.
# div, a 라는 tag가 하나의 기준이 될 수 있고. (soup.div, soup.a 등으로 판별)
# href, name 이라는 속성이 하나의 기준이 될 수 있다. (i.a['href']처럼 키 값 같은 느낌으로)

n = 1
for i in insta:
    time.sleep(0.1)
    print('https://www.instagram.com' + i.a['href'])
    imgUrl = i.img['src']
    with urlopen(imgUrl) as f:
        with open('./img/' + plusUrl + str(n) + '.jpg', 'wb') as h:
            img = f.read()
            h.write(img)
    n += 1
    print(imgUrl)
    # 왜 21개 img만 다운로드 되는가? = 우리가 스크롤 밑으로 내리기 이전에 표시되는 사진 개수가 21개
    # 더 많이 img 다운로드 하고 싶다면, selenium에서 스크롤 기능이 있으니까 그걸 사용해도 됨.

time.sleep(1)
driver.close()