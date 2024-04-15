import xlwings as xw
import pandas as pd
from code_config import data_path, etf_base_path, INFOMAX_HEADER
import time
import requests
from custom_progress import printProgressBar
from utils import time_format
import urllib3;urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_etf_pdf(
        wb = None,
        sheet_name = 'EtfPdf',
        output_range_name = 'EtfPdf',
        date_cell = 'C4',
        base_info_file_cell = 'C5',
        pdf_file_cell = 'C6',
        source_cell = 'C7'):
    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    date_str = str(ws.range(date_cell).value)
    base_info_file = str(ws.range(base_info_file_cell).value)
    pdf_file = str(ws.range(pdf_file_cell).value)
    source = str(ws.range(source_cell).value)
    
    output_range = ws.range(output_range_name)
    output_range.clear_contents()

    if source == "Json":
        res = pd.read_json(data_path + pdf_file)
        res['code'] = res['code'].astype(str)
        # make code 6 digit by attaching zeros in the head
        def attaching_zeros(x):
            if len(x) == 6:
                return x
            elif len(x) < 6:
                n = 6 - len(x)
                return '0'*n + x
            else:
                raise ValueError(f"code length is greater than 6: {x}")
        res['code'] = res['code'].apply(attaching_zeros)
        wb.sheets[sheet_name].range(output_range).options(pd.DataFrame, index=False).value = res
        return 
        
    match_df = pd.read_json(etf_base_path + base_info_file, dtype = False)

    tickers = match_df['code'].unique().tolist()

    session = requests.Session()
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf/port'

    st = time.time()
    df_list = []
    N = len(tickers)

    for i, ticker in enumerate(tickers):
        ticker = f'0{ticker}' if len(str(ticker)) == 5 else str(ticker)
        r = session.get(api_url,
                        params = {"code": ticker,
                                "date": date_str,
                                "sort": ""},
                        headers = INFOMAX_HEADER)
        printProgressBar(i+1,
                        N,
                        prefix = 'etf-pdf crawling: ',
                        suffix = f'complete (time: {time_format(time.time() - st)})', length = 20)
        success, results = r.json().values()

        df = pd.DataFrame(results)
        df_list.append(df)

    res = pd.concat(df_list)
    res.drop(columns = ['admin_number'], inplace = True)
    res['port_portion'] = res['port_value'] / res['etf_value']

    wb.sheets[sheet_name].range(output_range).options(pd.DataFrame, index=False).value = res

def save_etf_pdf(
        base_info_file = 'etf_base_info.json',
        pdf_file = 'etf_pdf.json'):
    base_info = pd.read_json(etf_base_path + base_info_file, dtype = False)
    tickers = base_info['code'].unique().tolist()

    session = requests.Session()
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf/port'

    st = time.time()
    df_list = []
    N = len(tickers)

    for i, ticker in enumerate(tickers):
        ticker = f'0{ticker}' if len(str(ticker)) == 5 else str(ticker)
        r = session.get(api_url,
                        params = {"code": ticker,
                                "date": "20240405",
                                "sort": ""},
                        headers = INFOMAX_HEADER)
        printProgressBar(i+1,
                        N,
                        prefix = 'etf-pdf crawling: ',
                        suffix = f'complete (time: {time_format(time.time() - st)})', length = 20)
        success, results = r.json().values()

        df = pd.DataFrame(results)
        df_list.append(df)

    res = pd.concat(df_list)
    res.drop(columns = ['admin_number'], inplace = True)
    res['port_portion'] = res['port_value'] / res['etf_value']

    res.reset_index(drop = True, inplace = True)

    res.to_json(data_path + pdf_file)

if __name__ == "__main__":
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    save_etf_pdf()    
