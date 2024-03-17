import sys, json, requests
import code_config
from datetime import datetime
import xlwings as xw
import pandas as pd
from custom_progress import printProgressBar
from utils import time_format
from time import time
# - 
def save_trade_history(wb = None,
                       sheet_name = 'Save',
                       config_range = 'TradeHistoryConfig'):
    #-
    if wb is None:
        wb = xw.Book.caller()
    ws = wb.sheets[sheet_name]
    config_dict = dict(ws.range(config_range).value)
    
    date_from = datetime.strftime(config_dict['date_from'], '%Y%m%d')
    date_upto = datetime.strftime(config_dict['date_upto'], '%Y%m%d')

    output_file_name = config_dict['output_file_name']
    market = config_dict['market'] if isinstance(config_dict['market'], str) else ''

    type_str = config_dict['type']
    type_str = type_str if isinstance(type_str, str) else ''

    session = requests.Session()
    session.verify = False

    # - 
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/code'
    params = {"search":"","code":"","name":"","isin":"","market": market,"type": type_str}
    r = session.get(api_url,
                    params = params,
                    headers = code_config.infomax_headers)
    success, results = r.json().values()
    _df = pd.DataFrame(results)
    codes = _df['code'].unique().tolist()
    # -
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/hist'
    df_list = []
    N = len(codes)
    st = time()
    for i, code in enumerate(codes):
        params = {"code": code, "endDate": date_upto, "startDate": date_from}

        r = session.get(api_url,
                        params = params,
                        headers = code_config.infomax_headers)

        success, results = r.json().values()

        _df = pd.DataFrame(results)

        
        print(f'there is no data of {code}') if len(_df) == 0 else None
        #_df['trading_volume'] = _df['trading_volume'] / 1000000.
        #_df['trading_value'] = _df['trading_value'] / 100000000.
        printProgressBar(i+1, N, prefix = 'trade history crawling: ',
                         suffix = f'complete (time: {time_format(time() - st)})', length = 20)
        df_list.append(_df)
        #ws.range(output_range).options(pd.DataFrame, index = False).value = df

    df = pd.concat(df_list).reset_index()
    df.to_json(code_config.trade_history_data_path + output_file_name,
               orient='records')

    print('done')
    x = input()
    #return pd.read_json(code_config.trade_history_data_path + output_file_name)

if __name__ == "__main__":
    xw.Book('C:\\Users\\junbe\\Dropbox\\02. Projects\\01. WebCralwer\\Crawler.xlsm').set_mock_caller()
    df = save_history()
