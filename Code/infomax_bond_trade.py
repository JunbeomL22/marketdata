from code_config import INFOMAX_HEADER
import requests
import pandas as pd
session = requests.Session()
# SSL 인증 처리 무효화
session.verify = False
api_url = 'https://infomaxy.einfomax.co.kr/api/bond/market/mn_hist'

params = {"stdcd":"",
          "market":"5",
          "startDate":"20240416",
          "endDate":"20240416",
          "aclassnm":"국채",
          "volume":""}

r = session.get(api_url, params = params, headers = INFOMAX_HEADER)

success, results = r.json().values()
res = pd.DataFrame(results)
print(res)