import xlwings as xw
import pandas as pd
import os
from code_config import jsondb_dir

def save_index_weight_from_etf(
        wb = None,
        sheet_name = 'Index',
        parameter_date = '20240520',
        idx_etf_match_range_name = "IndexEtfMatch",
        etf_pdf_file = "krx_etf_pdf.json",
        #
        #stock_price_file = "krx_stock_price.json",
        combined_etf_base_file = "krx_etf_combined_base.json",
        #
        output_file = "index_weight_from_etf.json",):
    # - 
    print("saving index weight from etf...")
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
            'COMPST_ISU_CD2': 'isin',
            'SECUGRP_ID': 'market2',
            'COMPST_ISU_CU1_SHRS': 'shares',
            'VALU_AMT': 'value',
            'COMPST_ISU_NM': 'name',
        },
        inplace=True,)

    etf_pdf['code'] = etf_pdf['code'].astype(str).str.zfill(6)
    etf_pdf['shares'] = etf_pdf['shares'].str.replace(',', '').replace('-', '0').astype(float)
    etf_pdf['value'] = etf_pdf['value'].str.replace(',', '').replace('-', '0').astype(float)
    etf_base = pd.read_json(os.path.join(directory, combined_etf_base_file), orient='records')
    etf_base['code'] = etf_base['code'].astype(str).str.zfill(6)

    idx_names = idx_etf_match['name'].unique().tolist()
    chosen_base = etf_base[etf_base['index'].isin(idx_names)].drop_duplicates(subset=['index'])
    chosen_base['index_close'] = chosen_base['index_close'].str.replace(',', '').astype(float)

    assert len(chosen_base) == len(idx_names), "Some ETFs are missing in the base file"

    def get_weight(idx_name, weight_scale=1000.0):
        idx_price = chosen_base[chosen_base['index'] == idx_name]['index_close'].values[0]
        etf = idx_etf_match[idx_etf_match['name'] == idx_name]

        weight1 = None
        weight2 = None

        etf_code1 = etf['etf_code1'].values[0]
        if etf_code1 is not None:
            etf_pdf1 = etf_pdf[etf_pdf['etf_code'] == etf_code1]
            if etf_pdf1.empty:
                raise ValueError(f"ETF {etf_code1} is not found in the ETF PDF file")
            res1 = etf_pdf1[~etf_pdf1['isin'].str.contains('KRD010010001') & ~etf_pdf1['isin'].str.contains('CASH00000001')]
            total1 = res1['value'].div(weight_scale).sum()
            ratio1 = idx_price / total1
            weight1 = (res1[['shares']] * ratio1).rename(columns={'shares': 'weight1'})
            weight1.set_index([pd.Index(res1['isin']), pd.Index(res1['code'])], inplace=True)

        etf_code2 = etf['etf_code2'].values[0]
        if etf_code2 is not None:
            etf_pdf2 = etf_pdf[etf_pdf['etf_code'] == etf_code2]
            if not etf_pdf2.empty:   
                res2 = etf_pdf2[~etf_pdf2['isin'].str.contains('KRD010010001') & ~etf_pdf2['isin'].str.contains('CASH00000001')]
                total2 = res2['value'].div(weight_scale).sum()
                ratio2 = idx_price / total2
                weight2 = (res2[['shares']] * ratio2).rename(columns={'shares': 'weight2'})
                weight2.set_index([pd.Index(res2['isin']), pd.Index(res2['code'])], inplace=True)

        if weight2 is None:
            weight = weight1
            weight.fillna(0, inplace=True)
            weight.rename(columns={'weight1': 'weight'}, inplace=True)
        else:
            weight = pd.concat([weight1, weight2], axis=1)
            weight.fillna(0, inplace=True)
            weight['weight'] = (weight['weight1'] + weight['weight2']) * 0.5
            weight.drop(columns=['weight1', 'weight2'], inplace=True)
            
        weight.insert(0, 'index', idx_name)
        weight['weight_scale'] = weight_scale
        return weight.reset_index()

    ids_df = idx_etf_match[['index_type', 'bbg_code', 'und_code', 'name']]
    weight_list = []
    for idx in ids_df.itertuples():
        idx_name = idx.name
        idx_bbg_code = idx.bbg_code
        idx_und_code = idx.und_code
        df = get_weight(idx_name)
        df['index_type'] = idx.index_type
        df['bbg_code'] = idx_bbg_code
        df['und_code'] = idx_und_code
        weight_list.append(df)

    weight = pd.concat(weight_list).reset_index(drop=True)
    weight.to_json(os.path.join(directory, output_file), orient='records')

if __name__ == '__main__':
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    save_index_weight_from_etf(parameter_date = '20240523')
    res = pd.read_json(os.path.join(jsondb_dir, '20240523', 'index_weight_from_etf.json'), orient='records')
    res['code'] = res['code'].astype(str).str.zfill(6)