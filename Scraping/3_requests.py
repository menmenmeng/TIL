import requests
# res = requests.get("http://www.google.com")
res = requests.get("https://beer-up.tistory.com/manage")
res.raise_for_status()
print('응답코드 :', res.status_code)

print(len(res.text))
print(res.text)

# with open("mygoogle.html", "w", encoding="utf8") as f:
#     f.write(res.text)