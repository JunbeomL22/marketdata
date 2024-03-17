import sys, json, requests
from config import infomax_api_token
import pandas as pd
import code_config
# -
session = requests.Session()
# SSL 인증 처리 무효화
session.verify = False
tick_api_url = 'https://infomaxy.einfomax.co.kr/api/stock/tick_etc'
params = {"code":"252670","date":"20231201","session": ''}


r = session.get(tick_api_url, params = params, headers = code_config.infomax_headers)
success, results = r.json().values()

df = pd.DataFrame(results)
print(df)
# 정렬. ensure_ascii = 한글 깨짐 방지. indent = 들여쓰기.
#print(json.dumps(r.json(), ensure_ascii=False, indent=2))
