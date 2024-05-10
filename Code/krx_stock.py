import requests
import pandas as pd

def get_krx_stock_price(
        dt = "20240509",
        type_name = "ALL",):
    """
    type_name: ALL, STK
    """
    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"

    mktId = ""
    seqTpCd = "ALL"
    if type_name == "ALL":
        mktId = "ALL"
    elif type_name == "KOSPI":
        mktId = "STK"
    elif type_name == "KOSDAQ":
        mktId = "KSQ"
        seqTpCd = "ALL"    
    elif type_name == "KOSDAQG":
        mktId = "KSQ"
        seqTpCd = "1"
    elif type_name == "KONEX":
        mktId = "KNX"
    else:
        raise ValueError(f"Invalid type_name for get_krx_price: {type_name}")
    
    if type_name in ("KOSDAQ", "KOSDAQG"):
        params = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
            'locale': 'ko_KR',
            'mktId': mktId,
            'segTpCd': seqTpCd,
            'trdDd': dt,
            'share': '1',
            'money': '1',
            'csvxls_isNo': 'false',
        }
    else:
        params = {
            'bld': 'dbms/MDC/STAT/standard/MDCSTAT01501',
            'locale': 'ko_KR',
            'mktId': mktId,
            'trdDd': dt,
            'share': '1',
            'money': '1',
            'csvxls_isNo': 'false',
        }

    res = requests.post(
        url, 
        verify=False,
        data = params,
        )
    
    data = res.json()
    df = pd.DataFrame(data['OutBlock_1'])

    return df