from config import data_path
from time import time, sleep
from krx_etf_info import get_krx_etf_ticker_history, get_krx_all_etf_cum_issue_history
from naver_etf_info import save_naver_finance_etf_info
import pandas as pd
from pykrx import stock, bond
from custom_progress import printProgressBar
from utils import time_format
import xlwings  as xw

def save_etf_info_naverfinance(wb = None,
                               sheet_name = 'Main',
                               config_range = 'BaseInfoConfig'):

    if wb is None:
        wb = xw.Book.caller()
        
    ws = wb.sheets[sheet_name]
    config = dict(ws.range(config_range).value)

    ticker_file_name = config['ticker_file_name']
    use_prev_data = not bool(config['refresh'])
    prev_file = config['prev_file']
    waiting_time = float(config['waiting_time'])
    crawl_iter = int(config['crawl_iter'])
    
    df = pd.read_json(data_path + ticker_file_name, dtype = 'object')

    tickers = df.ticker.astype(str).unique().tolist()
    if use_prev_data:
        prev_output = pd.read_csv(data_path + prev_file)
        #prev_output.rename(columns={'코드': 'ticker'}, inplace=True)    
        prev_tickers_to_skip = prev_output['ticker'].astype(str).tolist()
    else:
        prev_tickers_to_skip = []

    tickers = list(set(tickers))
    
    #input_tickers = [f'0{ticker}' if len(str(ticker)) == 5 else str(ticker) for ticker in tickers]

    st = time()

    save_naver_finance_etf_info(tickers = tickers,
                                use_prev_data = use_prev_data,
                                prev_list_to_skip = prev_tickers_to_skip)
    
    for i in range(1, crawl_iter):
        print("waiting to restart.....")
        sleep(waiting_time)
        prev_output = pd.read_csv(data_path + prev_file)

        #prev_output.rename(columns={'코드': 'ticker'}, inplace=True)
    
        prev_tickers_to_skip = prev_output['ticker'].astype(str).tolist()

        for i, pt in enumerate(prev_tickers_to_skip):
            N = len(str(pt))
            zero_patch = ''.join(['0' for _ in range(max(6-N, 0))])
            prev_tickers_to_skip[i] = zero_patch + pt
                    
        save_naver_finance_etf_info(tickers = tickers,
                                    use_prev_data = True,
                                    prev_list_to_skip = prev_tickers_to_skip)

    res = pd.read_csv(data_path + prev_file)
    res.drop_duplicates('ticker', inplace=True)
    res.to_csv(data_path + prev_file, index = False)
    print(f'elapsed time: {time_format(time() - st, 1)}')
    print('please enter to exit')
    
    x = input()

def save_ticker_history_json(date_from = '20230101',
                             date_upto = '20231207',
                             output_file_name = 'krx_ticker_history.json',
                             refresh = False
                             ):

    ticker_history = get_krx_etf_ticker_history(date_from = date_from,
                                                date_upto = date_upto)

    res_dict = {'date_str': list(ticker_history.keys()),
                'tickers': list(ticker_history.values())}

    if not refresh:
        prev_df = pd.read_json(data_path + output_file_name, dtype = False)
        prev_df['ticker'] = prev_df['ticker'].astype(str)
        res = prev_df.merge(res, on=['ticker', 'name'], how='left')
    res = pd.DataFrame(res_dict)
    
    def patching(z):
        N = len(str(z))
        zero_patch = ''.join(['0' for _ in range(max(6-N, 0))])
        return zero_patch + str(z)
        
    res['ticker'] = res['ticker'].apply(patching)
    res.to_json(config.data_path + output_file_name)


def save_ticker_name_match_json(date_from = '20020101',
                                date_upto = '20231207',
                                output_file_name = 'ticker_name_match.json',
                                refresh = False):
    # -
        
    all_tickers = get_krx_all_etf_cum_issue_history(date_from = date_from,
                                                    date_upto = date_upto)
    names = []
    tickers = []
    N = len(list(all_tickers))
    st = time()
    for i, ticker in enumerate(list(all_tickers)):
        if ticker == '':
            continue
        # I decided to have the original data
        #if len(str(ticker)) == 5:
        #    ticker = f'0{ticker}'
        name = stock.get_etf_ticker_name(ticker)
        tickers.append(ticker)
        names.append(name)
        printProgressBar(i+1, N, prefix = 'etf name crawling: ',
                         suffix = f'complete (time: {time_format(time() - st)})', length = 20)

    res = pd.DataFrame({'ticker': tickers,
                        'name': names})

    if not refresh:
        prev_df = pd.read_json(data_path + output_file_name, dtype = False)
        prev_df['ticker'] = prev_df['ticker'].astype(str)
        res = prev_df.merge(res, on=['ticker', 'name'], how='left')

    def patching(z):
        sz = str(z)
        N = len(sz)
        zero_patch = ''.join(['0' for _ in range(max(6-N, 0))])
        return zero_patch + sz
        
    res['ticker'] = res['ticker'].apply(patching)
    res.to_json(data_path + output_file_name)

if __name__ == "__main__":
    xw.Book("D:\\Projects\\WebCrawler\\Crawler.xlsm").set_mock_caller()
    save_etf_info_naverfinance()
