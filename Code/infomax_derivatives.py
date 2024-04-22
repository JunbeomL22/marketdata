from code_config import INFOMAX_HEADER
import requests
import pandas as pd
import xlwings as xw

def get_underline_match(infomax_data):
    #df = infomax_data[infomax_data['is_spread'] != 'Y']
    df = infomax_data
    underline = df['underline'].replace(
        {"코스피200": "KOSPI2",
         "미니코스피": "KOSPI2",
         "코스닥150": "KOSDAQ150",
         "유로스톡스50": "SX5E",
         "미국달러": "USDKRW",
         "엔": "JPYKRW",
         "유로": "EURKRW",
         "위안": "CNYKRW",
         "3개월무위험금리": "KOFR 3M", #KRFRRATE Index
         "변동성지수": "VKOSPI",
         "금": "GoldKRW", #XAUKRW Curncy 
         "에너지화학": "KSP2EC",
         "정보기술": "KSP2IT",
         "금융지수": "KSP2FI",
         "경기소비재": "KSP2CD",
         "고배당50": "KOSPIHDY",
         "배당성장50": "KOSPIGD",
         "건설": "KSP2CM",
         "헬스케어": "KSP2HC",
         "철강소재": "KSP2SM",
         "생활소비재": "KSP2CS",
         "산업재": "KSP2IN",
         "BBIG K-뉴딜": "BBIG K-뉴딜 (배당정보없음)", #unknown
         "2차전지 K-뉴딜": "2차전지 K-뉴딜 (배당정보없음)", #unknown
         "바이오 K-뉴딜": "바이오 K-뉴딜 (배당정보없음)", #unknown
         })
    
    def get_stock_bbg_ticker(type_name, underline, isin):
        if type_name == "개별주식":
            return (isin[3:9] + " KS Equity")
        else:
            return underline
        
    bbg_ticker = df[['underline_type', 'underline', 'underline_isin']].apply(lambda x: get_stock_bbg_ticker(x[0], x[1], x[2]), axis=1)

    bbg_ticker = bbg_ticker.replace(
        {"코스피200": "KOSPI2 Index",
         "미니코스피": "KOSPI2 Index",
         "코스닥150": "KOSDAQ150 Index",
         "유로스톡스50": "SX5E Index",
         "미국달러": "USDKRW Curncy",
         "엔": "JPYKRW Curncy",
         "유로": "EURKRW Curncy",
         "위안": "CNYKRW Curncy",
         "3개월무위험금리": "KRFRRATE Index",
         "변동성지수": "VKOSPI Index",
         "금": "XAUKRW Curncy",
         "에너지화학": "KSP2EC Index",
         "정보기술": "KSP2IT Index",
         "금융지수": "KSP2FI Index",
         "경기소비재": "KSP2CD Index",
         "고배당50": "KOSPIHDY Index",
         "배당성장50": "KOSPIGD Index",
         "건설": "KSP2CM Index",
         "헬스케어": "KSP2HC Index",
         "철강소재": "KSP2SM Index",
         "생활소비재": "KSP2CS Index",
         "산업재": "KSP2IN Index",
         "BBIG K-뉴딜": "unkown",
         "2차전지 K-뉴딜": "unknown",
         "바이오 K-뉴딜": "unknown",
         })
    
    data = {}
    data['krx_und_code'] = df['underline_code'].tolist()
    data['und_isin'] = df['underline_isin'].tolist()
    data['und_name'] = underline.tolist()
    data['und_bbg'] = bbg_ticker.tolist()

    res = pd.DataFrame(data)
    res = res.drop_duplicates(subset='krx_und_code', keep='first')

    return res

def get_fut_info(
        kr_name = "",
        underline = "",
        spread = ""):
    session = requests.Session()
    
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/future/code'

    params = {"kr_name": kr_name,
              "underline": underline,
              "spread": spread
              }
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None

    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception(f'infomax future crawling failed\n\
                        get_fut_info\n\
                        {kr_name}\n\
                        {underline}\n\
                        {spread}\n\
                        {api_url}\n\
                        {params}')
    
    return res

def get_option_info(
        kr_name = "",
        underline = "",
        maturity = "",
        option = "",
        atm = ""):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/option/code'

    params = {"kr_name": kr_name,
              "underline": underline,
              "maturity": maturity,
              "option": option,
              "atm": atm
              }
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()

    res = None

    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception(f'infomax future crawling failed\n\
                        get_option_info\n\
                        {kr_name}\n\
                        {underline}\n\
                        {maturity}\n\
                        {option}\n\
                        {atm}\n\
                        {api_url}\n\
                        {params}')

    return res

def load_option_info(
        wb = None,
        sheet_name = "OptionsInfo",
        output_head = "F15",
        kr_name = "",
        underline = "",
        maturity = "",
        option = "",
        atm = ""):
    if wb is None:
        wb = xw.Book.caller()
    
    ws = wb.sheets[sheet_name]
    option_info = get_option_info(
        kr_name = kr_name,
        underline = underline,
        maturity = maturity,
        option = option,
        atm = atm)
    
    option_info.drop(columns = ['isATM', 'en_name', 'maturity_YYYYMM', 'close_price'], inplace = True)
    option_info['underline'].replace(
        {'코스피 200': 'KOSPI2',
         '미니 코스피': 'KOSPI2',
         '코스피 위클리(목)': 'KOSPI2', 
         '코스피 위클리(월)': 'KOSPI2',
         '코스닥 150': 'KOSDAQ150',
         },
        inplace = True)
    
    ws.range(output_head).options(pd.DataFrame, index = False).value = option_info

def get_fut_past_info(kr_name = "", 
                     type_name = "", 
                     underline = "", 
                     endDate = "", 
                     startDate = "",
                     drop_spread = True):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/future/expired'

    params = {"kr_name": kr_name,
              "type": type_name,
              "underline": underline,
              "endDate": endDate,
              "startDate": startDate
              }

    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception(f'infomax future crawling failed\n\
                        get_fut_info\n\
                        {kr_name}\n\
                        {type_name}\n\
                        {underline}\n\
                        {endDate}\n\
                        {startDate}\n\
                        {api_url}\n\
                        {params}')
    
    if drop_spread:
        res = res[res['spread_near_isin'] == '']

    return res

def get_fut_underline(type_name = "C",
                      name = "",
                      code = ""):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/future/underline'

    params = {"type": type_name,
              "name": name,
              "code": code
              }
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    res = pd.DataFrame(results)

    return res

def get_fut_base_info(codes="", date = "20240405"):
    api_url = 'https://infomaxy.einfomax.co.kr/api/future/info'

    params = {"code": codes,
              "date": date
              }
    
    r = requests.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception(f'infomax future crawling failed\n\
                        get_fut_base_info\n\
                        {codes}\n\
                        {date}\n\
                        {api_url}\n\
                        {params}')
    
    return res

def load_fut_info(wb = None,
                  type_name = "",
                  underline = "",
                  startDate = "",
                  endDate = "",
                  drop_spread = True,
                  sheet_name = "FuturesInfo",
                  output_head = "F15"
                  ):
    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    fut_info = get_fut_past_info(
        kr_name = "",
        type_name = type_name,
        underline = underline,
        startDate = startDate,
        endDate = endDate)
    
    fut_info.drop(columns = ['spread_near_isin',
                             'spread_far_isin',
                             'maturity_YYYYMM',
                             'listed_date'
                             ], 
                  inplace = True)

    ws.range(output_head).options(pd.DataFrame, index = False).value = fut_info

if __name__ == "__main__":
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    load_option_info()
    load_fut_info()
    

    