from pykrx import stock, bond
import QuantLib as ql
from datetime import datetime
import pandas as pd
from custom_progress import printProgressBar
from utils import time_format
from time import time, sleep
from code_config import data_path
import xlwings as xw
import matplotlib.pyplot as plt

def get_krx_etf_ticker(date):
    tickers = stock.get_etf_ticker_list(date)

    return tickers

def get_krx_etf_ticker_history(date_from = '20230601',
                               date_upto = '20231207'):
    """
    return dict(string => csv style dates)
    """
    dt_string_list = [d.strftime('%Y%m%d') for d in pd.date_range(date_from, date_upto)]

    N = len(dt_string_list)
    st = time()
    res = {}
    for i, dt_str in enumerate(dt_string_list):
        tickers = get_krx_etf_ticker(dt_str)
        
        res[dt_str] = ",".join(set(tickers))
        printProgressBar(i+1, N, prefix = 'ticker history crawling: ',
                         suffix = f'complete (time: {time_format(time() - st)})', length = 20)
        
    return res

def get_krx_all_etf_cum_issue_history(date_from = '20230601',
                                      date_upto = '20231207'):
    """
    return csv style dates
    """
    # - 
    x = get_krx_etf_ticker_history(date_from = date_from,
                                   date_upto = date_upto)
    
    res = set()

    for dt, tickers in x.items():
        res.update(tickers.split(","))

    return res
    
def save_krx_etf_trade_history(wb = None,
                               sheet_name = 'Main',
                               config_range = 'TradeConfig'):

    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    save_config = dict(ws.range(config_range).value)
    date_from = datetime.strftime(save_config['date_from'], '%Y%m%d')
    date_upto = datetime.strftime(save_config['date_upto'], '%Y%m%d')
    freq = save_config['freq']
    output_file_name = save_config['output_file_name']
        
    cal = ql.SouthKorea()
    dt_range = pd.date_range(date_from,
                             date_upto,
                             freq = freq)

    date_str_list = []
    for dt in dt_range:
        dt = cal.adjust(ql.Date.from_date(dt), ql.Preceding)
        date_str_list.append(dt.to_date().strftime('%Y%m%d'))
        
    df_list = []
    N = len(date_str_list)
    st = time()
    
    for i, date_str in enumerate(date_str_list):
        if (i % 50 == 0) and (i !=0):
            print('resting...')
            sleep(30.0)
        _df = stock.get_etf_ohlcv_by_ticker(date_str)
        _df.reset_index(inplace=True)
        _df['date'] = date_str
        if len(_df) == 0:
            print(f'there is no data on {date_str}')
        else:
            df_list.append(_df)
        printProgressBar(i+1, N, prefix = 'trade history crawling: ',
                         suffix = f'complete (time: {time_format(time() - st)})', length = 20)

    ed = time()

    res = pd.concat(df_list)
    res.rename(columns = {'티커': 'ticker',
                          '거래량': 'trade unit',
                          '거래대금': 'trade amount',
                          '시가': 'open',
                          '저가': 'low',
                          '고가': 'high',
                          '종가': 'close'},
               inplace = True)

    res.drop_duplicates(['ticker', 'date'], inplace=True)
    def patching(z):
        N = len(str(z))
        zero_patch = ''.join(['0' for _ in range(max(6-N, 0))])
        return zero_patch + str(z)

    if len(res) > 0:
        res['ticker'] = res['ticker'].apply(patching)
    
    res.reset_index().to_json(data_path + 'TradeHistory\\' + output_file_name)

    print(f'elapsed time: {time_format(ed-st)}')
    print(f'please enter to exit')
    x = input()


def get_etf_trade_info(fromdate = "20230101",
                       todate = "20240405",
                       amount_type = "거래대금",
                       trade_type = "순매수",
                       code = None):
    
    if isinstance(code, str) and (len(code) != 6):
        raise ValueError("code must be a string of length 6 (e.g., '069500') or None")
        
    if code is None:
        res = stock.get_etf_trading_volume_and_value(fromdate,
                                                    todate,
                                                    amount_type,
                                                    trade_type)
    else:
        res = stock.get_etf_trading_volume_and_value(fromdate,
                                                    todate,
                                                    code,
                                                    amount_type,
                                                    trade_type
                                                    )
    
    return res

def get_etf_historical_data(fromdate = "20230101",
                            todate = "20240405",
                            code = "069500"):
    if isinstance(code, str) and (len(code) != 6):
        raise ValueError("code must be a string of length 6 (e.g., '069500') or None")
    
    res = stock.get_etf_ohlcv_by_date(fromdate, todate, code)
    
    return res

def get_all_etf_info(fromdate = "20240101",
                     todate = "20240405",
                     code = "069500"):
    res1 = get_etf_trade_info(fromdate = fromdate,
                              todate = todate, 
                              code = code)
    
    res1 = res1.div(100000000.)

    res2 = get_etf_historical_data(fromdate = fromdate, 
                                   todate = todate, 
                                   code = code)
    
    res2['괴리'] = res2['종가'] - res2['NAV']
    res2['괴리율'] = res2['괴리'] / res2['NAV']

    res = res1.join(res2)

    return res[['괴리율', 'NAV', '종가', '기관', '기타법인', '개인', '외국인']]

if __name__ == "__main__":
    #res = stock.get_etf_trading_volume_and_value("20230101", "20240405", "069500", "거래대금", "순매수")
    res = get_all_etf_info(todate = '20240411')
    #res = get_etf_trade_info()
    

    