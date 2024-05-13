import requests
import pandas as pd

def get_krx_kts(date):
    r = requests.post(
        url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd",
        params = {"bld": "dbms/MDC/STAT/standard/MDCSTAT09801",
                "locale": "ko_KR",
                "mktId": "KTS",
                "trdDd": date,
                "money": 2,
                "csvxls_isNo": False}
    )
    
    return pd.DataFrame(r.json()['output'])
    
def get_krx_credit(date):
    r = requests.post(
        url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd",
        params = {"bld": "dbms/MDC/STAT/standard/MDCSTAT09801",
                "locale": "ko_KR",
                "mktId": "BND",
                "trdDd": date,
                "money": 2,
                "csvxls_isNo": False}
    )
    
    return pd.DataFrame(r.json()['output'])

def get_krx_smb(date):
    r = requests.post(
        url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd",
        params = {"bld": "dbms/MDC/STAT/standard/MDCSTAT09801",
                "locale": "ko_KR",
                "mktId": "SMB",
                "trdDd": date,
                "money": 2,
                "csvxls_isNo": False}
    )
    
    return pd.DataFrame(r.json()['output'])
