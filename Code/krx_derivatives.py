from pykrx.website import krx
from infomax_derivatives import get_fut_past_info, get_underline_match
from utils import time_format
from custom_progress import printProgressBar
from code_config import data_path
import pandas as pd
from krx_ktbf_underline import get_ktbf_underline
import xlwings as xw

def get_derivatives_base_data(
    start_date = '20240423',
    end_date = '20240930',
    drop_spread = True):

    past_fut = get_fut_past_info(
        endDate = end_date, 
        startDate = start_date, 
        drop_spread = drop_spread
        )
    
    underline_match = get_underline_match(past_fut)

    ders = krx.future.core.파생상품검색().fetch()
    class_names = ders.index.tolist()

    worker = krx.future.core.전종목기본정보()
    df_list = []
    N = len(class_names)
    for i, name in enumerate(class_names):
        df_list.append(worker.fetch(prodId = name))
        printProgressBar(i, N, prefix = 'Progress:', suffix = 'Complete', length = 20)

    res = pd.concat(df_list)

    res = res[~res['ISU_SRT_CD'].str.startswith('4')]

    res.drop(columns=['ISU_ABBRV', 'ISU_ENG_NM', 'ULY_TP_NM'], inplace=True)
    res.LIST_DD = res.LIST_DD.str.replace('/', '')
    res.LSTTRD_DD = res.LSTTRD_DD.str.replace('/', '')
    res.LST_SETL_DD = res.LST_SETL_DD.str.replace('/', '')
    res = res[res.LSTTRD_DD <= end_date]
    res['krx_und_code'] = res['ISU_SRT_CD'].str[1:3]
    res = res.merge(underline_match, on='krx_und_code', how='left')

    res.rename(
        columns = {
            "ISU_CD": "isin",
            "ISU_SRT_CD": "code",
            "ISU_NM": "name",
            "LIST_DD": "listing_date",
            "LSTTRD_DD": "maturity",
            "LST_SETL_DD": "settlement_date",
            "SETLMULT": "unit_notional",
            "RGHT_TP_NM": "option_type",
            "EXER_PRC": "exercise_price",
        },
        inplace = True
    )

    ktbf_list = ["3년국채", "5년국채", "10년국채", "30년국채"]
    for und_name in ktbf_list:
        underline_match = get_ktbf_underline(und_name)
        mask = (res['und_name'] == und_name)
        for k, v in underline_match.items():
            res.loc[mask & (res['name'].str[-6:] == k), ['und_isin']] = v

    return res

def save_base_derivatives_data(
        start_date = "20240423",
        end_date = "20240930",
        drop_spread = True,
        cache_type = "overwrite",
        file_name = "derivatives_base_data.json"):
    # - 
    res = get_derivatives_base_data(
        start_date = start_date,
        end_date = end_date,
        drop_spread = drop_spread
    )
    
    if cache_type == "overwrite":
        res.to_json(f'{data_path}/{file_name}', orient='records')
    elif cache_type == "append":
        previous_data = pd.read_json(f'{data_path}/{file_name}', orient='records')
        res = pd.concat([previous_data, res]).drop_duplicates(subset='isin')


def load_base_derivatives_data(
        wb = None,
        file_name = "derivatives_base_data.json",
        sheet_name = "DerivativesBase",
        output_head = "F15",
        ):
    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    res = pd.read_json(f'{data_path}/{file_name}', orient='records')

    ws.range(output_head).options(pd.DataFrame, index = False).value = res

    
xw.Book("D:/Projects/marketdata/MarketData.xlsm").set_mock_caller()
load_base_derivatives_data()