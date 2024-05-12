import krx_etf
import krx_stock
import os
from code_config import jsondb_dir
import pandas as pd
from datetime import datetime
from custom_progress import printProgressBar
from time import time, sleep
import xlwings as xw
from utils import time_format

def save_krx_etf_price(
        parameter_date = "20240509",
        retrieval_date = "20240510",
        file_name = 'krx_etf_price.json'):
    directory = os.path.join(jsondb_dir, parameter_date)
    if not os.path.exists(directory): os.makedirs(directory)
    
    res = krx_etf.get_krx_etf_price(dt = parameter_date)
    res.insert(0, 'retrieval_date', retrieval_date)
    res.insert(1, 'mktdate', parameter_date)
    res.drop_duplicates(subset = ['ISU_CD'], inplace = True)
    res.to_json(f'{directory}/{file_name}')

def save_krx_stock_price(
        parameter_date = "20240509",
        retrieval_date = "20240510",
        type_name = "ALL",
        file_name = 'krx_stock_price.json'):
    directory = os.path.join(jsondb_dir, parameter_date)
    if not os.path.exists(directory): os.makedirs(directory)

    res = krx_stock.get_krx_stock_price(dt = parameter_date, type_name = type_name)
    res.insert(0, 'retrieval_date', retrieval_date)
    res.insert(1, 'mktdate', parameter_date)
    res.drop_duplicates(subset = ['ISU_CD'], inplace = True)
    res.to_json(f'{directory}/{file_name}')

def save_krx_etf_base(
        parameter_date = "20240509",
        file_name = 'krx_etf_base.json',):
    directory = os.path.join(jsondb_dir, parameter_date)
    if not os.path.exists(directory): os.makedirs(directory)

    res = krx_etf.get_krx_etf_base()
    timestamp = datetime.now().strftime('%Y%m%d %H:%M:%S')
    res['timestamp'] = timestamp
    res.drop_duplicates(subset = ['ISU_CD'], inplace = True)
    res.to_json(f'{directory}/{file_name}')

def save_krx_etf_combined_base(
        parameter_date = "20240509",
        base_file = 'krx_etf_base.json',
        price_file = 'krx_etf_price.json',
        output_file = 'krx_etf_combined_base.json'
        ):
    directory = os.path.join(jsondb_dir, parameter_date)
    # check the files exist, otherwise raise an error
    base_file_name = f'{directory}/{base_file}'
    try:
        base = pd.read_json(base_file_name)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {base_file_name}")
        
    price_file_name = f'{directory}/{price_file}'
    try:
        price = pd.read_json(price_file_name)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {price_file_name}")
    
    base.rename(
        columns = {
            'ISU_CD': 'isin', 
            'ISU_SRT_CD': 'code', 
            'ISU_ABBRV': 'name',
            'LIST_DD': 'list_date',
            'ETF_OBJ_IDX_NM': 'index',
            'IDX_CALC_INST_NM1': 'index_agent',
            'ETF_REPLICA_METHD_TP_CD': 'replication_method',
            'IDX_MKT_CLSS_NM': 'market',
            'IDX_ASST_CLSS_NM': 'asset_class',
            'IDX_CALC_INST_NM2': 'etf_type',
            'LIST_SHRS': 'list_shares',
            'COM_ABBRV': 'company',
            'CU_QTY': 'creation_unit',
            'ETF_TOT_FEE': 'ter_bp',
            'TAX_TP_CD': 'tax',
            'timestamp': 'timestamp',
            }, 
            inplace = True)
    
    price.rename(
        columns = {
            'mktdate': 'price_date',
            'ISU_CD': 'isin',
            'NAV': 'nav',
            'TDD_CLSPRC': 'close',
            'ACC_TRDVAL': 'trading_value',
            'MKTCAP': 'market_cap',
            },
            inplace = True)
    res = pd.merge(base, price, on = 'isin', how = 'inner')
    res_cols = [
        'isin', 
        'code', 
        'name', 
        'market_cap', 
        'trading_value',
        'price_date', 
        'nav', 
        'close', 
        'etf_type', 
        'replication_method',
        'market', 
        'asset_class', 
        'list_shares', 
        'company', 
        'index', 
        'index_agent',
        'creation_unit', 
        'ter_bp', 
        'tax', 
        'list_date', 
        'timestamp',
        ]
    
    res = res[res_cols]
    res['list_shares'] = res['list_shares'].str.replace(',', '').astype(int)
    res['creation_unit'] = res['creation_unit'].str.replace(',', '').astype(int)
    res['market_cap'] = res['market_cap'].str.replace(',', '').astype(float) / 100000000.0
    res['trading_value'] = res['trading_value'].str.replace(',', '').astype(float) / 100000000.0
    res['nav'] = res['nav'].str.replace(',', '').astype(float)
    res['close'] = res['close'].str.replace(',', '').astype(float)
    res['ter_bp'] = res['ter_bp'].astype(float) * 100.

    res.sort_values(by='market_cap', ascending=False, inplace=True)

    res.to_json(f'{directory}/{output_file}')

def load_krx_etf_combined_base(
        wb = None,
        sheet_name = "BaseData",
        parameter_date = "20240509",
        file_name = 'krx_etf_combined_base.json',
        output_head = 'G3',):
    # - wb: xlwings workbook object
    if wb is None:
        wb = xw.Book.caller()

    directory = os.path.join(jsondb_dir, parameter_date)
    file_name = f'{directory}/{file_name}'
    try:
        res = pd.read_json(file_name)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_name}")
    
    res['code'] = res['code'].astype(str).str.zfill(6)
    ws = wb.sheets[sheet_name]
    ws.range(output_head).options(index = False).value = res
        
def save_krx_etf_pdf(      
        wb = None,
        sheet_name = "EtfPdf",  
        etf_pdf_add_list_range = 'EtfPdfAddList',
        parameter_date = "20240509",
        combined_base_file = 'krx_etf_combined_base.json',
        pdf_file = 'krx_etf_pdf.json',
        min_cap = 800.0,
        market_type = '국내',
        sleep_time = 0.0):
    # - wb: xlwings workbook object
    if wb is None:
        wb = xw.Book.caller()
    ws = wb.sheets[sheet_name]
    etf_pdf_add_list = ws.range(etf_pdf_add_list_range).value
    # - remove empty rows from the list and make it to df with the first row as columns 
    etf_pdf_add_list = [x for x in etf_pdf_add_list if x[0] is not None]
    etf_pdf_add_list_df = pd.DataFrame(etf_pdf_add_list[1:], columns = etf_pdf_add_list[0])

    directory = os.path.join(jsondb_dir, parameter_date)
    if not os.path.exists(directory): os.makedirs(directory)
    base_file_name = f'{directory}/{combined_base_file}'
    pdf_file = f'{directory}/{pdf_file}'

    try:
        base = pd.read_json(base_file_name)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {base_file_name}")
    
    base['market_cap'] = base['market_cap'].astype(float)
    base['code'] = base['code'].astype(str).str.zfill(6)
    base = base[base['market_cap'] >= min_cap]
    if market_type != '전체':
        base = base[base['market'] == market_type]

    crawling_list = base[['isin', 'code', 'name']]
    crawling_list = pd.concat([crawling_list, etf_pdf_add_list_df], ignore_index = True)
    crawling_list.drop_duplicates(subset = ['isin'], inplace = True)
    crawling_list.reset_index(drop = True, inplace = True)

    st = time()
    N = len(crawling_list)
    print("# of ETFs to crawl: ", len(crawling_list))
    for i, row in crawling_list.iterrows():
        etf_isin = row['isin']
        etf_code = row['code']
        etf_name = row['name']
        try:
            printProgressBar(
                i + 1, 
                N, 
                prefix = 'Progress:', 
                suffix = f'Complete ({time_format(time() - st)})',
                length = 20
                )
            
            df = krx_etf.get_krx_etf_pdf(isin = etf_isin, code = etf_code, name = etf_name)
            if df is not None:
                df.insert(0, 'etf_isin', etf_isin)
                df.insert(1, 'etf_code', etf_code)
                df.insert(2, 'etf_name', etf_name)
                df['timestamp'] = datetime.now().strftime('%Y%m%d %H:%M:%S')

            if len(df) == 0:
                print(f"No data found for {etf_isin} | {etf_code} | {etf_name}")
                continue
        
            if i == 0:
                
                df.to_json(pdf_file, orient = 'records')
            else:
                existing_df = pd.read_json(pdf_file, orient = 'records')
                existing_df['timestamp'] = pd.to_datetime(existing_df['timestamp'])
                combined_df = pd.concat([existing_df, df])
                combined_df.reset_index(inplace=True, drop=True)
                combined_df['timestamp'] = combined_df['timestamp'].astype(str)
                combined_df.to_json(pdf_file, orient = 'records')
            sleep(sleep_time)

        except Exception as e:
            print(f"Error occured in retreiving {etf_isin} | {etf_code} | {etf_name}: {e}")
            continue

def load_krx_etf_pdf(
        wb = None,
        sheet_name = "EtfPdf",
        parameter_date = "20240509",
        pdf_file = 'krx_etf_pdf.json',
        output_head = 'J4',):
    # - wb: xlwings workbook object
    if wb is None:
        wb = xw.Book.caller()
    
    ws = wb.sheets[sheet_name]
    pdf_file = f'{jsondb_dir}/{parameter_date}/{pdf_file}'
    try:
        res = pd.read_json(pdf_file)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {pdf_file}")
    
    res['etf_code'] = res['etf_code'].astype(str).str.zfill(6)
    res.rename(
        columns = {
            'COMPST_ISU_CD': 'code',
            'COMPST_ISU_CD2': 'isin',
            'MKT_ID': 'market',
            'SECUGRP_ID': 'market2',
            'COMPST_ISU_NM': 'name',
            'COMPST_ISU_CU1_SHRS': 'share',
            'VALU_AMT': 'value',
            'COMPST_AMT': 'port_value',
            'COMPST_RTO': 'port_ratio',
        },
        inplace = True
    )
    res['code'] = res['code'].astype(str).str.zfill(6)
    ws.range(output_head).options(pd.DataFrame, index = False).value = res

if __name__ == '__main__':
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    save_krx_etf_pdf()