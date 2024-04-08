import xlwings as xw
import pandas as pd
import code_config
import re
from datetime import datetime
from time import time
import sys, json, requests
from custom_progress import printProgressBar
from utils import time_format
from infomax_base_data import get_index_list, get_index_pdf
import urllib3;urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_index_pdf(
        wb = None,
        #sheet_name = 'IndexPdf',
        #output_range_name = 'IndexPdf',
        #date_cell = 'C4',
        #match_file_name_cell = 'C5'
        ):             
        
    #if wb is None:
    #    wb = xw.Book.caller()

    #ws = wb.sheets[sheet_name]
    #date_str = str(ws.range(date_cell).value)
    #match_file_name = str(ws.range(match_file_name_cell).value)
    
    #output_range = ws.range(output_range_name)
    #output_range.clear_contents()

    #match_df = pd.read_json(code_config.data_path + match_file_name, dtype = False)

    #tickers = match_df['ticker'].unique().tolist()
    tickers = get_index_list()['code'].tolist()
    st = time()
    df_list = []
    N = len(tickers)

    for i, ticker in enumerate(tickers):
        
        printProgressBar(i+1,
                        N,
                        prefix = 'index-pdf crawling: ',
                        suffix = f'complete (time: {time_format(time() - st)})', length = 20)
        
        df = get_index_pdf(ticker)

        df_list.append(df)

    res = pd.concat(df_list)
    
    return res

if __name__ == '__main__':
    res = load_index_pdf()