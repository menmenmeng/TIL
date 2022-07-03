from selenium import webdriver
path = 'C:/Users/frank/Downloads/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(path)

# idle에서 사용해야 하는 듯
driver.get('https://www.google.com')

assert 'Google' in driver.title
assert 'Naver' in driver.title

driver.find_element()
elem = driver.find_element_by_name('q')

elem.clear()

elem.send_keys("Selenium")

elem.submit()
assert "No results found." not in driver.page_source