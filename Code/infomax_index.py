from code_config import INFOMAX_HEADER
import json, requests
import pandas as pd
import xlwings as xw

def get_index_list(type_name = "", kr_name = "", en_name = "", code = ""):
    session = requests.Session()
    # SSL 인증 처리 무효화
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/index/code'

    params = {"type": type_name,
              "kr_name": kr_name,
              "en_name": en_name,
              "code": code}

    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = pd.DataFrame(results)
    return res

def get_index_base_info(code = "", date = "20240405"):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/index/info'

    params = {"code": code,
              "date": date}
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)
    success, results = r.json().values()

    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise ValueError(f"index_base_data: {code}")
    
    return res

def get_index_pdf(codes):
    session = requests.Session()
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/index/constituents'

    df_list = []
    for code in codes:
        params = {"code": code}

        r = session.get(api_url, params = params, headers = INFOMAX_HEADER)
        success, results = r.json().values()
        if success:
            df = pd.DataFrame(results)
            df_list.append(df)
        else:
            print(f'Error: {code}')

    res = pd.concat(df_list)
    return res

def load_index_list(wb = None,
                    sheet_name = 'IndexData',
                    output_head = 'E4',
                    type_name = '',
                    kr_name = '',
                    en_name = '',
                    code = ''):
    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    output_head = ws.range(output_head)
    res = get_index_list(type_name, kr_name, en_name, code)
    res.drop(columns = ['en_name'], inplace = True)
    
    output_head.options(pd.DataFrame, index = False).value = res

def load_index_pdf(wb = None,
                   sheet_name = 'IndexData',
                   codes = "K2G01P/Q5G01P",
                   output_head = 'N4'):
    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    output_head = ws.range(output_head)
    res = get_index_pdf(codes.split('/'))

    res['code'] = res['isin'].apply(lambda x: "'"+x[3:9])

    output_head.options(pd.DataFrame, index = False).value = res[['isin', 'code', 'kr_name']]


if __name__ == '__main__':
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    load_index_pdf()
    load_index_list()
