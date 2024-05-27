from xbbg.blp import bdp, bdh, bds
from datetime import datetime
from code_config import jsondb_dir, serverdb_dir
from custom_progress import printProgressBar
from utils import time_format
from time import time
import pandas as pd
import os
import argparse

def save_bbg_div_est(
        parameter_date = "20240523",
        end_year_offset = 1,
        equity_crawl_split_num = 10,
        ticker_file = "bbg_ticker_for_dividend.json",
        output_file = "bbg_div_est.json"):
    dt = datetime.now().strftime("%Y%m%d")
    end_date_override = (datetime.strptime(dt, "%Y%m%d") + pd.DateOffset(years = end_year_offset)).strftime("%Y%m%d")

    directory = os.path.join(serverdb_dir, parameter_date)

    bbg_codes = pd.read_json(os.path.join(directory, ticker_file), orient = "records")

    index_codes = bbg_codes[~bbg_codes['und_bbg'].str.endswith("Equity")]['und_bbg'].unique().tolist()
    equity_codes = bbg_codes[bbg_codes['und_bbg'].str.endswith("Equity")]['und_bbg'].unique().tolist() 

    idx_div = bds(
        tickers = index_codes, 
        flds = ["BDVD_PROJ_DIV_INDX_PTS"], 
        periodicity_override = "D", 
        end_date_override = end_date_override)

    idx_div = idx_div.loc[idx_div['dividend_(in_index_points)'] > 0.]

    idx_div.reset_index(inplace = True)
    idx_div.rename(
        columns = {
            'index': 'und_bbg', 
            'dividend_(in_index_points)': 'div_amt',
            'month/year': 'ex_date'}, 
        inplace = True)

    idx_div['payment_date'] = ''
    print('idnex dividend done')
    # split equity_codes in 10 with custom_progress_bar
    equity_div_list = []
    n_code = len(equity_codes)
    chop = list(range(0, n_code, equity_crawl_split_num))
    if n_code not in chop:
        chop.append(n_code)
    
    tasks = list(zip(chop[:-1], chop[1:]))
    st = time()
    for bg, ed in tasks:
        codes = equity_codes[bg:ed]
        divs = bds(
            tickers = codes,
            flds = ["BDVD_ALL_PROJ_WITH_PAY_DT"])
        
        if len(divs) > 0:
            equity_div_list.append(divs)

        printProgressBar(
            ed, n_code, 
            prefix = "Progress:", 
            suffix = f'Complete, Time: {time_format(time() - st)}', 
            length = 20)

    equity_div = pd.concat(equity_div_list)
    equity_div.reset_index(inplace = True)
    equity_div.rename(
        columns = {
            'index': 'und_bbg',
            'ex-date': 'ex_date', # 'ex-date' -> 'ex_date
            'amount_per_share': 'div_amt',
            'projected_pay_date': 'payment_date',
        },
        inplace = True)
    equity_div['payment_date'] = pd.to_datetime(equity_div['payment_date'])
    equity_div['payment_date'] = equity_div['payment_date'].dt.strftime("%Y%m%d")

    # Python
    frames = []
    
    if not idx_div.empty:
        frames.append(idx_div[['und_bbg', 'ex-date', 'div_amt']])
    
    if not equity_div.empty:
        frames.append(equity_div[['und_bbg', 'ex-date', 'div_amt']])
    
    res = pd.concat(frames).reset_index(drop=True)

    res['ex_date'] = pd.to_datetime(res['ex_date']).dt.strftime("%Y%m%d")

    res.to_json(os.path.join(directory, output_file), orient = "records")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('parameter_date', type=str, help='The parameter date')
    parser.add_argument('end_year_offset', type=int, help='The end year offset')
    parser.add_argument('equity_crawl_split_num', type=int, help='The equity crawl split number')
    #parser.add_argument('ticker_file', type=str, help='The ticker file')
    #parser.add_argument('output_file', type=str, help='The output file')
    args = parser.parse_args()
    save_bbg_div_est(args.parameter_date, args.end_year_offset, args.equity_crawl_split_num)
    # python bbg_dividend.py 20240523 1 10 bbg_ticker_for_dividend.json bbg_div_est.json