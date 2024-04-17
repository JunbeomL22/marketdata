import requests
import pandas as pd
from code_config import INFOMAX_HEADER, data_path
from custom_progress import printProgressBar
from utils import time_format
import time
import re
import xlwings as xw

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
        pdf_file_name = "etf_pdf_20240416.json",
        output_file_name = "bond_info.json"):
    
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

def load_bond_info(wb = None,
                   sheet_name = "BondInfo",
                   output_head = "F3",
                   file_name = "bond_info.json"):
    if wb is None:
        wb = xw.Book.caller()
    
    ws = wb.sheets[sheet_name]
    bond_info = pd.read_json(data_path + file_name)
    
    bond_info.rename(columns= {"stdcd": "ISIN",
                                "bondnm": "Name",
                                "issuedate": "IssueDate",
                                "expidate": "Maturity",
                                "couponrate": "CouponRate",
                                "intpayterm": "Frequency",
                                "crdtparrate1": "CreditRating",
                                "bhgigwancd": "Issuer",
                                "currencygb": "Currency",
                                "inttype_1": "CouponType"},
                                inplace = True)
    
    bond_info['Currency'] = bond_info['Currency'].astype(str)
    bond_info['Frequency'] = bond_info['Frequency'].astype(str)
    bond_info['Issuer'] = bond_info['Issuer'].astype(str)

    bond_info['Currency'].replace({"1": "KRW",}, inplace = True)
    bond_info['Frequency'].replace({"1": "Monthly",
                                    "3": "Quarterly",
                                    "6": "Semi-annually",
                                    "12": "Annually"
                                    }, 
                                    inplace = True)

    bond_info['Issuer'].replace({
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
        }, 
        inplace = True)


    res = bond_info[['ISIN', 'Name', 'IssueDate', 'Maturity', 'CouponType', 'CouponRate', 
                     'Frequency', 'CreditRating', 'Issuer', 'Currency']]
    ws.range(output_head).options(pd.DataFrame, index = False).value = res

#xw.Book("D:/Projects/marketdata/MarketData.xlsm").set_mock_caller()
load_bond_info(sheet_name="BondInfo")