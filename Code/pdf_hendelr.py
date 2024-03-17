import xlwings as xw
import pandas as pd
import config
import re
from datetime import datetime
from time import time
import sys, json, requests
from custom_progress import printProgressBar
from utils import time_format
import urllib3;urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

xw.Book('C:\\Users\\junbe\\Dropbox\\02. Projects\\01. WebCralwer\\Crawler.xlsm').set_mock_caller()
wb = None
match_file_name = 'ticker_name_match.json'
#etf_info_file_name = 'etf_base_info.csv'
match_df = pd.read_json(config.data_path + match_file_name,
                        dtype = False)
sheet_name = 'PDF'
tickers = match_df['ticker'].unique().tolist()
date_str = '20231214'
if wb is None:
    wb = xw.Book.caller()
#output_range = 'G3:H5000'):
# -

#if wb is None:
#    wb = xw.Book.caller()
    
#df = pd.read_json(config.data_path + file_name)

session = requests.Session()
session.verify = False
api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf/port'
headers = {"Authorization" : f'bearer {config.infomax_api_token}'}

st = time()
df_list = []
N = len(tickers)

for i, ticker in enumerate(tickers):
    ticker = f'0{ticker}' if len(str(ticker)) == 5 else str(ticker)
    r = session.get(api_url,
                    params = {"code": ticker,
                              "date": date_str,
                              "sort": ""},
                    headers = headers)
    printProgressBar(i+1,
                     N,
                     prefix = 'etf-pdf crawling: ',
                     suffix = f'complete (time: {time_format(time() - st)})', length = 20)
    success, results = r.json().values()

    df = pd.DataFrame(results)
    df_list.append(df)

res = pd.concat(df_list)
res['ticker'] = res['code']

wb.sheets[sheet_name].range('A1').options(pd.DataFrame, index=False).value = res

if __name__ == "__main__":
    xw.Book('C:\\Users\\junbe\\Dropbox\\02. Projects\\01. WebCralwer\\Crawler.xlsm').set_mock_caller()
    load_base_info()    
