from code_config import data_path, INFOMAX_HEADER, INFOMAX_TOKEN
import sys, json, requests
import pandas as pd
import xlwings as xw

def find_etf_include(code, date):
    session = requests.Session()
    # SSL 인증 처리 무효화
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf/search'

    params = {'code': code,
              'date': date}

    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = pd.DataFrame(results)
    return res

def load_etf_include(wb = None,
                     sheet_name = 'FindETF',
                     output_head = 'F3',
                     code = 'KR350101GCB1',
                     date = '20240405'):
    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    output_head = ws.range(output_head)
    res = find_etf_include(code, date)
    
    output_head.options(pd.DataFrame, index = False).value = res


if __name__ == '__main__':
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    load_etf_include()
        
