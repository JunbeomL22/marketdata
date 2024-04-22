from pykrx.website import krx
from infomax_derivatives import get_fut_past_info, get_underline_match
import pandas as pd

start_date = '20240401'
end_date = '20250401'
drop_spread = True

past_fut = get_fut_past_info(endDate = end_date, startDate = start_date, drop_spread = drop_spread)
underline_match = get_underline_match(past_fut)

ders = krx.future.core.파생상품검색().fetch()
class_names = ders.index.tolist()

worker = krx.future.core.전종목기본정보()
df_list = []
for name in class_names:
    df_list.append(worker.fetch(prodId = name))

res = pd.concat(df_list)

res = res[~res['ISU_SRT_CD'].str.startswith('4')]

res.drop(columns=['ISU_ABBRV', 'ISU_ENG_NM', 'ULY_TP_NM'], inplace=True)
res.LIST_DD = res.LIST_DD.str.replace('/', '')
res.LSTTRD_DD = res.LSTTRD_DD.str.replace('/', '')
res.LST_SETL_DD = res.LST_SETL_DD.str.replace('/', '')
res = res[res.LSTTRD_DD > end_date]
res['krx_und_code'] = res['ISU_SRT_CD'].str[1:3]

res = res.merge(underline_match, on='krx_und_code', how='left')