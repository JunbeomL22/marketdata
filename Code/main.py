import requests
import json
from pandas.io.json import json_normalize
import pandas as pd
import io
#url = 'https://testoap.k-mydata.org/v3/market/extra/stocks/kospi/069500/pdf'
#json_data = json.loads(requests.get(url, verify=False).text)
#df = json_normalize(json_data['result']['etfItemList'])

url_naver = 'https://navercomp.wisereport.co.kr/v2/ETF/index.aspx?cmp_cd='+'153130'
req = requests.get(url_naver, verify=False)
#json_data_naver = json.loads(.text)
#df_naver = json_normalize(json_data['result']['etfItemList'])

