from code_config import INFOMAX_HEADER
import requests
import pandas as pd
import xlwings as xw
from code_config import data_path
from custom_progress import printProgressBar

def get_underline_match(infomax_data):
    df = infomax_data

    def get_result(inp):
        code, isin, name = inp
        """
        returns isin, name, and bbg_ticker
        """
        if name == "유로스톡스50":
            res = code, "EUxxxxxxxx50", "SX5E", "SX5E Index"
        elif name == "미국달러":
            res = code, isin, "USDKRW", "USDKRW Curncy"
        elif name == "엔":
            res = code, isin, "JPYKRW", "JPYKRW Curncy"
        elif name == "유로":
            res = code, isin, "EURKRW", "EURKRW Curncy"
        elif name == "위안":
            res = code, isin, "CNYKRW", "CNYKRW Curncy"
        elif name in ["3개월무위험금리", "3개월무위험지표금리"]:
            res = code, "KRxxxxKOFR3M", "KOFR 3M", "KRFRRATE Index"
        elif name == "변동성지수":
            res = code, isin, "VKOSPI", "VKOSPI Index"
        elif name == "금":
            res = code, isin, "GoldKRW", "XAUKRW Curncy"
        elif name in ("코스피200", "미니코스피", "미니코스피200", "코스피200 위클리"):
            res = code, "KRxxxxxxKSP2", "KOSPI2", "KOSPI2 Index"
        elif name == "코스닥150":
            res = code, "KRxxxKSDQ150", "KOSDAQ150", "KOSDAQ150 Index"
        elif name == "KRX300":
            res = code, "KRxxxxKRX300", "KRX300", "KRX300 Index"
        elif (isin == "KRD020020GV9") or (name == "코스닥 글로벌 지수"):
            res = code, isin, "KOSDAQG", "not given"
        elif (isin == "KRD020020362") or (name == "코스피200 에너지화학 섹터지수"):
            res = code, isin, "에너지화확", "KSP2EC Index"
        elif (isin == "KRD020020370") or (name == "코스피200 정보기술 섹터지수"):
            res = code, isin, "정보기술", "KSP2IT Index"
        elif (isin == "KRD020020388") or (name == "코스피200 금융 섹터지수"):
            res = code, isin, "금융지수", "KSP2FI Index"
        elif (isin == "KRD020020404") or (name == "코스피200 경기소비재 섹터지수"):
            res = code, isin, "경기소비재", "KSP2CD Index"
        elif (isin == "KRD020021329") or (name == "코스피 고배당 50"):
            res = code, isin, "고배당50", "KOSPIHDY Index"
        elif (isin == "KRD020021311") or (name == "코스피 배당성장 50"):
            res = code, isin, "배당성장50", "KOSPIGD Index"
        elif (isin == "KRD020020339") or (name == "코스피200 건설 섹터지수"):
            res = code, isin, "건설", "KSP2CM Index"
        elif (isin == "KRD020020347") or (name == "코스피200 중공업 섹터지수"):
            res = code, isin, "중공업", "KSP2ST Index"
        elif (isin == "KRD020021397") or (name == "코스피200 헬스케어 섹터지수"):
            res = code, isin, "헬스케어", "KSP2HC Index"
        elif (isin == "KRD020020354") or (name == "코스피200 철강소재 섹터지수"):
            res = code, isin, "철강소재", "KSP2SM Index" 
        elif (isin == "KRD020020396") or (name == "코스피200 생활소비재 섹터지수"):
            res = code, isin, "생활소비재", "KSP2CS Index"
        elif (isin == "KRD020021386") or (name == "코스피200 산업재 섹터지수"):
            res = code, isin, "산업재", "KSP2IN Index"
        elif (isin == "KRD020023085") or (name == "KRX BBIG 지수"):
            res = code, isin, "BBIG K-뉴딜", "not given"
        elif (isin == "KRD020023127") or (name == "KRX 2차전지 TOP 10 지수"):
            res = code, isin, "2차전지 TOP 10", "not given"
        elif (isin == "KRD020023119") or (name == "KRX 바이오 TOP 10 지수"):
            res = code, isin, "바이오 TOP 10", "not given"
        elif (isin == "KR7161510003") or (name == "ARIRANG 고배당주"):
            res = code, isin, "ARIRANG 고배당주", "161510 KS Equity"
        elif "국채" in name:
            res = code, isin, name, "not used"
        else:
            res = code, isin, name, isin[3:9] + " KS Equity"
        
        return pd.Series(res)
        
    res = df[['underline_code', 
              'underline_isin', 
              'underline']].apply(get_result, axis = 1)

    res.rename(columns = {
        0: 'krx_und_code',
        1: 'und_isin',
        2: 'und_name',
        3: 'und_bbg'
    }, inplace = True)
    
    new_row1 = pd.DataFrame({
        'krx_und_code': ['04'],
        'und_isin': ['KRxxxxVKOSPI'],
        'und_name': ['VKOSPI'],
        'und_bbg': ['VKOSPI Index']
    })
    new_row2 = pd.DataFrame({
        'krx_und_code': ['AF'],
        'und_isin': ['KRxxxxxxKSP2'],
        'und_name': ['KOSPI2'],
        'und_bbg': ['KOSPI2 Index']
    })
    
    res = pd.concat([res, new_row1, new_row2])

    res.drop_duplicates(subset = 'krx_und_code', inplace = True)


    return res

def get_fut_info(
        kr_name = "",
        underline = "",
        spread = "",
        size = 5000,
        ):
    session = requests.Session()
    
    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/future/code'

    params = {"kr_name": kr_name,
              "underline": underline,
              "spread": spread,
              "_size": size,
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
        atm = "", 
        size = 1000):
    session = requests.Session()

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/option/code'

    params = {"kr_name": kr_name,
              "underline": underline,
              "maturity": maturity,
              "option": option,
              "atm": atm,
              "_size": size,
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

def get_connected_fut(
        underline = "",
        start_date = "",
        end_date = "",
    ):
    session = requests.Session()
    

    session.verify = False
    api_url = 'https://infomaxy.einfomax.co.kr/api/future/active'

    params = {"underline": underline,
              "startDate": start_date,
              "endDate": end_date
              }
    
    r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

    success, results = r.json().values()
    res = None
    if success:
        res = pd.DataFrame(results)
    else:
        raise Exception(f'infomax future crawling failed\n\
                        get_connected_fut\n\
                        {underline}\n\
                        {start_date}\n\
                        {end_date}\n\
                        {api_url}\n\
                        {params}')
    
    return res

def load_all_connected_future(
        start_date = "",
        end_date = "",
        basis_type = "underline_basis",
        derivatives_file = "derivatives_base_data.json",
        wb = None,
        sheet_name = "FindETF",
        output_head = "K4",
        ):
    # - 
    derivatives = pd.read_json(f'{data_path}/{derivatives_file}', orient='records')
    derivatives = derivatives[~derivatives['option_type'].str.contains('옵션')]
    all_krx_codes = derivatives['krx_und_code'].unique().tolist()
    name_match = dict(zip(derivatives['krx_und_code'], derivatives['und_name']))

    res = []
    N = len(all_krx_codes)
    for underline in all_krx_codes:
        connected_fut = get_connected_fut(
            underline = underline,
            start_date = start_date,
            end_date = end_date
        )
        printProgressBar(
            all_krx_codes.index(underline) + 1,
            N,
            prefix = 'connected future crawling: ',
            suffix = f'complete', length = 20
        )
        if len(connected_fut) == 0:
            continue

        v = connected_fut.set_index('date').sort_index(ascending=False)
        v = v[basis_type]/v['theoretical_price']
        v = pd.DataFrame(v, columns = [f'{name_match[underline]} {(underline)}'])
        res.append(v)
    
    res = pd.concat(res, axis = 1)

    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    ws.range(output_head).options(pd.DataFrame, index = True).value = res
        
load_all_connected_future(start_date="20230901", end_date="20240315")
if __name__ == "__main__":
    xw.Book('D:/Projects/marketdata/MarketData.xlsm').set_mock_caller()
    load_option_info()
    load_fut_info()
    

    