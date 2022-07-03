import pandas as pd
import requests
from bs4 import BeautifulSoup

url = "https://finance.naver.com/item/sise_day.nhn?code=066570"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, "lxml")
table = soup.select("table")
table_df = pd.read_html(str(table))
print(table_df[0].dropna(axis=0))