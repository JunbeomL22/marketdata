from infomax_derivatives import get_infomax_underline_identifier
from code_config import jsondb_dir
import pandas as pd
import os
import xlwings as xw

def save_infomax_underline_identifier(
        parameter_date = "20240513",
        retrieval_date = "20240514",
        file_name = "infomax_underline_identifier.json",
        ):
    print("Saving infomax_underline_identifier...")
    res = get_infomax_underline_identifier()
    res.insert(0, "parameter_date", parameter_date)
    res.insert(1, "retrieve_date", retrieval_date)
    
    if not os.path.exists(jsondb_dir): os.makedirs(jsondb_dir)
    res.to_json(f"{jsondb_dir}/{parameter_date}/{file_name}", orient = "records")

def load_infomax_underline_identifier(
        wb = None,
        sheet_name = 'Derivatives',
        parameter_date = "20240513",
        output_head = 'B17',
        file_name = "infomax_underline_identifier.json",
        ):
    print("Loading infomax_underline_identifier...")
    if wb is None:
        wb = xw.Book.caller()
    ws = wb.sheets[sheet_name]

    res = pd.read_json(f"{jsondb_dir}/{parameter_date}/{file_name}", orient = "records")
    res.drop(columns = ["parameter_date"], inplace = True)
    res['krx_und_code'] = res['krx_und_code'].astype(str).str.zfill(2)
    def attach_zero(x):
        und_type, und_code = x
        if und_type == 'L':
            N = max(6-len(und_code), 0)
            return f"{N*'0'}{und_code}"
        else:
            return und_code

    res['und_code'] = res[['und_type', 'und_code']].apply(lambda x: attach_zero(x), axis = 1)
    ws.range(output_head).options(pd.DataFrame, index = False).value = res

def save_bbg_tickers_for_dividend(
        parameter_date = "20240517",
        deriv_und_file: str = "infomax_underline_identifier.json",
        output_file_name: str = "bbg_tickers_for_dividend.json",):
    directory = os.path.join(jsondb_dir, parameter_date)
    und_iden_file = os.path.join(directory, deriv_und_file)
    try:
        und_iden = pd.read_json(und_iden_file)
    except:
        raise FileNotFoundError(f"File not found: {und_iden_file}")
    
    bbg_und = und_iden[["und_bbg"]].dropna(inplace=False)
    bbg_und.drop_duplicates(inplace=True)
    bbg_und.reset_index(drop=True, inplace=True)
    bbg_und.to_json(os.path.join(directory, output_file_name), orient='records')

if __name__ == "__main__":
    xw.Book("D:/Projects/marketdata/MarketData.xlsm").set_mock_caller()
    load_infomax_underline_identifier()