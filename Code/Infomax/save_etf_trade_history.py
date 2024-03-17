import sys, json, requests
from config import infomax_api_token
# -
session = requests.Session()
# SSL 인증 처리 무효화
session.verify = False
api_url = 'https://infomaxy.einfomax.co.kr/api/stock/hist'

params = {"code": "448310",
          "startDate": "19950101",
          "endDate": "20231215"}
headers = {"Authorization" : f'bearer {infomax_api_token}'}

r = session.get(api_url, params = params, headers = headers)
success, results = r.json().values()

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
    
if __name__ == "__main__":
    xw.Book('C:\\Users\\junbe\\Dropbox\\02. Projects\\01. WebCralwer\\Crawler.xlsm').set_mock_caller()
    save_etf_trade_history()    
