import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

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
                        
                        res[key_conversion(text)] = "/".join(df['표준코드'].tolist())
                    else:
                        print(f'Table not found for: {text}')
                else:
                    print(f'<dd> element not found for: {text}')
    else:
        print(f'Request failed with status code: {response.status_code}')

    return res