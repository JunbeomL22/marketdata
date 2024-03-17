import matplotlib.pyplot as plt
from datetime import datetime
import QuantLib as ql
import pandas as pd
import numpy as np
import re

trade_history_df = pd.read_json('trade-history.json')
trade_history_df.rename(columns = {'티커': '코드'},
                        inplace = True)

etf_info_df = pd.read_csv('etf_base_info.csv')
df = trade_history_df.merge(etf_info_df,
                            on = '코드',
                            how='inner')
df.rename(columns = {'유형': 'type',
                     '거래대금': 'trade amount',
                     '시가총액': 'market cap'},
          inplace = True)

df['market cap'] = df['market cap'].apply(lambda z: int(re.sub('(조|억|원|,)', '', z) ))
df['date'] = df['date'].apply(lambda z: datetime.strptime(str(int(z)), '%Y%m%d'))
df['qldate'] = df['date'].apply(lambda z: ql.Date.from_date(z))#, '%Y%m%d')
df['trade amount'] = df['trade amount'] / 1000000000000.
df['market cap'] = df['market cap'] / 10000.
                                          
res = df[df['qldate'] > ql.Date(1, 1, 2017)]
res['type'] = res['type'].apply(lambda z: z.split(",")[0])
res_cap = res.groupby(['qldate', 'type'])['market cap'].sum().reset_index()
res_trade_amount = res.groupby(['date', 'type'])['trade amount'].sum().reset_index()

pivoted_trade_amount = res_trade_amount.pivot(index='date', columns = 'type', values = 'trade amount').fillna(0.0)

pivoted_trade_amount.plot(kind='area', stacked=True);plt.show()

#res_trade_amount.plot('date', 'trade amount');plt.show()
plt.rc('font', family='Malgun Gothic')

row = 3
col = 2

fig, axes = plt.subplots(row, col)

qldates = [ql.Date(28, 12, 2018),
           ql.Date(30, 12, 2019),
           ql.Date(30, 12, 2020),
           ql.Date(30, 12, 2021),
           ql.Date(29, 12, 2022),
           ql.Date(30, 11, 2023)]


qldate = ql.Date(30, 11, 2023)


#snapshot = res_cap.set_index('qldate').loc[qldates[0]]
types = res_cap['type'].unique().tolist()
colors = ['yellowgreen', 'gold', 'lightblue', 
          'lightcoral','green', 'gold',
          'pink','magenta', 'violet', 'lightgreen',
          'blue', 'cyan', 'lightskyblue', 'pink'][:len(types)]

color_match = dict(zip(types, colors))
res_cap['color'] = res_cap['type'].replace(color_match)

label_cut_number = 5

for i, qldate in enumerate(qldates):
    snapshot = res_cap.set_index('qldate').loc[qldate]
    
    snapshot.sort_values(by = 'market cap',
                         inplace = True,
                         ascending = False)

    types = snapshot['type'].tolist()
    market_cap = snapshot['market cap'].tolist()
    colors = snapshot['color'].tolist()
    
    lenged_labels = ['{0}: {1:1.1f}%'.format(i,j) for i,j in zip(types, market_cap)]
    labels = ['{0} ({1:1.0f}%)'.format(t, m) if i < label_cut_number else "" for i, (t,m) in enumerate(zip(types, market_cap))]
    explode = [0.05 if '국내채권' in x else 0.0 for x in types]
    #print(i//col, i % col)
    ax = axes[i//col][i % col]
    patches, texts = ax.pie(market_cap,
                            colors = colors,
                            labels = labels,
                            labeldistance = 0.95,
                            textprops={'fontsize': 12},
                            #shadow=True,
                            #fontsize = 0.9,
                            #startangle=90,
                            explode = explode,
                            radius = 0.9)
    
    #plt.legend(patches,
    #           lenged_labels,
    #           loc='lower right',
    #           bbox_to_anchor=(0.1, 0.5),
    #           fontsize=12)

    ax.set_title(f'시가총액 ({qldate.year()}-{qldate.month()}-{qldate.dayOfMonth()})',
                 fontsize = 15,
                 fontweight = 'bold')

plt.tight_layout()
plt.show()
