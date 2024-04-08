import xlwings as xw
import pandas as pd
import code_config
import re
from datetime import datetime

def load_etf_info(wb = None, 
                   sheet_name = 'BaseInfo',
                   file_name = 'etf_base_info.json',
                   etf_info_file_name = 'full_etf_info.csv',
                   output_range = 'G3:H5000'):
    # -    
    if wb is None:
        wb = xw.Book.caller()
    
    df = pd.read_json(code_config.data_path + file_name)
    info_df = pd.read_csv(code_config.data_path + etf_info_file_name)
    res = df.merge(info_df, on='code', how='left')

    #def notional_parser(z):
    #    if not isinstance(z, str):
    #        return z
    #    elif bool(re.match('^[1-9].*원$', z)):
    #        return int(re.sub('(조|억|원|,)', '', z) )
    #    else:
    #        return z
    #res['market cap'] = res['market cap'].apply(notional_parser)

    res['cu'] = res['creationunit']
    res.drop(columns=['market cap'], inplace=True)
    res.rename(columns = {'net_asset': 'market cap'}, inplace = True)
    res['market cap'] = res['market cap'].astype(float) / 100000000.0
    res = res.sort_values(by='market cap', ascending=False)
    res.drop(columns=['creationunit', 'listed_shares', 'nav', 'issuer'], inplace=True)
    
    def ter_parser(z):
        if not isinstance(z, str):
            return z
        elif bool(re.match('^연.*%$', z)):
            return 100.0*float(re.sub('(%|연)', '', z) )
        else:
            return z
    
    res['ter'] = res['ter'].apply(ter_parser)
    res.rename(
        columns = {'ter': 'ter(bp)'}, 
        inplace = True)

    def issue_date_parser(z):
        if not isinstance(z, str):
            return z
        elif bool(re.match('^[1-9].*일$', z)):
            return datetime.strptime(z, '%Y년 %m월 %d일')
        else:
            return z
    
    res['issue date'] = res['issue date'].apply(issue_date_parser)

    ws = wb.sheets[sheet_name]

    ws.range(output_range).clear_contents()

    res.drop_duplicates('code', inplace=True)
    #res.sort_values(by='code', inplace=True, ascending=False)
    res['code'] = res['code'].apply(lambda z: f'0{z}' if len(str(z)) == 5 else str(z))
    
    ws.range(output_range).options(pd.DataFrame, index = False).value = res

if __name__ == "__main__":
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    load_etf_info()
