from code_config import data_path, INFOMAX_HEADER
import sys, json, requests
import pandas as pd

def get_daily_nav(code = '069500',
                  start_date = '20170101',
                  end_date = '20240405'):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf/hist'

    params = {'code': code,
              'startDate': start_date,
              'endDate': end_date}

    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values() 

    if not success:
        raise Exception('Failed to get daily NAV')
    else:
        res = pd.DataFrame(results)
        return res
    
def get_intra_inav(code,
                   date=''):
    session = requests.Session()
    
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf/intra'

    params = {'code': code,
              'date': date}
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    if not success:
        raise Exception('Failed to get intra INAV')
    else:
        res = pd.DataFrame(results)
        return res
    