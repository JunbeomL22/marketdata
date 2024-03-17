import xlwings as xw
import pandas as pd
import config
import re
from datetime import datetime

def load_base_info(wb = None, 
                   sheet_name = 'BaseInfo',
                   file_name = 'ticker_name_match.json',
                   etf_info_file_name = 'etf_base_info.csv',
                   output_range = 'G3:H5000'):
    # -    
    if wb is None:
        wb = xw.Book.caller()
    
    df = pd.read_json(config.data_path + file_name)
    info_df = pd.read_csv(config.data_path + etf_info_file_name)
    res = df.merge(info_df, on='ticker', how='left')

    def notional_parser(z):
        if not isinstance(z, str):
            return z
        elif bool(re.match('^[1-9].*원$', z)):
            return int(re.sub('(조|억|원|,)', '', z) )
        else:
            return z
    
    res['market cap'] = res['market cap'].apply(notional_parser)

    def ter_parser(z):
        if not isinstance(z, str):
            return z
        elif bool(re.match('^연.*%$', z)):
            return 0.01*float(re.sub('(%|연)', '', z) )
        else:
            return z
    
    res['ter'] = res['ter'].apply(ter_parser)

    def issue_date_parser(z):
        if not isinstance(z, str):
            return z
        elif bool(re.match('^[1-9].*일$', z)):
            return datetime.strptime(z, '%Y년 %m월 %d일')
        else:
            return z
    
    res['issue date'] = res['issue date'].apply(issue_date_parser)
    
    ws = wb.sheets[sheet_name]

    ws.range(output_range).clear_contents()

    res.drop_duplicates('ticker', inplace=True)
    res.sort_values(by='ticker', inplace=True, ascending=False)
    res['ticker'] = res['ticker'].apply(lambda z: f'0{z}' if len(str(z)) == 5 else str(z))
    ws.range(output_range).options(pd.DataFrame, index = False).value = res

xw.Book('C:\\Users\\junbe\\Dropbox\\02. Projects\\01. WebCralwer\\Crawler.xlsm').set_mock_caller()
wb = None
if wb is None:
    wb = xw.Book.caller()
sheet_name = 'TradeInfo'
config_range = 'TradeInfoConfig'
ws = wb

if __name__ == "__main__":
    xw.Book('C:\\Users\\junbe\\Dropbox\\02. Projects\\01. WebCralwer\\Crawler.xlsm').set_mock_caller()
    load_base_info()    
