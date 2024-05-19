import requests
import pandas as pd
import xml.etree.ElementTree as ET
from time import sleep, time
from utils import time_format
from code_config import jsondb_dir
import os

def get_seibro_etf_creation(
    start_date = "20240502",
    end_date = "20240502",
    page_num = 2,):

    url = 'https://seibro.or.kr/websquare/engine/proworks/callServletService.jsp'

    referer = 'https://seibro.or.kr/websquare/control.jsp?w2xPath=/IPORTAL/user/etf/BIP_CNTS06026V.xml&menuNo=176'

    df_list = []
    for i in range(1, page_num + 1):
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

    if len(df_list) == 0:
        return None
    res = pd.concat(df_list)
    res.drop_duplicates('ISIN', inplace=True)

    res.rename(
        columns={
            'SETUP_CU_QTY': '설정',
            'RP_CU_QTY': '환매',
        },
        inplace=True
    )
    res['설정'] = res['설정'].str.replace(',', '').str.zfill(1).astype(float)
    res['환매'] = res['환매'].str.replace(',', '').str.zfill(1).astype(float)
    return res

def get_etf_creation(
        parameter_date = "20240503",
        start_date = "20240503",
        end_date = "20240503",
        page_num = 2,
        file_name = 'etf_base_data.json',):
    directory = os.path.join(jsondb_dir, parameter_date)
    file_name = os.path.join(directory, file_name)
    # check the file exsitence
    if not os.path.exists(os.path.join(directory, file_name)):
        msg = f'''
        The file {file_name} does not exist.\n
        Seibro data does not have nav and creation unit data.
        The base file must be cached in advance
        '''
        raise Exception(msg)
    
    base_data = pd.read_json(file_name)
    seibro_data = get_seibro_etf_creation(
        start_date = start_date,
        end_date = end_date,
        page_num = page_num,)
    
    if seibro_data is None:
        return None
    
    seibro_data.rename(
        columns={
            'ISIN': 'isin',
        },
        inplace=True
    )
     
    seibro_data = seibro_data.merge(base_data, on='isin', how='left')
    seibro_data['설정대금'] = seibro_data['설정'] * seibro_data['nav'] * seibro_data['creationunit'] / 100000000.
    seibro_data['환매대금'] = seibro_data['환매'] * seibro_data['nav'] * seibro_data['creationunit'] / 100000000.

    return seibro_data
    
def get_seibro_etf_dividend(
        start_date = "20240401",
        end_date = "20240631",
        dividend_type = "이익분배",
        sleep_time = 5,):
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
        print(f'Sleeping for {sleep_time} seconds...')
        sleep(sleep_time)

    res = pd.concat(df_list)
    res.drop_duplicates('ISIN', inplace=True)

    return res

def get_seibro_stock_dividend(
        start_date = "20240330",
        end_date = "20240505",
        sleep_time = 5,):
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
        print(f'Sleeping for {sleep_time} seconds...')
        sleep(sleep_time)

        df = pd.DataFrame(data_list)

        df_list.append(df)

    res = pd.concat(df_list)

    res.drop_duplicates(['SHOTN_ISIN', 'KOR_SECN_NM'], inplace=True)

    return res

def get_seibro_dividend(
        start_date = "20240330",
        end_date = "20240505",
        etf_dividend_type = "이익분배",
        sleep_time = 5,):

    res1 = get_seibro_stock_dividend(
        start_date = start_date,
        end_date = end_date,
        sleep_time = sleep_time,)

    res1.rename(
        columns = {
            'SHOTN_ISIN': 'code',
            'KOR_SECN_NM': 'name',
            'RGT_STD_DT': 'dividend_date',
            'TH1_PAY_TERM_BEGIN_DT': 'payment_date',
            'RGT_RSN_DTAIL_SORT_NM': 'dividend_type',
            'ESTM_STDPRC': 'dividend_amount',
        },
        inplace=True
    )

    res2 = get_seibro_etf_dividend(
        start_date = start_date,
        end_date = end_date,
        dividend_type = etf_dividend_type,
        sleep_time = sleep_time,)

    res2.rename(
        columns = {
            'ISIN': 'isin',
            'KOR_SECN_NM': 'name',
            'RGT_STD_DT': 'dividend_date',
            'TH1_PAY_TERM_BEGIN_DT': 'payment_date',
            'RGT_RSN_DTAIL_NM': 'dividend_type',
            'ESTM_STDPRC': 'dividend_amount',
        },
        inplace = True
    )

    stock_div = res1[['code', 'name', 'dividend_date', 'payment_date', 'dividend_type', 'dividend_amount']].copy()
    etf_div = res2[['isin', 'name', 'dividend_date', 'payment_date', 'dividend_type', 'dividend_amount']].copy()

    stock_div['isin'] = ''
    etf_div['code'] = ''

    result = pd.concat([stock_div, etf_div])[['isin', 'code', 'name', 'dividend_date', 'payment_date', 'dividend_type', 'dividend_amount']]

    result = result.reset_index().drop(columns = ['index'])

    return result

