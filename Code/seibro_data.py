import requests
import pandas as pd
import xml.etree.ElementTree as ET
from time import sleep

def get_seibro_etf_dividend(
        start_date = "20240401",
        end_date = "20240631",
        dividend_type = "이익분배",):
    url = 'https://seibro.or.kr/websquare/engine/proworks/callServletService.jsp'

    # Set the headers
    headers = {
        'Referer': 'https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/etf/BIP_CNTS06030V.xml&menuNo=179'
    }

    if dividend_type == "이익분배":
        rgt_rsn_dtail_sort_cd = "11"
    else:
        rgt_rsn_dtail_sort_cd = ""
    
    df_list = []
    for i in range(1, 1000):
        start_page = 30*(i-1) + 1
        end_page = 30*i
        data = f'''
        <reqParam action="exerInfoDtramtPayStatPlist" task="ksd.safe.bip.cnts.etf.process.EtfExerInfoPTask">
            <MENU_NO value="179"/>
            <CMM_BTN_ABBR_NM value="allview,allview,print,hwp,word,pdf,searchIcon,searchIcon,seach,searchIcon,seach,link,link,wide,wide,top,"/>
            <W2XPATH value="/IPORTAL/user/etf/BIP_CNTS06030V.xml"/>
            <etf_sort_level_cd value="0"/>
            <etf_big_sort_cd value=""/>
            <START_PAGE value="{start_page}"/>
            <END_PAGE value="{end_page}"/>
            <etf_sort_cd value=""/>
            <isin value=""/>
            <mngco_custno value=""/>
            <RGT_RSN_DTAIL_SORT_CD value="{rgt_rsn_dtail_sort_cd}"/>
            <fromRGT_STD_DT value="{start_date}"/>
            <toRGT_STD_DT value="{end_date}"/>
        </reqParam>
        '''

        response = requests.post(url, headers=headers, data=data, verify=False)
        xml_data = response.text
        root = ET.fromstring(xml_data)
        
        data_list = []
        for data in root.findall('data'):
            result = data.find('result')
            data_dict = {}
            for child in result:
                data_dict[child.tag] = child.get('value')
            if len(data_dict) > 0:
                data_list.append(data_dict)
        if len(data_list) == 0:
            break
        df = pd.DataFrame(data_list)
        df_list.append(df)

        print(f'{i} pages are processed. Sleeping for 5 seconds...')
        sleep(5)

    res = pd.concat(df_list)
    res.drop_duplicates('ISIN', inplace=True)
    res.rename(
        columns={
            "ISIN": "isin",
            "KOR_SECN_NM": "name",
            "RGT_STD_DT": "dividend_date",
            "TH1_PAY_TERM_BEGIN_DT": "payment_date",
            "ESTM_STDPRC": "dividend_amount",
            "RGT_RSN_DTAIL_NM": "dividend_type",
            },
        inplace=True
    )
    res = res[['isin', 'name', 'dividend_date', 'payment_date', 'dividend_amount', 'dividend_type']]

    return res

url = 'https://seibro.or.kr/websquare/engine/proworks/callServletService.jsp'

# Set the headers
headers = {
    'Referer': 'https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/company/BIP_CNTS01041V.xml&menuNo=285'
}

data = '''
<reqParam action="divStatInfoPList" task="ksd.safe.bip.cnts.Company.process.EntrFnafInfoPTask">
    <RGT_STD_DT_FROM value="20240330"/>
    <RGT_STD_DT_TO value="20240430"/>
    <ISSUCO_CUSTNO value=""/>
    <KOR_SECN_NM value=""/>
    <SECN_KACD value=""/>
    <RGT_RSN_DTAIL_SORT_CD value=""/>
    <LIST_TPCD value=""/>
    <START_PAGE value="1"/>
    <END_PAGE value="15"/>
    <MENU_NO value="285"/>
    <CMM_BTN_ABBR_NM value="allview,allview,print,hwp,word,pdf,searchIcon,seach,xls,link,link,wide,wide,top,"/>
    <W2XPATH value="/IPORTAL/user/company/BIP_CNTS01041V.xml"/>
</reqParam>
'''

response = requests.post(url, headers=headers, data=data, verify=False)
xml_data = response.text
root = ET.fromstring(xml_data)

df_list = []
data_list = []
for data in root.findall('data'):
    result = data.find('result')
    data_dict = {}
    for child in result:
        data_dict[child.tag] = child.get('value')
    if len(data_dict) > 0:
        data_list.append(data_dict)

df = pd.DataFrame(data_list)

df_list.append(df)

res = pd.concat(df_list)

res.drop_duplicates(['SHOTN_ISIN', 'KOR_SECN_NM'], inplace=True)