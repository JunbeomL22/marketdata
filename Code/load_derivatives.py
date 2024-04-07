from code_config import data_path, INFOMAX_HEADER
import sys, json, requests
import pandas as pd
session = requests.Session()

session.verify = False
api_url = 'https://infomaxy.einfomax.co.kr/api/future/expired'

params = {"kr_name": "",
          "type": "",
          "underline": "",
          "endDate": "",
          "startDate": "20240304"
          }

r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

success, results = r.json().values()
res = pd.DataFrame(results)
print(res)