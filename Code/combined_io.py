from code_config import jsondb_dir
import pandas as pd
import os

def save_all_equity_codes(
        parameter_date = "20240517",
        base_file = "krx_etf_combined_base.json",
        pdf_file = "krx_etf_pdf.json",
        ifmx_und_identifier = "infomax_underline_identifier.json",):
    print("Saving all_equity_codes...")
    directory = os.path.join(jsondb_dir, parameter_date)
    base = pd.read_json(os.path.join(directory, base_file), orient = "records")
    base = base[['code', 'name']]

    pdf = pd.read_json(os.path.join(directory, pdf_file), orient = "records")

    pdf = pdf[pdf['SECUGRP_ID'] == 'ST'][['COMPST_ISU_CD', 'COMPST_ISU_NM']]
    pdf.rename(columns = {'COMPST_ISU_CD': 'code', 'COMPST_ISU_NM': 'name'}, inplace = True)

    ifmx = pd.read_json(os.path.join(directory, ifmx_und_identifier), orient = "records")
    ifmx = ifmx[ifmx['und_type'] != 'C']
    ifmx = ifmx[['und_code', 'und_name']]
    ifmx.rename(columns = {'und_code': 'code', 'und_name': 'name'}, inplace = True)

    res = pd.concat([base, pdf, ifmx])
    res['code'] = res['code'].astype(str).str.zfill(6)
    res.drop_duplicates(inplace = True)

    return res