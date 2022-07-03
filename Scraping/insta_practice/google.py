from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

baseUrl = 'https://www.google.com/search?q='
plusUrl = input('무엇을 검색할까요? : ')
url = baseUrl + quote_plus(plusUrl)

driver = webdriver.Chrome()
driver.get(url)

time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html)

googleLinks = soup.select('.yuRUbf') # class='yURUbf' 인 파트를 가져온다.

for source in googleLinks:
    pageUrl = source.a['href']
    print(pageUrl)
    pageTitle = source.select_one('.LC20lb.MBeuO.DKV0Md').text # tag에 싸여 있는 text 가져오기.
    print(pageTitle)

driver.close()