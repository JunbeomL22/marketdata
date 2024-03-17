import sys, json, requests
import pandas as pd
# - 
# -
def get_infomax_etf_info(codes,
                         TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJFMjEwMzc0IiwiY291cG9uVHlwZSI6ImFwaSIsInN2YyI6ImluZm9tYXgiLCJpYXQiOjE3MDE5MjM1NTUsImV4cCI6MjY0ODAwMzU1NX0.4Hfd4LRerv3KaQ8Dygd7Lflv_FL2JrhvBcPRnwHBilg'):
    session = requests.Session()
    # SSL 인증 처리 무효화
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf'

    params = {"code": ",".join(codes)}
    headers = {"Authorization" : f'bearer {TOKEN}'}
    r = session.get(api_url, params = params, headers = headers)
    success, results = r.json().values()

    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception('infomax crawling failed')
    

def get_infomax_etf_pdf(codes,
                        date,
                        TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJFMjEwMzc0IiwiY291cG9uVHlwZSI6ImFwaSIsInN2YyI6ImluZm9tYXgiLCJpYXQiOjE3MDE5MjM1NTUsImV4cCI6MjY0ODAwMzU1NX0.4Hfd4LRerv3KaQ8Dygd7Lflv_FL2JrhvBcPRnwHBilg'):
    session = requests.Session()
    # SSL 인증 처리 무효화
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf/port'
    
    params = {"code": ",".join(codes),
              "date": date,
              "sort": ""}
    
    headers = {"Authorization" : f'bearer {TOKEN}'}
    r = session.get(api_url, params = params, headers = headers)

    success, results = r.json().values()
    
    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception('infomax crawling failed')




    
