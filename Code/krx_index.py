from pykrx import stock
from infomax_base_data import get_security_base_info
import pandas as pd
import xlwings as xw

def get_krx_index_list(date = '20240405'):
    tickers = stock.get_index_ticker_list(date, market = 'KOSPI')
    tickers += stock.get_index_ticker_list(date, market = 'KOSDAQ')
    tickers += stock.get_index_ticker_list(date, market = 'KRX')
    tickers += stock.get_index_ticker_list(date, market = '테마')


    ticker_dict = {}
    for ticker in tickers:
        ticker_dict[ticker] = stock.get_index_ticker_name(ticker)

    res = pd.DataFrame(ticker_dict.items(), columns = ['code', 'name'])
    return res

def get_krx_index_pdf(
        codes = "1001",
        date = '20240405'):
    
    codes = codes.split("/")
    names = {}
    for code in codes:
        names[code] = stock.get_index_ticker_name(code)
    
    # make dataframe with code, name, und code

    data = {}
    code_data = []
    name_nada = []
    und_code_data = []
    for code in codes:
        pdf = stock.get_index_portfolio_deposit_file(code, date)
        for und_code in pdf:
            code_data.append(code)
            name_nada.append(names[code])
            und_code_data.append(und_code) 
    
    data['code'] = code_data
    data['name'] = name_nada
    data['und code'] = und_code_data

    res1 = pd.DataFrame(data)

    res2_list = []

    for i in range(10):
        df = get_security_base_info(market = f"{i}")
        res2_list.append(df)

    res2 = pd.concat(res2_list)

    res2.rename(columns = {'code': 'und code'}, inplace = True)
    
    res = pd.merge(res1, res2, on = 'und code', how = 'left')

    nan_code = res[res['isin'].isna()]['und code'].unique()

    res3_list = []
    for code in nan_code:
        df = get_security_base_info(code = code)
        res3_list.append(df)

    res3 = pd.concat(res3_list)
    res3.rename(columns = {'code': 'und code'}, inplace = True)

    code_df = pd.concat([res2, res3])
    
    res = pd.merge(res1, code_df, on = 'und code', how = 'left')

    return res

def load_krx_index_list(wb = None,
                        sheet_name = "IndexData",
                        date = "20240409",
                        output_head = "E4"):
    if wb is None:
        wb = xw.Book.caller()
    ws = wb.sheets[sheet_name]
    res = get_krx_index_list(date)
    ws.range(output_head).options(pd.DataFrame, index = False).value = res

def load_krx_index_pdf(wb = None,
                        sheet_name = "IndexData",
                        codes = "1001",
                        date = "20240409",
                        output_head = "N4"):
    if wb is None:
        wb = xw.Book.caller()
    ws = wb.sheets[sheet_name]
    res = get_krx_index_pdf(codes, date)
    ws.range(output_head).options(pd.DataFrame, index = False).value = res