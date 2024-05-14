from pykrx.website import krx
from custom_progress import printProgressBar
from code_config import jsondb_dir
from bs4 import BeautifulSoup
from time import sleep, time
from utils import time_format
import pandas as pd
import requests
import re

def get_krx_derivative_data(
        sleep_time = 1,
        ):
    ders = krx.future.core.파생상품검색().fetch()
    class_names = ders.index.tolist()

    worker = krx.future.core.전종목기본정보()
    df_list = []
    N = len(class_names)
    st = time()
    for i, name in enumerate(class_names):
        df_list.append(worker.fetch(prodId = name))
        sleep(sleep_time)
        printProgressBar(
            i, N, 
            prefix = 'Progress:', 
            suffix = f'Complete ({time_format(time() - st)} elapsed)',
            length = 20)

    res = pd.concat(df_list)
    res.reset_index(drop=True, inplace=True)
    return res

def key_conversion(key):
    return key.replace(" ", "").replace("년", "").replace("월물", "").replace("최종결제기준채권", "")

def get_ktbf_underline(
        fut_type = "3년국채"):
    url = ''
    if fut_type == "3년국채":
        url = 'https://open.krx.co.kr/contents/OPN/01/01040501/OPN01040501.jsp'
    elif fut_type == "5년국채":
        url = 'https://open.krx.co.kr/contents/OPN/01/01040502/OPN01040502.jsp'
    elif fut_type == "10년국채":
        url = 'https://open.krx.co.kr/contents/OPN/01/01040503/OPN01040503.jsp'
    elif fut_type == "30년국채":
        url = 'https://open.krx.co.kr/contents/OPN/01/01040506/OPN01040506.jsp'
    else:
        raise ValueError(f"Invalid fut_type: {fut_type}")

    response = requests.get(url, verify=False)
    res = {}
    if response.status_code == 200:
        # Create a BeautifulSoup object to parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all the <dt> elements
        dt_elements = soup.find_all('dt')
        
        # Iterate over the <dt> elements and extract the desired information
        for dt in dt_elements:
            # Check if the <dt> element matches the specific format
            if re.match(r'\d{4}년 \d{2}월물 최종결제기준채권', dt.text.strip()):
                # Extract the text from the <dt> element
                text = dt.text.strip()
                
                # Find the next <dd> element (sibling of <dt>)
                dd = dt.find_next_sibling('dd')
                
                if dd:
                    # Find the table within the <dd> element
                    table = dd.find('table')
                    
                    if table:
                        # Convert the table to a DataFrame
                        df = pd.read_html(str(table))[0]
                        
                        res[key_conversion(text)] = ",".join(df['표준코드'].tolist())
                    else:
                        print(f'Table not found for: {text}')
                else:
                    print(f'<dd> element not found for: {text}')
    else:
        print(f'Request failed with status code: {response.status_code}')

    return res


def get_krx_derivatives_last_trade_time():
    res = {
        "채권(Bond)": "11:30:00", # 3년국채
        "금리(Interest Rates)": "15:45:00", # 3개월무위험금리
        "통화(Currency)": "11:30:00", # 달러
        "일반상품(Commodity)": "11:30:00", # 금
        "주권(Equity)": "15:20:00", # 삼성전자
        "지수(Index)": "15:20:00", # 코스피200
        "글로벌지수(Global Index)": "15:20:00", # 유로스톡스50
    }

    df = pd.DataFrame(list(res.items()), columns=['category', 'time'])

    return df


    