import requests
# res = requests.get("http://www.google.com")
url = "https://beer-up.tistory.com/manage"
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}
res = requests.get(url, headers=headers)
res.raise_for_status()
print('응답코드 :', res.status_code)

print(len(res.text))
print(res.text)

with open("mytistory.html", "w", encoding="utf8") as f:
    f.write(res.text)