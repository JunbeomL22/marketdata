import sys, json, requests
from config import infomax_api_token

session.verify = False
api_url = 'https://infomaxy.einfomax.co.kr/api/stock/info'

params = {"code":"472830,153130",
          "date": "20231215"}

headers = {"Authorization" : f'bearer {infomax_api_token}'}

r = session.get(api_url, params = params, headers = headers)
success, results = r.json().values()
