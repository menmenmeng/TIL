import requests
from bs4 import BeautifulSoup

def get_per(code):
    url = "https://finance.naver.com/item/main.nhn?code="+code
    html = requests.get(url).text

    soup = BeautifulSoup(html, "lxml")
    tags = soup.select("#_per")
    tag = tags[0]
    return float(tag.text)

def get_dividend(code): # 배당
    url = "https://finance.naver.com/item/main.nhn?code="+code
    html = requests.get(url).text

    soup = BeautifulSoup(html, "lxml")
    tags = soup.select("#_dvr")
    tag = tags[0]
    return float(tag.text)

print(get_per("000660"))
print(get_dividend("000660"))