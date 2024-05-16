import requests
import pandas as pd
from code_config import INFOMAX_HEADER, data_path, etf_base_path
from custom_progress import printProgressBar
from utils import time_format
import time
import re
import xlwings as xw
issuer_match = {
        "GB035": "대한민국",
        "AB101": "한국은행",
        "04725": "산업은행",
        "02411": "기업은행",
        "AB808": "수출입은행",
        "00001": "신한은행",
        "00003": "우리은행",
        "00494": "하나은행",
        "06000": "국민은행",
        "15373": "농협은행",
        "03075": "하나증권",
        "17414": "우리카드",
        "20549": "하나카드",
        "09724": "농협캐피탈",
        "13893": "BNK금융지주",
        "00827": "산은캐피탈",
        "00856": "메리츠증권",
        "01980": "하나캐피탈",
        "02978": "삼성캐피탈",
        "02988": "현대캐피탈",
        "00528": "부산은행",
        "01945": "아이비케이캐피탈",
        }

coupon_type_match = {
    "11": "Zero Coupon",
    "12": "Compoundeds",
    "13": "Fixed",
    "14": "Simple",
    "21": "Floating",
}
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

def bond_base_info(stdcd = "",
                   inttype_1 = ""):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/bond/basic_info'

    params = {"stdcd": stdcd, "inttype_1": inttype_1}
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None

    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception("bond_base_info() failed")

    return res

def select_port_isin(
        pdf_file_name = "etf_pdf_20240416.json",
        base_file_name = "etf_base_info.json",
        full_info_file_name = "full_etf_info.csv",
        etf_types = "국내채권형, 일반/해외채권형, 일반")
    
    etf_types = etf_types.split("/")
    pdf = pd.read_json(data_path + pdf_file_name)
    base_info = pd.read_json(etf_base_path + base_file_name)
    full_info = pd.read_csv(etf_base_path + full_info_file_name)
    info = base_info.merge(full_info, on='code', how='left')
    
    # Merge pdf and base_info on 'isin'
    merged_df = pd.merge(pdf, info, on='isin', how='inner')
    
    df_list = []
    for type_name in etf_types:
        filtered_df = merged_df[merged_df['type'].str.contains(type_name)]
        df_list.append(filtered_df)
    
    df = pd.concat(df_list)
    res = df['port_isin'].unique().tolist()

    return res

def load_bond_isin_in_pdf(wb = None,
                   sheet_name = "BondInfo",
                   pdf_file_name = "etf_pdf_20240416.json",
                   base_file_name = "etf_base_info.json",
                   full_info_file_name = "full_etf_info.csv",
                   etf_types = "국내채권형, 일반/해외채권형, 일반",
                   output_head = "F3"):
    if wb is None:
        wb = xw.Book.caller()
    
    isins = select_port_isin(
        pdf_file_name = pdf_file_name,
        base_file_name = base_file_name,
        full_info_file_name = full_info_file_name,
        etf_types = etf_types)
                           
    ws = wb.sheets[sheet_name]
    
    ws.range(output_head).value = isins[:,None]

xw.Book("D:/Projects/marketdata/MarketData.xlsm").set_mock_caller()
