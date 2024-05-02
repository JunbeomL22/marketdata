from pykrx.website import krx
from infomax_derivatives import get_fut_info, get_underline_match
from custom_progress import printProgressBar
from code_config import jsondb_dir
import pandas as pd
from krx_ktbf_underline import get_ktbf_underline
import xlwings as xw
import os
from time import sleep

def get_derivatives_base_data(
    start_date = '20240423',
    end_date = '20240930',
    drop_spread = True):

    fut_info = get_fut_info(
       kr_name = "",
       underline="",
       spread="N",
       size = 5000,
       )
    
    underline_match = get_underline_match(fut_info)

    ders = krx.future.core.파생상품검색().fetch()
    class_names = ders.index.tolist()

    worker = krx.future.core.전종목기본정보()
    df_list = []
    N = len(class_names)
    for i, name in enumerate(class_names):
        df_list.append(worker.fetch(prodId = name))
        sleep(2)
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

    print("base retrieval completed. Retrieving KTBF underline ISINs...")
    ktbf_list = ["3년국채", "5년국채", "10년국채", "30년국채"]
    for und_name in ktbf_list:
        underline_match = get_ktbf_underline(und_name)
        print(f"retrieved {und_name} underline ISINs. Sleeping 2 seconds...")
        sleep(2)
        mask = (res['und_name'] == und_name)
        for k, v in underline_match.items():
            res.loc[mask & (res['name'].str[-6:] == k), ['und_isin']] = v
    
    return res

def save_derivatives_base_data(
        parameter_date = "20240423",
        start_date = "20240423",
        end_date = "20240930",
        drop_spread = True,
        file_name = "derivatives_base_data.json"):
    # - 
    res = get_derivatives_base_data(
        start_date = start_date,
        end_date = end_date,
        drop_spread = drop_spread
    )
    
    if not os.path.exists(f'{jsondb_dir}/{parameter_date}'):
        os.makedirs(f'{jsondb_dir}/{parameter_date}')
    
    res.to_json(f'{jsondb_dir}/{parameter_date}/{file_name}', orient='records')

def load_derivatives_base_data(
        wb = None,
        parameter_date = "20240423",
        file_name = "derivatives_base_data.json",
        sheet_name = "DerivativesBase",
        output_head = "F15",
        ):
    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    res = pd.read_json(
        f'{jsondb_dir}/{parameter_date}/{file_name}',
        orient='records'
        )

    ws.range(output_head).options(pd.DataFrame, index = False).value = res


if __name__ == "__main__":
    xw.Book("D:/Projects/marketdata/MarketData.xlsm").set_mock_caller()
    save_derivatives_base_data()
    
 

