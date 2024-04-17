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
