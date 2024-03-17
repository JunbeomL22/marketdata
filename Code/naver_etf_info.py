import numpy as np
import csv
import urllib.request
from bs4 import BeautifulSoup
import json
import pandas as pd
import time
import math
import config

def save_naver_finance_etf_info(tickers,
                                prev_list_to_skip = [],
                                use_prev_data = True,
                                output_file_name = 'etf_base_info.csv'):

    write_type = 'a' if use_prev_data else 'w'
    f = open(config.data_path+output_file_name, write_type, encoding = 'utf-8', newline = '')
    wr = csv.writer(f)

    if not use_prev_data:
        wr.writerow(['ticker', 'market cap', 'type', 'issue date', 'ter', 'issuer'])
    count = 0

    #import pdb;pdb.set_trace()
    try:
        for code in tickers:
            if code in prev_list_to_skip:
                continue

            N = len(str(code))
            zero_patch = ''.join(['0' for _ in range(max(6-N, 0))])
            url_code = zero_patch + str(code)                
            each_url = f'https://finance.naver.com/item/main.nhn?code={url_code}'
            each_data = urllib.request.urlopen(each_url).read().decode('CP949')
            soup = BeautifulSoup(each_data)
            
            if soup.body is None:
                continue

            soup1 = soup.body.find('table', summary = '시가총액 정보')
            if soup1 is None:
                continue
            info1 = soup1.find_all('em')
            
            soup2 = soup.body.find('table', summary = '기초지수 정보')
            if soup2 is None:
                continue
            info2 = soup2.find_all('td')

            soup3 = soup.body.find('table', summary = '펀드보수 정보')
            if soup3 is None:
                continue
            info3 = soup3.find_all('td')
            
            info_all = [
                url_code,
                info1[0].get_text(strip=True).replace('\t', '').replace('\n', '') + '억원',
                info2[1].get_text(),
                info2[2].get_text(),
                info3[0].get_text(),
                info3[1].get_text()
            ]
            print(f'{count} : {" | ".join(info_all)}')
            wr.writerow(info_all)
            count += 1
            time.sleep(0.2)
    except:
        print('Exception happend. The output file closed')
        f.close()

    f.close()
    print(f'{count} etf information was retrived')

