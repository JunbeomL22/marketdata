import matplotlib.pyplot as plt
from datetime import datetime
import QuantLib as ql
import pandas as pd
import numpy as np
import re

name_match = pd.read_json('ticker_name_match.json')
trade_history_df = pd.read_json('trade-history.json')
trade_history_df.rename(columns = {'티커': '코드'}, inplace = True)

etf_info_df = pd.read_csv('etf_base_info.csv')
df = trade_history_df.merge(etf_info_df, on = '코드', how='inner')
df.rename(columns = {'유형': 'type', '거래대금': 'trade amount', '시가총액': 'market cap'}, inplace = True)

df['market cap'] = df['market cap'].apply(lambda z: int(re.sub('(조|억|원|,)', '', z) ))
df['date'] = df['date'].apply(lambda z: datetime.strptime(str(int(z)), '%Y%m%d'))

df['qldate'] = df['date'].apply(lambda z: ql.Date.from_date(z), '%Y%m%d')
df['trade amount'] = df['trade amount'] / 1000000000000.
df['market cap'] = df['market cap'] / 10000.
df['name'] = df['코드'].replace(dict(zip(name_match['ticker'], name_match['name'])))
df['issue date'] = df['코드'].replace(dict(zip(etf_info_df['코드'], etf_info_df['상장일'])))


res = df[df['qldate'] == ql.Date(31, 10, 2023)].sort_values(by = 'trade amount')
res['type'] = res['type'].apply(lambda z: z.split(",")[0])
res[['name', 'type', 'issue date', 'trade amount']].tail(20)

res = df[df['qldate'] > ql.Date(1, 1, 2008)]
res['type'] = res['type'].apply(lambda z: z.split(",")[0])
res_cap = res.groupby(['date', 'type'])['market cap'].sum().reset_index()
res_trade_amount = res.groupby(['qldate', 'type'])['trade amount'].sum().reset_index()

plt.rc('font', family='Malgun Gothic')

res_trade_amount.pivot(index='qldate', columns = 'type', values = 'trade amount').plot(kind='area', stacked=True);plt.show()
res_cap.pivot(index='date', columns = 'type', values = 'market cap').plot(kind='area', stacked=True);plt.show()

snapshot = res_cap.set_index('date').loc[np.datetime64('2023-11-30T00:00:00.000000000')]
