import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/item/main.nhn?code=000660"
html = requests.get(url).text

soup = BeautifulSoup(html, "lxml")
tags = soup.select("#_per")
tag = tags[0]
print(tag.text)