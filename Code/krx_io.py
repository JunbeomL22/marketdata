import krx_etf
import krx_stock
import os
from code_config import jsondb_dir
import pandas as pd
from datetime import datetime
from custom_progress import printProgressBar
from time import time, sleep

def save_krx_etf_price(
        parameter_date = "20240509",
        retrieval_date = "20240510",
        file_name = 'krx_etf_price.json'):
    directory = os.path.join(jsondb_dir, parameter_date)
    if not os.path.exists(directory): os.makedirs(directory)
    
    res = krx_etf.get_krx_etf_price(dt = parameter_date)
    res.insert(0, 'retrieval_date', retrieval_date)
    res.insert(1, 'mktdate', parameter_date)

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

    res.to_json(f'{directory}/{file_name}')

def save_krx_etf_base(
        parameter_date = "20240509",
        file_name = 'krx_etf_base.json',):
    directory = os.path.join(jsondb_dir, parameter_date)
    if not os.path.exists(directory): os.makedirs(directory)

    res = krx_etf.get_krx_etf_base()
    timestamp = datetime.now().strftime('%Y%m%d %H:%M:%S')
    res['timestamp'] = timestamp

    res.to_json(f'{directory}/{file_name}')

def save_krx_multiple_etf_pdf(
        base = None,
        codes = None,
        parameter_date = "20240509",
        file_name = 'krx_etf_pdf.json',
        sleep_time = 0.0):
    directory = os.path.join(jsondb_dir, parameter_date)
    if not os.path.exists(directory): os.makedirs(directory)
    file_name = f'{directory}/{file_name}'

    if base is None:
        base = krx_etf.get_krx_etf_base()

    if codes is not None:
        if isinstance(codes, str):
            codes = codes.split(',')
        base = base[base['ISU_SRT_CD'].isin(codes)]

    st = time()
    N = len(base)

    for i, row in base.iterrows():
        etf_isin = row['ISU_CD']
        etf_code = row['ISU_SRT_CD']
        etf_name = row['ISU_ABBRV']
        try:
            printProgressBar(
                i + 1, 
                N, 
                prefix = 'Progress:', 
                suffix = 'Complete ({:.2f} seconds)'.format(time() - st),
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
        
            if i == 0:
                df.to_json(file_name)
            else:
                existing_df = pd.read_json(file_name)
                combined_df = pd.concat([existing_df, df])
                combined_df.reset_index(inplace=True, drop=True)
                combined_df.to_json(file_name)
            sleep(sleep_time)

        except Exception as e:
            print(f"Error occured in retreiving {etf_isin} | {etf_code} | {etf_name}: {e}")
            continue

#price_df = pd.read_json(f'{jsondb_dir}/20240509/krx_etf_price.json')
#base_df = pd.read_json(f'{jsondb_dir}/20240509/krx_etf_base.json')

#save_krx_multiple_etf_pdf(base = base_df, sleep_time = 3)