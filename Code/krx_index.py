import pandas as pd
import requests

def get_krx_index_price(
        dt = "20240509",
        type_name = "KOSPI",):
    """
    type_name: KRX(01), KOSPI(02), KOSDAQ(03), Sector(04)
    단위
     * 수량: 천
     * 금액: 백만
    """
    if type_name == "KRX":
        idxIndMidclssCd = "01"
    elif type_name == "KOSPI":
        idxIndMidclssCd = "02"
    elif type_name == "KOSDAQ":
        idxIndMidclssCd = "03"
    elif type_name == "Sector":
        idxIndMidclssCd = "04"

    url = "http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd"
    params = {
        'bld': 'dbms/MDC/STAT/standard/MDCSTAT00101',
        'locale': 'ko_KR',
        'idxIndMidclssCd': idxIndMidclssCd,
        'trdDd': dt,
        'share': '2',
        'money': '3',
        'csvxls_isNo': 'false',
    }
    
    res = requests.get(
        url, 
        verify=False,
        params = params,
        )
    
    data = res.json()

    df = pd.DataFrame(data['output'])

    return df

