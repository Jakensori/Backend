from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl
import json

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://happybean.naver.com/rdona-service/rdona/rdonaboxes?begin=1&end=19&order=rcmd_ymdt&sortType=desc&lgCatNo=3&supportNo=16&_=1676368998771"
req = Request(url)
response = urlopen(req)
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html5lib')
#soup = BeautifulSoup(html, 'html.parser')
print("모금함 개수", json.loads(soup.text)['result']['totalCount'])
print("모금함 정보 목록", json.loads(soup.text)['result']['rdonaBoxes'])




## parser.py
# import requests
# from bs4 import BeautifulSoup
# import json
# import os

# ## python파일의 위치
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# req = requests.get("https://happybean.naver.com/donation/DonateHomeMain#theme=3")
# html = req.text
# soup = BeautifulSoup(html, 'html.parser')
# urls = soup.select(
#     'div.wrap > #content > #rdonaboxes > a'
#     )

# data = {}

# for title in urls:
#     data[title.text] = title.get('href')

# with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
#     json.dump(data, json_file)