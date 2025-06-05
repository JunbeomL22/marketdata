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
    df['date'] = int(dt_str)
    # drop if "bench_id" is empty
    df = df[df['bench_id'].notna()]

    # convert issue_date, maturity, list_date, code_date all to "YYYYMMDD" format
    df['issue_date'] = df['issue_date'].apply(lambda x: x if x in (pd.NaT, None) else int(x.strftime('%Y%m%d')))
    df['maturity'] = df['maturity'].apply(lambda x: x if x in (pd.NaT, None) else int(x.strftime('%Y%m%d')))
    df['list_date'] = df['list_date'].apply(lambda x: x if x in (pd.NaT, None) else int(x.strftime('%Y%m%d')))
    df['code_date'] = df['code_date'].apply(lambda x: x if x in (pd.NaT, None) else int(x.strftime('%Y%m%d')))

    # select df that bench_id starts_from KTB_
    ktb_df = df[df['bench_id'].str.startswith('KTB_')].copy()
    # group by bench_id and add column start and end
    # start is issue_date and the end is the None or min of issue dates among bigger than my issue date
    ktb_df['start'] = ktb_df['issue_date']
    # sort by bench_id and issue_date to get the next issue date
    ktb_df.sort_values(['bench_id', 'issue_date'], inplace=True)
    ktb_df['end'] = ktb_df.groupby('bench_id')['issue_date'].shift(-1)

    other_df = df[~df['bench_id'].str.startswith('KTB_')].copy()
    other_df['end'] = other_df['maturity']
    other_df.sort_values(['bench_id', 'maturity'], inplace=True)
    other_df['start'] = other_df.groupby('bench_id')['maturity'].shift(1)
    
    ktb_res = ktb_df[['date', 'isin', 'start', 'end', 'bench_id']].copy()
    other_res = other_df[['date', 'isin', 'start', 'end', 'bench_id']].copy()

    res = pd.concat([ktb_res, other_res], ignore_index=True)

    # if start and end is not None, pd.Nat or NaN convert to int
    res['start'] = res['start'].apply(lambda x: x if x in (pd.NaT, None) or pd.isna(x) else str(int(x)))
    res['end'] = res['end'].apply(lambda x: x if x in (pd.NaT, None) or pd.isna(x) else str(int(x)))

    # Remove duplicate isin
    res = res.drop_duplicates(subset='isin', keep='first')

    res.to_json('D:/Projects/marketdata/bench_rev.json', orient='records', date_format='iso', indent=4, force_ascii=False)

if __name__ == "__main__":
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    save_bench_json()