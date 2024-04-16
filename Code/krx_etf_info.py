import QuantLib as ql
from datetime import datetime
import pandas as pd
from custom_progress import printProgressBar
from utils import time_format
from time import time, sleep
from code_config import data_path, etf_base_path
import xlwings as xw
import matplotlib.pyplot as plt
from pykrx import stock
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.ticker import FuncFormatter

def to_percent(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = str(int(10000 * y)/100)

    # The percent symbol needs escaping in latex
    if matplotlib.rcParams['text.usetex'] is True:
        return s + r'$\%$'
    else:
        return s + '%'

def to_comma(y, position):
    # Ignore the passed in position. This has the effect of scaling the default
    # tick locations.
    s = '{:0,d}'.format(int(y))
    return s

# Create formatters
percent_formatter = FuncFormatter(to_percent)
comma_formatter = FuncFormatter(to_comma)

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

def get_all_etf_info(
        code = "069500",
        fromdate = "20240101",
        todate = "20240405"):
    res1 = get_etf_trade_info(fromdate = fromdate,
                              todate = todate, 
                              code = code)
    
    res1 = res1.div(100000000.)

    res2 = get_etf_historical_data(fromdate = fromdate, 
                                   todate = todate, 
                                   code = code)
    
    res2['괴리'] = res2['종가'] - res2['NAV']
    res2['괴리율'] = res2['괴리'] / res2['NAV']

    res2['거래대금'] = res2['거래대금'] / 100000000.
    res1.rename(columns={'기관': '기관 (순매수)',
                         '기타법인': '기타법인 (순매수)',
                         '개인': '개인 (순매수)',
                         '외국인': '외국인 (순매수)'}, inplace=True)
    
    res = res1.join(res2)
    
    return res[['괴리율', 'NAV', '종가', '거래대금',
                '기관 (순매수)', '기타법인 (순매수)', '개인 (순매수)', '외국인 (순매수)']]

def graph(
        inp,
        field1 = '괴리율',
        field2 = '거래대금',
        period = 'W',
        value_type = 'mean',
        title = ""):
    if value_type == "mean":
        res = inp.resample(period).mean()
    elif value_type == "last":
        res = inp.resample(period).last()
    else:
        raise ValueError(f'value_type: {value_type}')

    fig, axs = plt.subplots(nrows=2, sharex=True)
    fig.suptitle(title)

    # Plot 괴리율 in the first subplot
    if field1 == '괴리율':
        axs[0].yaxis.set_major_formatter(percent_formatter)
    else:
        axs[0].yaxis.set_major_formatter(comma_formatter)

    axs[0].plot(res.index, res[field1], color='blue')
    axs[0].set_ylabel(field1)#, color='blue')
    #axs[0].tick_params(axis='y', labelcolor='blue')
    axs[0].grid(True, linestyle=':', color='gray')  
    
    # Plot 거래대금 in the second subplot
    if field2 == '괴리율':
        axs[1].yaxis.set_major_formatter(percent_formatter)
    else:
        axs[1].yaxis.set_major_formatter(comma_formatter)
    
    axs[1].plot(res.index, res[field2], color='red')
    axs[1].set_ylabel(field2)#, color='red')
    #axs[1].tick_params(axis='y', labelcolor='red')
    axs[1].grid(True, linestyle=':', color='gray')  

    fig.tight_layout()  # Ensure the subplots do not overlap
    plt.show()

def load_and_graph(
        wb = None,
        sheet_name = 'EtfAnalysis',
        output_head = 'F3',
        code = "069500",
        name = "KODEX 200",
        fromdate = "",
        todate = "",
        field1 = '괴리율',
        field2 = '거래대금',
        period = 'W',
        value_type = 'mean',
        ):
    if wb is None:
        wb = xw.Book.caller()
    
    ws = wb.sheets[sheet_name]
    output_head = ws.range(output_head)


    all_info = get_all_etf_info(
        code = code,
        fromdate = fromdate,
        todate = todate,
        )

    if all_info.shape[0] == 0:
        raise ValueError('no data')
    if all_info is None:
        raise ValueError('all_info is None')
    
    title = f'{name} ({code})'

    graph(
        all_info, 
        field1 = field1, field2 = field2,
        period = period, value_type = value_type,
        title = title,
        )

    output_head.options(pd.DataFrame, index = True).value = all_info
                           
