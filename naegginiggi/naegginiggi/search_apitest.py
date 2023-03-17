from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import ssl
import json
import os

###### 사용자가 기부 모금함 리스트 업데이트 버튼 누를 시,
###### result.json 파일 초기화하고 search_apitest.py 파일 실행 !!

## python파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ssl._create_default_https_context = ssl._create_unverified_context
url = "https://happybean.naver.com/rdona-service/rdona/rdonaboxes?begin=1&end=19&order=rcmd_ymdt&sortType=desc&lgCatNo=3&supportNo=16&_=1676368998771"
req = Request(url)
response = urlopen(req)
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')

data = json.loads(soup.text)['result']['rdonaBoxes'] # 리스트 안에 json 형태로 모금함 개수만큼 저장됨

with open(os.path.join(BASE_DIR, 'result.json'), 'w+') as json_file:
    json.dump(data, json_file)

# print("모금함 개수", json.loads(soup.text)['result']['totalCount'])
# print("모금함 정보 목록", json.loads(soup.text)['result']['rdonaBoxes'])