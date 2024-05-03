import requests
import pandas as pd
import xml.etree.ElementTree as ET
from time import sleep, time
from utils import time_format
from code_config import jsondb_dir


def get_seibro_etf_creation(
    start_date = "20240502",
    end_date = "20240502",
    page_num = 2,):

    url = 'https://seibro.or.kr/websquare/engine/proworks/callServletService.jsp'

    referer = 'https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/etf/BIP_CNTS06026V.xml&menuNo=176'

    df_list = []
    for i in range(1, page_num):
        start_page = 30*(i-1) + 1
        end_page = 30*i
        data = f'''
        <reqParam action="secnBySetredStatPList" task="ksd.safe.bip.cnts.etf.process.EtfSetredInfoPTask">
            <MENU_NO value="176"/>
            <CMM_BTN_ABBR_NM value="allview,allview,print,hwp,word,pdf,searchIcon,seach,xls,searchIcon,seach,xls,link,link,wide,wide,top,"/>
            <W2XPATH value="/IPORTAL/user/etf/BIP_CNTS06026V.xml"/>
            <etf_sort_level_cd value=""/>
            <etf_big_sort_cd value=""/>
            <mngco_custno value=""/>
            <fromDt value="{start_date}"/>
            <toDt value="{end_date}"/>
            <START_PAGE value="{start_page}"/>
            <END_PAGE value="{end_page}"/>
        </reqParam>
        '''

        headers = {'Referer': referer}
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
        
        print(f'The data in page-{i} is collected. Sleep for 5 seconds...')
        sleep(5)
        
        df = pd.DataFrame(data_list)
        df_list.append(df)

    res = pd.concat(df_list)
    res.drop_duplicates('ISIN', inplace=True)

    res.rename(
        columns={
            'SETUP_CU_QTY': '설정',
            'RP_CU_QTY': '환매',
        },
        inplace=True
    )

    return res

def get_etf_creation(
        start_date = "20240502",
        end_date = "20240502",
        page_num = 2,
        parameter_date = "20240502",
        file_name = 'etf_base_data.json',):
    directory = os.path.join(jsondb_dir, parameter_date)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
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

        st = time()
        response = requests.post(url, headers=headers, data=data, verify=False)
        print(f'The page-{i} is processed. Time: {time_format(time() - st)}')

        xml_data = response.text
        root = ET.fromstring(xml_data)
        
        st = time()
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

        print(f'The data in page-{i} is collected. Time: {time_format(time() - st)}')
        print('Sleeping for 5 seconds...')
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

def get_seibro_stock_dividend(
        start_date = "20240330",
        end_date = "20240505",):
    url = 'https://seibro.or.kr/websquare/engine/proworks/callServletService.jsp'

    # Set the headers
    headers = {
        'Referer': 'https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/company/BIP_CNTS01041V.xml&menuNo=285'
    }

    df_list = []
    for i in range(1, 1000):
        start_page = 15*(i-1) + 1
        end_page = 15*i
        data = f'''
        <reqParam action="divStatInfoPList" task="ksd.safe.bip.cnts.Company.process.EntrFnafInfoPTask">
            <RGT_STD_DT_FROM value="{start_date}"/>
            <RGT_STD_DT_TO value="{end_date}"/>
            <ISSUCO_CUSTNO value=""/>
            <KOR_SECN_NM value=""/>
            <SECN_KACD value=""/>
            <RGT_RSN_DTAIL_SORT_CD value=""/>
            <LIST_TPCD value=""/>
            <START_PAGE value="{start_page}"/>
            <END_PAGE value="{end_page}"/>
            <MENU_NO value="285"/>
            <CMM_BTN_ABBR_NM value="allview,allview,print,hwp,word,pdf,searchIcon,seach,xls,link,link,wide,wide,top,"/>
            <W2XPATH value="/IPORTAL/user/company/BIP_CNTS01041V.xml"/>
        </reqParam>
        '''

        st = time()
        response = requests.post(url, headers=headers, data=data, verify=False)
        print(f'The page-{i} is processed. Time: {time_format(time() - st)}')
        xml_data = response.text
        root = ET.fromstring(xml_data)

        st = time()
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

        print(f'The data in page-{i} is collected. Time: {time_format(time() - st)}')
        print('Sleeping for 5 seconds...')
        sleep(5)

        df = pd.DataFrame(data_list)

        df_list.append(df)

    res = pd.concat(df_list)

    res.drop_duplicates(['SHOTN_ISIN', 'KOR_SECN_NM'], inplace=True)

    return res

