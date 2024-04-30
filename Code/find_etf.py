import os
import pandas as pd
import xlwings as xw
import time
from code_config import jsondb_dir

def find_etf(
        wb = None,
        codes = "KR350101GCB1", 
        sheet_name = "FindETF",
        dt = "20240424",
        all_futures = "N",
        derivative_file = "derivatives_base_data.json",
        pdf_file = "etf_pdf.json",
        output_head = "E4"
        ):
    # - 
    directory = os.path.join(jsondb_dir, dt)
                             
    pdf_file = f'{directory}/{pdf_file}'
    if not os.path.exists(pdf_file):
        raise ValueError(f'{pdf_file} does not exist. Make the pdf first or copy the file to the directory.')
    
    pdf = pd.read_json(pdf_file, dtype = False)
    pdf['code'] = pdf['code'].str.zfill(6)
    
    if all_futures == "N":
        codes = codes.split('/')
    else:
        derivative_file = f'{directory}/{derivative_file}'
        if not os.path.exists(derivative_file):
            raise ValueError(f'{derivative_file} does not exist. Make the derivative file first or copy the file to the directory.')
        
        derivative = pd.read_json(derivative_file, dtype = False)
        
        codes = derivative['und_isin'].unique().tolist()
    
    df_list = []
    for code in codes:
        df = pdf[pdf['port_isin'].str.contains(code)]
        df_list.append(df)
    
    if len(df_list) == 0:
        return None
    
    res = pd.concat(df_list)

    res = res.groupby(['isin', 'kr_name'])['port_portion'].sum().reset_index()
    res.sort_values(by = 'port_portion', ascending=False, inplace=True)

    if wb is None:
        wb = xw.Book.caller()
    ws = wb.sheets[sheet_name]
    ws.range(output_head).options(pd.DataFrame, index=False).value = res
    
def load_etf_include(wb = None,
                     sheet_name = 'FindETF',
                     codes = '247540/086520/005490/383310',
                     condition = 'and',
                     date = '20240405',
                     base_file = 'etf_base_info.json',
                     pdf_file = 'etf_pdf_20240405.json',
                     output_head = 'H3'):
    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    output_head = ws.range(output_head)

    res = find_etf(codes = codes, 
                           date = date,
                           condition = condition, 
                           base_file = base_file, 
                           pdf_file = pdf_file)
    
    if res is not None:
        output_head.options(pd.DataFrame, index = False).value = res
    else:
        print("there is no data")
        print(f"codes: {codes}, date: {date}, condition: {condition}")
        time.sleep(3)

if __name__ == '__main__':
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    #res = find_etf_include(codes = "247540/086520/005490/383310", condition = 'and', date = '20240405')
    load_etf_include(codes = "247540/086520/005490/383310")