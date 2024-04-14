from code_config import INFOMAX_HEADER
import requests
import pandas as pd

def get_fut_past_info(kr_name = "", 
                     type_name = "", 
                     underline = "", 
                     endDate = "", 
                     startDate = ""):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/future/expired'

    params = {"kr_name": kr_name,
              "type": type_name,
              "underline": underline,
              "endDate": endDate,
              "startDate": startDate
              }

    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception(f'infomax future crawling failed\n\
                        get_fut_info\n\
                        {kr_name}\n\
                        {type_name}\n\
                        {underline}\n\
                        {endDate}\n\
                        {startDate}\n\
                        {api_url}\n\
                        {params}')
    
    return res

def get_fut_underline(type_name = "C",
                      name = "",
                      code = ""):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/future/underline'

    params = {"type": type_name,
              "name": name,
              "code": code
              }
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    res = pd.DataFrame(results)

    return res

def get_fut_base_info(codes="", date = "20240405"):
    api_url = 'https://infomaxy.einfomax.co.kr/api/future/info'

    params = {"code": codes,
              "date": date
              }
    
    r = requests.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception(f'infomax future crawling failed\n\
                        get_fut_base_info\n\
                        {codes}\n\
                        {date}\n\
                        {api_url}\n\
                        {params}')
    
    return res

    
    