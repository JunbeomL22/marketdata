import sys, json, requests
import pandas as pd
from code_config import INFOMAX_TOKEN, INFOMAX_HEADER
# - 
# -
def get_etf_info(codes):
    session = requests.Session()
    
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf'

    params = {"code": ",".join(codes)}
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)
    success, results = r.json().values()

    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception('infomax crawling failed')

    return res    

def get_etf_pdf(codes, date):
    session = requests.Session()
    # SSL 인증 처리 무효화
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf/port'
    
    params = {"code": ",".join(codes),
              "date": date,
              "sort": ""}
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    
    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception('infomax crawling failed')
    
    return res

def get_index_list(type_code = ''):
    """
    (K:코스피, Q: 코스닥, X: KRX, F: 선물/옵션, G: Global&other, T: 일반상품&etc. M: 멀티에셋, N: 코넥스)
    """
    session = requests.Session()
    # SSL 인증 처리 무효화
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/index/code'
    
    params = {"type": type_code,
              "kr_name":"",
              "en_name":"",
              "code":""}
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)
    
    success, results = r.json().values()
    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception(f'infomax index crawling failed\n\
                        get_index_list\n\
                        {type_code}\n\
                        {api_url}\n\
                        {params}')
    return res

def get_index_pdf(code = ''):
    session = requests.Session()
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/index/constituents'

    params = {"code": code}

    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception(f'infomax index crawling failed\n\
                        get_index_pdf\n\
                        {code}\n\
                        {api_url}\n\
                        {params}')
    return res

def get_bond_info(isin_codes):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/bond/basic_info'

    df_list = []
    for code in isin_codes:
        params = {"stdcd": code}
        r = session.get(api_url, params = params, headers = INFOMAX_HEADER)
        success, results = r.json().values()
        
        if success:
            df_list.append(pd.DataFrame(results))
    
    res = pd.concat(df_list)

    return res

def get_security_base_info(search = "",
                            code = "",
                            name = "",
                            isin = "",
                            market = "",
                            type_name = ""):
    
    session = requests.Session()
    
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/code'

    params = {"search": search,
                "code": code,
                "name": name,
                "isin": isin,
                "market": market,
                "type": type_name}
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception('infomax crawling failed')
    
    return res


if __name__ == '__main__':
    res = get_index_list(type_code = '')
    




    
