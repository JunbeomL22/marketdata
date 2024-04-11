from code_config import data_path
from time import time, sleep
from krx_etf_info import get_krx_etf_ticker_history, get_krx_all_etf_cum_issue_history
from naver_etf_info import _save_naver_attached_data
from infomax_base_data import get_etf_info
import pandas as pd
from pykrx import stock, bond
from custom_progress import printProgressBar
from utils import time_format
import xlwings  as xw

def save_naver_attached_data(wb = None,
                             sheet_name = 'Save',
                             config_range = 'NaverAttachedConfig'):

    if wb is None:
        wb = xw.Book.caller()
        
    ws = wb.sheets[sheet_name]
    config = dict(ws.range(config_range).value)

    base_file_name = config['etf base info']
    use_prev_data = not bool(config['refresh'])
    output_file = config['output file']
    waiting_time = float(config['waiting time'])
    crawl_iter = int(config['crawl iter'])
    
    base_info = pd.read_json(data_path + base_file_name, dtype = 'object')
    codes = base_info.code.astype(str).unique().tolist()

    if use_prev_data:
        prev_output = pd.read_csv(data_path + output_file)
        prev_codes_to_skip = prev_output['code'].astype(str).tolist()
    else:
        prev_codes_to_skip = []

    codes = list(set(codes))
    st = time()

    for i, pt in enumerate(prev_codes_to_skip):
            N = len(str(pt))
            zero_patch = ''.join(['0' for _ in range(max(6-N, 0))])
            prev_codes_to_skip[i] = zero_patch + pt

    _save_naver_attached_data(base_info = base_info,
                             use_prev_data = use_prev_data,
                             prev_list_to_skip = prev_codes_to_skip)
    
    for i in range(1, crawl_iter):
        print("waiting to restart.....")
        sleep(waiting_time)
        prev_output = pd.read_csv(data_path + output_file)
        prev_codes_to_skip = prev_output['code'].astype(str).tolist()

        for i, pt in enumerate(prev_codes_to_skip):
            N = len(str(pt))
            zero_patch = ''.join(['0' for _ in range(max(6-N, 0))])
            prev_codes_to_skip[i] = zero_patch + pt
                    
    _save_naver_attached_data(base_info = base_info,
                             use_prev_data = True,
                             prev_list_to_skip = prev_codes_to_skip)

    res = pd.read_csv(data_path + output_file)
    res.drop_duplicates('code', inplace=True)
    res.to_csv(data_path + output_file, index = False)
    print(f'elapsed time: {time_format(time() - st, 1)}')
    print('please enter to exit')
    x = input()

def cache_base_data(date_from = '20100101',
                    date_upto = '20240405',
                    output_file_name = 'base_info.json'
                    ):        
    all_tickers = get_krx_all_etf_cum_issue_history(date_from = date_from,
                                                    date_upto = date_upto)
    
    res = get_etf_info(list(all_tickers))

    res.to_json(data_path + output_file_name)

if __name__ == "__main__":
    xw.Book("D:/Projects/marketdata/MarketData.xlsm").set_mock_caller()
    save_naver_attached_data()
    cache_base_data()

