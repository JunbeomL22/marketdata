import xlwings as xw
import pandas as pd
import os
from code_config import jsondb_dir

wb = None
sheet_name = 'Index'
parameter_date = '20240517'
idx_etf_match_range_name = "IndexEtfMatch"
etf_pdf_file = "krx_etf_pdf.json"
etf_price_file = "krx_etf_price.json"
stock_price_file = "krx_stock_price.json"
combined_etf_base_file = "krx_etf_combined_base.json"

xw.Book('MarketData.xlsm').set_mock_caller()
if wb is None:
    wb = xw.Book.caller()
ws = wb.sheets[sheet_name]
etf_range = ws.range(idx_etf_match_range_name).value
etf_range = [x for x in etf_range if x[0] is not None]
idx_etf_match = pd.DataFrame(etf_range[1:], columns=etf_range[0])
idx_etf_match['etf_code1'] = idx_etf_match['etf_code1'].astype(str).str.zfill(6)
idx_etf_match['etf_code2'] = idx_etf_match['etf_code2'].apply(lambda x: str(x).zfill(6) if x is not None else None)

directory = os.path.join(jsondb_dir, parameter_date)
etf_pdf = pd.read_json(os.path.join(directory, etf_pdf_file), orient='records')
etf_pdf['etf_code'] = etf_pdf['etf_code'].astype(str).str.zfill(6)
etf_pdf.rename(
    columns={
        'COMPST_ISU_CD': 'code',
        'SECUGRP_ID': 'market2',
        'COMPST_ISU_CU1_SHRS': 'shares',
        'VALU_AMT': 'value',
        'COMPST_ISU_NM': 'name',
    },
    inplace=True,)

etf_pdf['code'] = etf_pdf['code'].astype(str).str.zfill(6)
etf_pdf['shares'] = etf_pdf['shares'].str.replace(',', '').replace('-', '0').astype(float)
etf_pdf['value'] = etf_pdf['value'].str.replace(',', '').replace('-', '0').astype(float)
etf_price = pd.read_json(os.path.join(directory, etf_price_file), orient='records')
stock_price = pd.read_json(os.path.join(directory, stock_price_file), orient='records')
etf_base = pd.read_json(os.path.join(directory, combined_etf_base_file), orient='records')
etf_base['code'] = etf_base['code'].astype(str).str.zfill(6)

idx_names = idx_etf_match['name'].unique().tolist()
chosen_base = etf_base[etf_base['index'].isin(idx_names)].drop_duplicates(subset=['index'])
chosen_base['index_close'] = chosen_base['index_close'].str.replace(',', '').astype(float)

assert len(chosen_base) == len(idx_names), "Some ETFs are missing in the base file"


idx_name = '코스피 200'
idx_price = chosen_base[chosen_base['index'] == idx_name]['index_close'].values[0]
etf = idx_etf_match[idx_etf_match['name'] == idx_name]
etf_pdf1 = etf_pdf[etf_pdf['etf_code'] == etf['etf_code1'].values[0]]
res = etf_pdf1[~etf_pdf1['name'].str.contains('현금')]

total = res['value'].div(100.0).sum()
weight = idx_price / total

res['shares'] = res['shares'] * weight