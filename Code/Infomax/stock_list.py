import sys, json, requests
import code_config
from datetime import datetime
import xlwings as xw
import pandas as pd

def rank_list(wb = None,
              sheet_name = 'List',
              config_range = 'RankConfig',
              output_range = 'G4:U2000'):
    #-
    if wb is None:
        wb = xw.Book.caller()
    ws = wb.sheets[sheet_name]
    config_dict = dict(ws.range(config_range).value)
    date_str = config_dict['date'].strftime('%Y%m%d')

    market = config_dict['market'] if isinstance(config_dict['market'], str) else ''

    type_str = config_dict['type']
    type_str = type_str if isinstance(type_str, str) else ''

    rank_str = config_dict['rank']
    rank_str = rank_str if isinstance(rank_str, str) else ''

    session = requests.Session()
    session.verify = False

    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/rank'


    params = {"market": market,
              "type": type_str,
              "date": date_str,
              "rank": rank_str}

    r = session.get(api_url,
                    params = params,
                    headers = code_config.infomax_headers)

    success, results = r.json().values()

    df = pd.DataFrame(results)
    df['trading_volume'] = df['trading_volume'] / 1000000.
    df['marketcap'] = df['marketcap'] / 100000000.
    df['trading_value'] = df['trading_value'] / 100000000.
    ws.range(output_range).options(pd.DataFrame, index = False).value = df

if __name__ == "__main__":
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
