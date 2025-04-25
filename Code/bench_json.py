import xlwings as xw
import pandas as pd

def save_bench_json():
    """Load ISIN DataFrame from Excel and return it."""
    wb = xw.Book.caller()
    sheet = wb.sheets['Bench']
    df = sheet.range('IsinList').options(pd.DataFrame, header=1, index=False).value
    # get today from "D2" cell as "YYYYMMDD" format
    dt = sheet.range('D2').value
    dt_str = dt.strftime('%Y%m%d')
    df['date'] = dt_str
    # convert issue_date, maturity, list_date, code_date all to "YYYYMMDD" format
    df['issue_date'] = df['issue_date'].apply(lambda x: x if x in (pd.NaT, None) else x.strftime('%Y%m%d'))
    df['maturity'] = df['maturity'].apply(lambda x: x if x in (pd.NaT, None) else x.strftime('%Y%m%d'))
    df['list_date'] = df['list_date'].apply(lambda x: x if x in (pd.NaT, None) else x.strftime('%Y%m%d'))
    df['code_date'] = df['code_date'].apply(lambda x: x if x in (pd.NaT, None) else x.strftime('%Y%m%d'))

    # drop if "bench_id" is empty
    df = df[df['bench_id'].notna()]

    # save as bench_rev.json
    # keep korean characters in the json file
    df = df[['date', 'isin', 'issue_date', 'maturity', 'list_date', 'code_date', 'bench_id']]
    df.to_json('D:/Projects/marketdata/bench_rev.json', orient='records', date_format='iso', indent=4, force_ascii=False)

if __name__ == "__main__":
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    save_bench_json()
    