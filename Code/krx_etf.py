import requests
import pandas as pd
from custom_progress import printProgressBar
from time import time, sleep
from code_config import jsondb_dir

def get_krx_etf_price(
        dt = '20240509',):
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
    params = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT04301',
        'locale': 'ko_KR',
        'trdDd': dt,
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false',
    }
    response = requests.post(
        url, 
        verify = False,
        params = params, )
    
    df = pd.DataFrame(response.json()['output'])

    return df

def get_krx_etf_base():
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    params = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT04601',
        'locale': 'ko_KR',
        'share': '1',
        'csvxls_isNo': 'false',
    }

    response = requests.post(
        url,
        verify = False,
        params = params,)
    
    df = pd.DataFrame(response.json()['output'])

    return df

def get_krx_etf_pdf(
        isin = 'KR7069500007',
        code = '069500',
        name = 'KODEX 200',
        dt = '20240509',):
    url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'

    params = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT05001',
        'locale': 'ko_KR',
        'tboxisuCd_finder_secuprodisu1_1': f'{code}/{name}',
        'isuCd': isin,
        'isuCd2': code,
        'codeNmisuCd_finder_secuprodisu1_1': name,
        'param1isuCd_finder_secuprodisu1_1': '',
        'trdDd': dt,
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false',
    }

    response = requests.post(
        url,
        verify = False,
        params = params,)
    
    output = response.json()['output']

    if len(output) > 0:
        df = pd.DataFrame(output)
        return df
    else:
        print(f'No data found for {name} ({code})')
        return None

