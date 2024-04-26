import sys, json, requests
from code_config import INFOMAX_HEADER
import time
import pandas as pd

def get_stock_tick(code = "000660", date = ""):
    st = time.time()
    session = requests.Session()
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/tick'

    params = {"code": code, "date": date}
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    res = pd.DataFrame(results)
    print(f"get_stock_trade: {code} {time.time() - st:.2f}")
    return res

def get_equity_daily(
        code = "000660", 
        start_date = "",
        end_date = "",):
    session = requests.Session()
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/hist'

    params = {
        "code": code, 
        "startDate": start_date,
        "endDate": end_date,
    }

    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise ValueError(f"get_equity_daily: {code}")
    
    return res

def get_equity_base(
        codes = "000660", 
        date = "20240425",):
    session = requests.Session()
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/info'

    if isinstance(codes, str):
        codes = codes.split(',')
    params = {
        "code": codes, 
        "date": date,
    }

    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise ValueError(f"get_equity_daily: {codes}")
    
    return res