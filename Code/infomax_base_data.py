import requests
import pandas as pd
from code_config import INFOMAX_HEADER
import xlwings as xw
from seibro_data import get_etf_creation
from custom_progress import printProgressBar
from utils import time_format
from time import time
# - 
# -
def get_etf_info(codes):
    session = requests.Session()
    
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf'

    params = {"code": codes}
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)
    success, results = r.json().values()

    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception('infomax crawling failed')

    return res    



def get_etf_pdf(code = "069500", 
                date = "",
                sort = 'value'):
    session = requests.Session()
    # SSL 인증 처리 무효화
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/etf/port'
    
    params = {"code": code,
              "date": date,
              "sort": sort
              }
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    
    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception('infomax cr awling failed')
    
    return res

def get_index_list(type_code = ''):
    """
    (K:코스피, Q: 코스닥, X: KRX, F: 선물/옵션, G: Global&other, T: 일반상품&etc. M: 멀티에셋, N: 코넥스)
    """
    session = requests.Session()
    # SSL 인증 처리 무효화
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/index/code'
    
    params = {"type": type_code,
              "kr_name":"",
              "en_name":"",
              "code":""}
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)
    
    success, results = r.json().values()
    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception(f'infomax index crawling failed\n\
                        get_index_list\n\
                        {type_code}\n\
                        {api_url}\n\
                        {params}')
    return res

def get_index_pdf(code = ''):
    session = requests.Session()
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/index/constituents'

    params = {"code": code}

    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception(f'infomax index crawling failed\n\
                        get_index_pdf\n\
                        {code}\n\
                        {api_url}\n\
                        {params}')
    return res

def get_bond_info(isin_codes):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/bond/basic_info'

    df_list = []
    for code in isin_codes:
        params = {"stdcd": code}
        r = session.get(api_url, params = params, headers = INFOMAX_HEADER)
        success, results = r.json().values()
        
        if success:
            df_list.append(pd.DataFrame(results))
    
    res = pd.concat(df_list)

    return res

def get_security_base_info(search = "",
                            code = "",
                            name = "",
                            isin = "",
                            market = "",
                            dt = "",
                            type_name = ""):
    
    session = requests.Session()
    
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/code'

    params = {"search": search,
                "code": code,
                "name": name,
                "isin": isin,
                "market": market,
                "date": dt,
                "type": type_name}
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception('infomax crawling failed')
    
    return res
    
def get_expired(
        name ="",
        type_name = "",
        code = "",
        end_date = "",
        start_date = ""):
    session = requests.Session()
    
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/expired'

    params = {
        "name": name,
        "type": type_name,
        "code": code,
        "endDate": end_date,
        "startDate": start_date
    }
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None

    if success:
        res = pd.DataFrame(results)

    else:
        raise Exception('get_expired infomax crawling failed')
    
    return res

def get_list(
        date = 20240430,
        market = '',
        type_name = 'EF',
        rank = 'trading',):
    """
    market: str [1:거래소 2:거래소 기타 5:KRX 7:코스닥 8:코스닥 기타] 미입력시 전체
    type_name:str [ST:주식, MF:뮤추얼종목, RT:리츠, SC:선박투자회사, IF:인프라투융자회사, DR:예탁증서 , SW:신주인수권증권, SR:신주인수권증서, EW:주식워런트증권(ELW), EF:상장지수펀트(ETF), BC:수익증권, FE:해외ETF, FS:해외원주]
    date: int [조회 일자 (YYYYMMDD), 미입력시 today-1]
    rank:str [정렬 기준 (디폴트: 등락률), [등락률(rate), 시가총액(cap, marketcap), 거래대금(trading_value, trading), 거래량(trading_vol, vol, volume), 가격(price, close)]]
    """
    session = requests.Session()
    session.verify = False

    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/rank'

    params = {
        "date": date,
        "market": market,
        "type": type_name,
        "rank": rank
    }

    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None

    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception('infomax crawling failed')

    res.drop(
        columns = ['open_price', 'high_price', 'low_price', 'close_price', 'change', 'trading_volume'],
        inplace = True
        )
    
    res['marketcap'] = res['marketcap'].div(100000000.0)
    res['trading_value'] = res['trading_value'].div(100000000.0)

    return res

def load_list(
        wb = None,
        sheet_name = 'List',
        date = 20240430,
        market = '',
        type_name = 'EF',
        rank = 'trading',
        #-
        start_date = "20240401",
        end_date = "20240930",
        investor = "1000,8000",
        num_code = 20,
        num_page = 2,
        base_file_date = "20240430",
        file_name = 'etf_base_data.json',
        output_head = 'G5'):
    
    date = int(date)
    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    res = get_list(
        date = date, 
        market = market, 
        type_name = type_name,
        rank = rank,
        )

    num_code = int(num_code)
    if num_code > 0:
        codes = res['code'].str.zfill(6).head(num_code).tolist()
        investor_list = []
        N = len(codes)
        st = time()
        for i, code in enumerate(codes):
            try:
                investor_df = get_investor(
                    code = code,
                    investor = investor,
                    start_date = start_date,
                    end_date = end_date
                )
                if len(investor_df) == 0:
                    print(f'No data retrieved for {code}')
                    continue
            except Exception as e:
                print(f'An error occurred with ticker {code}: {str(e)}')

            investor_df['ask_value'] = investor_df['ask_value'].div(100000.0)
            investor_df['bid_value'] = investor_df['bid_value'].div(100000.0)
            
            investor_df = investor_df.groupby('investor')[['ask_value', 'bid_value']].sum().reset_index()
            investor_df.rename(
                columns = {
                    'ask_value': f'매도',
                    'bid_value': f'매수'
                },
                inplace = True
            )
            # flatten investor dataframe such as
            # {investor_value}ask_value, {investor_value}bid_value, so num(distinct(investor)) * 2 columns
            investor_df = investor_df.pivot(columns='investor')
            investor_df.columns = [f'{col[1]}_{col[0]}' for col in investor_df.columns]
            investor_df = pd.DataFrame(investor_df.fillna(0.0).sum()).T
            investor_df['code'] = code
            
            investor_list.append(pd.DataFrame(investor_df))

            printProgressBar(
                i + 1, 
                N, 
                prefix = 'Progress:',
                suffix = f'Complete, Elapsed time: {time_format(time() - st)}',
                length = 20
            )
                             
        if len(investor_list) > 0:
            investor_df = pd.concat(investor_list)
            res = res.merge(investor_df, on = 'code', how = 'left')

    seibro_data = get_etf_creation(
        parameter_date = base_file_date,
        start_date = start_date,
        end_date = end_date,
        page_num = num_page,
        file_name = file_name,
    )

    if seibro_data is not None:
        res = res.merge(
            seibro_data[['isin', '설정대금', '환매대금']], 
            on = 'isin', 
            how = 'left')
        
    ws.range(output_head).options(pd.DataFrame, index = False).value = res

def get_investor(
        code = "",
        investor = "",
        end_date = "",
        start_date = "",):
    """
    investor: str
    
    [T010: 기관계, 1000: 증권(금융투자), 2000: 보험, 3000: 투자신탁, 3100: 사모펀드, 
    4000: 은행, 5000: 종금/저축(기타금융), 6000: 연기금, 
    7000: 미분류(정부), 7100: 기타법인, 8000: 개인, 
    9000: 외국인합, 9001: 외국인(금감원 투자등록 ID 보유 외국인), 9002: 기타 외국인(금감원 투자등록 ID 미보유 외국인)]

    복수 선택 가능: "," 로 구분
    """

    session = requests.Session()
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/stock/investor'

    params = {"code": code, 
              "investor": investor,
              "endDate": end_date,
              "startDate": start_date
              }
              

    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None

    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception(f'get_investor infomax crawling failed {results}')
    
    return res

if __name__ == '__main__':
    xw.Book("D:/Projects/marketdata/MarketData.xlsm").set_mock_caller()
    load_list(rank = 'trading')