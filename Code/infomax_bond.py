import requests
import pandas as pd
from code_config import INFOMAX_HEADER, data_path
from custom_progress import printProgressBar
from utils import time_format
import time
import re

def listed_bond(
        stdcd: str = "",
        bondnm: str = "",
        kindnm: str = ""):
    
    session = requests.Session()
    
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/bond/market/code_info'

    params = {"stdcd": stdcd,
              "bondnm": bondnm,
              "kindnm": kindnm}
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        print("listed_bond() failed")
    return res

def bond_base_info(stdcd):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/bond/basic_info'

    params = {"stdcd": stdcd.split(",")}
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None

    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception("bond_base_info() failed")

    return res

def get_bond_info_in_pdf(
        pdf_file_name = "etf_pdf_20240416.json"):
    
    pdf = pd.read_json(data_path + pdf_file_name)

    isins = pdf['port_isin'].unique()

    df_list = []
    N = len(isins)
    st = time.time()
    pattern = r'^KR([1-3]|6)'
    for i, isin in enumerate(isins):
        if bool(re.match(pattern, isin)):
            df_list.append(bond_base_info(isin))
        
        printProgressBar(
            i+1, N,
            prefix = 'bond info crawling: ',
            suffix = f'complete (time: {time_format(time.time() - st)})', length = 20)
        
    res = pd.concat(df_list)
    res.reset_index(inplace = True)
    res.drop(columns = ['index'], inplace = True)

    return res