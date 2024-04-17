from code_config import INFOMAX_HEADER
import requests
import pandas as pd

def bond_otc_trade(
        stdcd: str = "",
        market: str = "",
        startDate: str = "",
        endDate: str = "",
        aclassnm: str = "",
        volume: str = ""):

    session = requests.Session()
    
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/bond/market/mn_hist'

    params = {"stdcd": stdcd,
              "market": market,
              "startDate": startDate,
              "endDate": endDate,
              "aclassnm": aclassnm,
              "volume": volume}

    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    
    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        print("bond_otc_trade() failed")

    return res

def listed_bond_order_real_time(
        stdcd: str = "",
        bonddate: str = ""):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/bond/market/hoga_real'

    params = {"stdcd": stdcd,
              "bonddate": bonddate}
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        print("listed_bond_order() failed")

    return res

def listed_bond_order(
    stdcd: str = "",
    bonddate: str = ""):
    # - 
    session = requests.Session()
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/bond/market/hoga_info'

    params = {"stdcd": stdcd,
              "bonddate": bonddate}
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        print("listed_bond_order() failed")
    
    return res

def listed_bond_trade_real_time(
    stdcd: str = "",
    bonddate: str = ""):
    # - 
    session = requests.Session()
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/bond/market/tick_info'

    params = {"stdcd": stdcd,
              "bonddate": bonddate}
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        print("listed_bond_order() failed")
    
    return res