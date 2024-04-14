import xlwings as xw
import pandas as pd
import code_config
import re
from datetime import datetime
from time import time
import sys, json, requests
from custom_progress import printProgressBar
from utils import time_format
import urllib3;urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_etf_pdf(
        wb = None,
        sheet_name = 'EtfPdf',
        output_range_name = 'EtfPdf',
        date_cell = 'C4',
        match_file_name_cell = 'C5'):                    
    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    date_str = str(ws.range(date_cell).value)
    match_file_name = str(ws.range(match_file_name_cell).value)
    
    output_range = ws.range(output_range_name)
    output_range.clear_contents()

    match_df = pd.read_json(code_config.etf_base_path + match_file_name, dtype = False)

    tickers = match_df['code'].unique().tolist()

    session = requests.Session()
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf/port'

    st = time()
    df_list = []
    N = len(tickers)

    for i, ticker in enumerate(tickers):
        ticker = f'0{ticker}' if len(str(ticker)) == 5 else str(ticker)
        r = session.get(api_url,
                        params = {"code": ticker,
                                "date": date_str,
                                "sort": ""},
                        headers = code_config.INFOMAX_HEADER)
        printProgressBar(i+1,
                        N,
                        prefix = 'etf-pdf crawling: ',
                        suffix = f'complete (time: {time_format(time() - st)})', length = 20)
        success, results = r.json().values()

        df = pd.DataFrame(results)
        df_list.append(df)

    res = pd.concat(df_list)
    res.drop(columns = ['admin_number'], inplace = True)
    res['port_portion'] = res['port_value'] / res['etf_value']

    wb.sheets[sheet_name].range(output_range).options(pd.DataFrame, index=False).value = res

if __name__ == "__main__":
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    load_etf_pdf()    
