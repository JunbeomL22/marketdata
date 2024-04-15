from code_config import data_path, INFOMAX_HEADER, etf_base_path
import sys, json, requests
import pandas as pd
import xlwings as xw

def find_etf_include(codes = "KR350101GCB1", 
                     condition = "and",
                     date = "20240405",
                     base_file = "etf_base_info.json",
                     pdf_file = "etf_pdf_20240405.json"
                     ):
    session = requests.Session()
    # SSL 인증 처리 무효화
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf/search'

    codes = codes.split('/')
    df_list = []
    for code in codes:
        params = {'code': code,
                  'date': date}

        r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

        success, results = r.json().values()

        df = pd.DataFrame(results)
        df_list.append(df)

    if len(df_list) == 0:
        return None
    
    all_df = pd.concat(df_list)
    res = None
    res_list = []
    if condition == 'and':
        etfs = all_df.etf_isin.unique().tolist()
        for etf in etfs:
            etf_df = all_df[all_df['etf_isin'] == etf]
            search_isins = etf_df.search_isin.unique().tolist()
            search_codes = etf_df.search_code.unique().tolist()
            include = True
            
            for code in codes:
                if not ((code in search_codes) or (code in search_isins)):
                    include = False
                    break

            if include:
                res_list.append(etf_df)
        if len(res_list) != 0:
            res = pd.concat(res_list)
            
    elif condition == 'or':
        res = all_df
    else:
        raise ValueError(f'condition: {condition}')

    if res is not None:
        if base_file != "":
            base = pd.read_json(etf_base_path + base_file, dtype = False)
            res = res.merge(base[['isin', 'kr_name', 'net_asset']], left_on='etf_isin', right_on='isin', how='left')
            res.drop(columns = ['search_code', 'isin'], inplace = True)
            res['net_asset'] = res['net_asset'].astype(float) / 100000000.
        if pdf_file != "":
            pdf = pd.read_json(data_path + pdf_file, dtype = False)
            res = res.merge(pdf[['isin', 'port_isin', 'port_portion']], left_on=['etf_isin', 'search_isin'], right_on=['isin', 'port_isin'], how='left')
            res.drop(columns = ['isin', 'port_isin'], inplace = True)

    return res

def load_etf_include(wb = None,
                     sheet_name = 'FindETF',
                     codes = '247540/086520/005490/383310',
                     condition = 'and',
                     date = '20240405',
                     base_file = 'etf_base_info.json',
                     pdf_file = 'etf_pdf_20240405.json',
                     output_head = 'H3'):
    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    output_head = ws.range(output_head)

    res = find_etf_include(codes = codes, 
                           date = date,
                           condition = condition, 
                           base_file = base_file, 
                           pdf_file = pdf_file)
    
    output_head.options(pd.DataFrame, index = False).value = res


if __name__ == '__main__':
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    res = find_etf_include(codes = "247540/086520/005490/383310", condition = 'and', date = '20240405')