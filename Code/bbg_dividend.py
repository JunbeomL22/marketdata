from xbbg.blp import bdp, bdh, bds
from datetime import datetime
import pandas as pd
import os
from code_config import jsondb_dir

dt = datetime.now().strftime("%Y%m%d")
after_1y = (datetime.strptime(dt, "%Y%m%d") + pd.DateOffset(years = 1)).strftime("%Y%m%d")
parameter_date = "20240523"
ticker_file = "bbg_ticker_for_dividend.json"
output_file = "bbg_div_est.json"

directory = os.path.join(jsondb_dir, parameter_date)

bbg_codes = pd.read_json(os.path.join(directory, ticker_file), orient = "records")

index_codes = bbg_codes[~bbg_codes['und_bbg'].str.endswith("Equity")]['und_bbg'].unique().tolist()
equity_codes = bbg_codes[bbg_codes['und_bbg'].str.endswith("Equity")]['und_bbg'].unique().tolist() 

idx_div = bds(
    tickers = index_codes, 
    flds = ["BDVD_PROJ_DIV_INDX_PTS"], 
    periodicity_override = "D", 
    end_date_override = after_1y)

idx_div = idx_div.loc[idx_div['dividend_(in_index_points)'] > 0.]

idx_div.reset_index(inplace = True)
idx_div.rename(
    columns = {
        'index': 'und_bbg', 
        'dividend_(in_index_points)': 'div_amt',
        'month/year': 'ex_date'}, 
    inplace = True)

equity_div = bds(
    tickers = equity_codes, 
    flds = ["BDVD_ALL_PROJECTIONS"])

equity_div.reset_index(inplace = True)
equity_div.rename(
    columns = {
        'index': 'und_bbg',
        'ex-date': 'ex_date', # 'ex-date' -> 'ex_date
        'amount_per_share': 'div_amt',
    }
)

res = pd.concat([idx_div[['und_bbg', 'ex-date', 'div_amt']], 
                 equity_div[['und_bbg', 'ex-date', 'div_amt']]]).reset_index(drop = True)

res.to_json(os.path.join(directory, ), orient = "records")


