import matplotlib.pyplot as plt
from datetime import datetime
import pandas as pd
#def graph_krx_etf_number():
df = pd.read_json('krx_ticker_history.json')
df['all etf number'] = df['tickers'].apply(lambda z: len(z.split(",")) if z != '' else 0)
df['date'] = df['date_str'].apply(lambda z: datetime.strptime(str(z), '%Y%m%d'))
df = df.sort_values(by = 'date')
df['issuance'] = df['all etf number'].diff().fillna(method='bfill').astype(int)

trade_history_df = pd.read_json('trade-history.json')
trade_history_df.rename(columns = {'티커': '코드'},
                        inplace = True)

etf_info_df = pd.read_csv('etf_base_info.csv')
trade_history_df = trade_history_df.merge(etf_info_df,
                                          on = '코드',
                                          how='inner')
trade_history_df.rename(columns = {'유형': 'type',
                                   '코드': 'ticker',
                                   '거래대금': 'trade amount',
                                   '시가총액': 'market cap'},
                        inplace = True)
trade_history_df['date'] = trade_history_df['date'].apply(lambda z: datetime.strptime(str(z), '%Y%m%d'))

name_match = pd.read_json('ticker_name_match.json')
trade_history_df['name'] = trade_history_df['ticker'].replace(dict(zip(name_match['ticker'], name_match['name'])))
trade_history_df[['date', 'trade amount']].groupby('date').sum().plot()
df['all etf number'].plot();plt.show()
#plt.show()
