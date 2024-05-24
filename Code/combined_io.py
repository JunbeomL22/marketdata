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

    pdf = pdf[pdf['MKT_ID'] == 'STK'][['COMPST_ISU_CD', 'COMPST_ISU_NM']]
    pdf.rename(columns = {'COMPST_ISU_CD': 'code', 'COMPST_ISU_NM': 'name'}, inplace = True)

    ifmx = pd.read_json(os.path.join(directory, ifmx_und_identifier), orient = "records")
    ifmx = ifmx[ifmx['und_type'] != 'C']
    ifmx = ifmx[['und_code', 'und_name']]
    ifmx.rename(columns = {'und_code': 'code', 'und_name': 'name'}, inplace = True)

    res = pd.concat([base, pdf, ifmx])
    res['code'] = res['code'].astype(str).str.zfill(6)
    res.drop_duplicates(inplace = True)

    return res

def save_bbg_tickers_for_dividend(
        parameter_date = "20240523",
        deriva_und_file = "infomax_underline_identifier.json",
        index_weight_file = "index_weight_from_etf.json",
        output_file = "bbg_ticker_for_dividend.json",):
    """
    1) derivatives underline
    2) stocks in "not given index"
    """
    print("Saving bbg_ticker_for_dividend...")
    directory = os.path.join(jsondb_dir, parameter_date)
    deriva_und = pd.read_json(os.path.join(directory, deriva_und_file), orient = "records")
    index_weight = pd.read_json(os.path.join(directory, index_weight_file), orient = "records")
    index_weight['code'] = index_weight['code'].astype(str).str.zfill(6)
    deriva_bbg_not_given = deriva_und[deriva_und['und_bbg'].str.contains("not given")]
    deriva_bbg_given = deriva_und[~deriva_und['und_bbg'].str.contains("not given")]

    not_given_und_codes = deriva_bbg_not_given['und_code'].unique().tolist()
    not_given_idx_weight = index_weight[index_weight['und_code'].isin(not_given_und_codes)]
    # select rows in not_given_idx_weight where isin starts with "KR7" <- 한국 주식
    not_given_idx_weight_KR = not_given_idx_weight[not_given_idx_weight['isin'].str.startswith("KR7")]
    bbg_codes_in_not_given_idx_weight_KR = not_given_idx_weight_KR[['code']]
    bbg_codes_in_not_given_idx_weight_KR['und_code'] = bbg_codes_in_not_given_idx_weight_KR['code']
    bbg_codes_in_not_given_idx_weight_KR['und_bbg'] = not_given_idx_weight_KR['code'].apply(lambda x: x + " KS Equity")
    bbg_codes_in_not_given_idx_weight_KR.rename(columns = {'code': 'bbg_code'}, inplace = True)

    all_bbg_codes = pd.concat(
        [bbg_codes_in_not_given_idx_weight_KR[['und_code', 'und_bbg']], deriva_bbg_given[['und_code', 'und_bbg']]]
    ).drop_duplicates().reset_index(drop=True)

    all_bbg_codes.to_json(os.path.join(directory, output_file), orient = "records")

#if __name__ == "__main__":rhks

#    parameter_date = "20240523"
#    directory = os.path.join(jsondb_dir, parameter_date)
#    pdf_file = os.path.join(directory, "krx_etf_pdf.json")
#    pdf = pd.read_json(pdf_file, orient = "records")