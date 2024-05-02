import xlwings as xw
import pandas as pd
from code_config import jsondb_dir
import time
from custom_progress import printProgressBar
from utils import time_format
import urllib3;urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import os
import infomax_base_data

def load_etf_pdf(
        wb = None,
        sheet_name = 'EtfPdf',
        dt = '20240424',
        pdf_file = 'etf_pdf.json',
        output_head = 'F4',
        ):

    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    directory = os.path.join(jsondb_dir, dt)

    # if there is no pdf file, raise error message
    if not os.path.exists(f'{directory}/{pdf_file}'):
        raise ValueError(f'{directory}/{pdf_file} does not exist. Make the file first.')
    
    res = pd.read_json(f'{directory}/{pdf_file}', dtype = False)
    res['code'] = res['code'].str.zfill(6)
    ws.range(output_head).options(pd.DataFrame, index=False).value = res
       
def save_etf_pdf(
        dt = "20240424",
        base_info_file = 'etf_base_data.json',
        pdf_file = 'etf_pdf.json'):
    directory = os.path.join(jsondb_dir, dt)
    
    file = f'{directory}/{base_info_file}'

    if not os.path.exists(file):
        raise ValueError(f'{file} does not exist. Make the base data first.')
    
    base_info = pd.read_json(f'{directory}/{base_info_file}', dtype = False)
    codes = base_info['code'].unique().tolist()

    st = time.time()
    df_list = []
    N = len(codes)

    for i, ticker in enumerate(codes):
        try:
            df = infomax_base_data.get_etf_pdf(
                code = ticker, 
                date = dt,
                sort = "value"
                )
            df_list.append(df)
        except Exception as e:
            raise Exception(f"An error occurred with ticker {ticker}: {str(e)}")
        
        printProgressBar(
            i+1,
            N,
            prefix = 'etf-pdf crawling: ',
            suffix = f'complete (time: {time_format(time.time() - st)})', length = 20
            )
        
    if len(df_list) == 0:
        raise ValueError('No data retrieved. Check the data.')
    
    res = pd.concat(df_list)
    res.drop(columns = ['admin_number'], inplace = True)
    res['port_portion'] = res['port_value'] / res['etf_value']

    res.reset_index(drop = True, inplace = True)

    res.to_json(f'{directory}/{pdf_file}')

if __name__ == "__main__":
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    save_etf_pdf(
        dt = '20240430',
        base_info_file='etf_base_data.json',
    )    
