from infomax_base_data import get_etf_info
import pandas as pd
from pykrx.website import krx
from datetime import datetime
import xlwings  as xw
import os

def get_krx_infomax_combined_etf_info():
    krx_base = krx.ETF_전종목기본종목().fetch()
    krx_base.rename(
        columns={
            "ISU_CD": "isin",
            "ISU_SRT_CD": "code",
            "ISU_NM": "name",
            "ISU_ABBRV": "short name",
            "LIST_DD": "issue date",
            "ETF_OBJ_IDX_NM": "target index",
            "IDX_CALC_INST_NM1": "index provider",
            "IDX_CALC_INST_NM2": "etf type",
            "ETF_REPLICA_METHD_TP_CD": "replication (krx)",
            "IDX_MKT_CLSS_NM": "market type",
            "IDX_ASST_CLSS_NM": "asset class",
            "CU_QTY": "creation unit",
            "ETF_TOT_FEE": "total fee",
            "TAX_TP_CD": "tax type",
            "COM_ABBRV": "issuer",
            },
        inplace=True
    )
    krx_base['total fee'] = krx_base['total fee'].astype(float).div(100.0   )

    krx_base['code'] = krx_base['code'].apply(lambda x: str(x).zfill(6))
    codes = krx_base.code.astype(str).unique().tolist()
    
    infomax_base = get_etf_info(codes)
    infomax_base.rename(
        columns={
            "replication": "replication (infomax)",
            "net_asset": "market cap",
            }, 
        inplace = True)
    
    infomax_base['market cap'] = infomax_base['market cap'].div(100000000.0)

    res = krx_base.merge(infomax_base[['isin', 'replication (infomax)', 'market cap']], 
                         on = 'isin', how = 'left')
    
    res = res[['isin', 'code', 'short name', 'market cap', 'issuer', 'issue date', 
               'etf type', 'replication (krx)', 'market type', 'asset class', 'creation unit',
               'total fee', 'tax type',  'replication (infomax)', 
               'target index', 'index provider']]

    return res

def save_etf_base_data(
        date = "20240421",
        file_name = 'etf_base_data.json'):
    # if there is no folder named Data/{date}, make it first
    directory = f'Data/{date}'
    if not os.path.exists(directory):
        os.makedirs(directory)

    res = get_krx_infomax_combined_etf_info()
    res.to_json(f'{directory}/{file_name}')

def load_etf_base_data(
        wb = None,
        sheet_name = 'BaseData',
        dt = "20240421",
        file_name = 'etf_base_info.json',
        output_head = 'G3',
        ):
    df = pd.read_json(f'Data/{dt}/{file_name}')
    if wb is None:
        wb = xw.Book.caller()
    
    df['issue date'] = df['issue date'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d'))
    df['code'] = df['code'].apply(lambda x: str(x).zfill(6))
    df.sort_values(by='market cap', ascending=False, inplace=True)
    ws = wb.sheets[sheet_name]
    ws.range(output_head).options(pd.DataFrame, index = False).value = df
    

if __name__ == "__main__":
    xw.Book("D:/ProjectsE/marketdata/MarketData.xlsm").set_mock_caller()
    save_etf_base_data()
    load_etf_base_data()

