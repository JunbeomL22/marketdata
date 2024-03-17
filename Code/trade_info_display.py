import xlwings as xw
from config import data_path, trade_history_data_path
from time import time
from custom_progress import printProgressBar
from utils import time_format
import xlwings  as xw
from datetime import datetime
import os
import pandas as pd

xw.Book('C:\\Users\\junbe\\Dropbox\\02. Projects\\01. WebCralwer\\Crawler.xlsm').set_mock_caller()
wb = None
if wb is None:
    wb = xw.Book.caller()
sheet_name = 'TradeAnalysis'
config_range = 'TradeAnalysisConfig'
ws = wb.sheets[sheet_name]

config_dict = dict(ws.range(config_range).value)
date_from = datetime.strftime(config_dict['date_from'], '%Y%m%d')
date_upto = datetime.strftime(config_dict['date_upto'], '%Y%m%d')

path_to_json = trade_history_data_path

json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

df_list = []
for json_file in json_files:
    x = json_file.split("-")

    if (x[-1].split(".")[0] >= date_from) and (date_upto >= x[-2]):
        _df = pd.read_json(trade_history_data_path + json_file, dtype = False)
        df_list.append(_df)

res = pd.concat(df_list)
res = res[res.date.between(date_from, date_upto)]
res.drop_duplicates(['date', 'ticker'], inplace=True)

res['price-index'] = res[['NAV', 'close']].mean(axis=1)
my_portion = config_dict['my_expected_trade_portion']
tick_size = config_dict['tick_size']

res['expected pnl'] = my_portion * res['trade unit'] * (tick_size / 3.)


df1 = res[['ticker', 'expected pnl', 'trade amount', 'trade unit']].groupby('ticker').sum().reset_index()
df2 = res[['ticker', 'price-index']].groupby('ticker').mean().reset_index()
#-
df = df1.merge(df2, on='ticker', how = 'inner')

#-
df['trade amount (억)'] = df['trade amount'] / 100000000.
df['expected pnl (백만)'] = df['expected pnl'] / 1000000.
df['trade unit (백만)'] = df['trade unit'] / 1000000.
df.sort_values('expected pnl', inplace = True, ascending = False)
df = df.reset_index()
df['rank'] = df.index.values+1

base_info_df = pd.read_csv(data_path + config_dict['base_info_file'])
name_match_df = pd.read_json(data_path + config_dict['name_match_file'], dtype = False)

def patching(z):
    N = len(str(z))
    zero_patch = ''.join(['0' for _ in range(max(6-N, 0))])
    return zero_patch + str(z)
base_info_df['ticker'] = base_info_df['ticker'].apply(patching)
name_match_df['ticker'] = name_match_df['ticker'].apply(patching)        

#df = df.merge(name_match_df, on='ticker', how='left')
#df = df.merge(name_match_df, on='ticker', how='left')
df['issuer'] = df['ticker'].replace(dict(zip(base_info_df['ticker'], base_info_df['issuer'])))
df['name'] = df['ticker'].replace(dict(zip(name_match_df['ticker'], name_match_df['name'])))
df['type'] = df['ticker'].replace(dict(zip(base_info_df['ticker'], base_info_df['type'])))

display_res = df.head(int(config_dict['top_list_number']))[['rank',
                                                            'ticker',
                                                            'name',
                                                            'expected pnl (백만)',
                                                            'type',
                                                            'issuer',
                                                            'price-index',
                                                            'trade unit (백만)',
                                                            'trade amount (억)'
                                                            ]]
ws.range('F3:M2000').clear_contents()
ws.range('F3').options(pd.DataFrame, index=False).value = display_res
