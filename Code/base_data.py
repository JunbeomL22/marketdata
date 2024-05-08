from infomax_base_data import get_etf_info, get_security_base_info
import pandas as pd
from pykrx.website import krx
from datetime import datetime
import xlwings  as xw
import os
from code_config import jsondb_dir

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
    
    infomax_base = get_etf_info(",".join(codes))
    infomax_base.rename(
        columns={
            "replication": "replication (infomax)",
            "net_asset": "market cap",
            }, 
        inplace = True)
    
    infomax_base['market cap'] = infomax_base['market cap'].div(100000000.0)

    res = krx_base.merge(infomax_base[['isin', 'replication (infomax)', 'market cap']], 
                         on = 'isin', how = 'left')
    
    res = res[['isin', 'code', 'short name', 'market cap', 'issuer', 'issue date', 'etf type', 
               'replication (krx)', 'market type', 'asset class', 'creation unit', 'total fee', 
               'tax type',  'replication (infomax)', 'target index', 'index provider']]

    return res

def get_infomax_etf_base_data(
        dt = "20240502",):
    # - 
    etf_list = get_security_base_info(dt = dt, type_name = "EF")
    etf_list['code'] = etf_list['code'].str.zfill(6)
    codes = etf_list['code'].str.cat(sep = ",")
    etf_info = get_etf_info(codes)
    etf_info['code'] = etf_info['code'].str.zfill(6)    
    etf_info.drop_duplicates('isin', inplace=True)
    etf_info.rename(
        columns={
            "net_asset": "market_cap",
            },
        inplace=True
    )

    etf_info['market_cap'] = etf_info['market_cap'].div(100000000.0)
    etf_info.sort_values(by='market_cap', ascending=False, inplace=True)

    return etf_info

def save_infomax_etf_base_data(
        retrieval_date = "20240503",
        parameter_date = "20240502",
        file_name = 'etf_base_data.json'):
    directory = os.path.join(jsondb_dir, parameter_date)
    if not os.path.exists(directory):
        os.makedirs(directory)
    res = get_infomax_etf_base_data(dt = retrieval_date)
    res.to_json(f'{directory}/{file_name}')

def load_infomax_etf_base_data(
        wb = None,
        sheet_name = 'BaseData',
        parameter_date = "20245202",
        file_name = 'etf_base_data.json',
        output_head = 'G3',
        ):
    directory = os.path.join(jsondb_dir, parameter_date)

    df = pd.read_json(f'{directory}/{file_name}')
    if wb is None:
        wb = xw.Book.caller()
    
    df['code'] = df['code'].astype(str).str.zfill(6)
    df['company_code'] = df['company_code'].astype(str).str.zfill(6)
    
    ws = wb.sheets[sheet_name]
    ws.range(output_head).options(pd.DataFrame, index = False).value = df

def save_krx_etf_base_data(
        retrieval_date = "20240421",
        parameter_date = "20240421",
        file_name = 'etf_base_data.json'):
    directory = os.path.join(jsondb_dir, parameter_date)    
    
    if not os.path.exists(directory):
        os.makedirs(directory)

    res = get_krx_infomax_combined_etf_info()
    # Add 'retrieval date' column with the given retrieval_date as its value
    res['retrieval date'] = retrieval_date

    # Make 'retrieval date' the first column
    res.insert(0, 'retrieval date', res.pop('retrieval date'))

    res.to_json(f'{directory}/{file_name}')

def load_krx_etf_base_data(
        wb = None,
        sheet_name = 'BaseData',
        parameter_date = "20240421",
        file_name = 'etf_base_info.json',
        output_head = 'G3',
        ):
    directory = os.path.join(jsondb_dir, parameter_date)

    df = pd.read_json(f'{directory}/{file_name}')
    if wb is None:
        wb = xw.Book.caller()
    
    df['issue date'] = df['issue date'].apply(lambda x: datetime.strptime(x, '%Y/%m/%d'))
    df['code'] = df['code'].apply(lambda x: str(x).zfill(6))
    df.sort_values(by='market cap', ascending=False, inplace=True)
    ws = wb.sheets[sheet_name]
    ws.range(output_head).options(pd.DataFrame, index = False).value = df
    
if __name__ == "__main__":
    xw.Book("D:/ProjectsE/marketdata/MarketData.xlsm").set_mock_caller()
    save_infomax_etf_base_data()
    save_etf_base_data()
    load_etf_base_data()

