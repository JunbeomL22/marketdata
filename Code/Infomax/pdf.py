import sys, json, requests
import xlwings as xw

session = requests.Session()
# SSL 인증 처리 무효화
session.verify = False
api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf/port'

params = {"code":"448310","date":"20231215","sort":""}

r = session.get(api_url, params = params, headers = headers)

msg, results = r.json().values()

if __name__ == "__main__":
    xw.Book('D:/Prodjcts/WebCrawler/Crawler.xlsm').set_mock_caller()


