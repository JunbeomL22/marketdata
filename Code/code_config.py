from api_keys import infomax_key
import urllib3;urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

colors = ['yellowgreen', 'gold', 'lightblue', 'lightcoral', 'green',
          'gold', 'pink','magenta', 'violet', 'lightgreen', 'blue',
          'cyan', 'lightskyblue', 'pink']

jsondb_dir = 'C:/JsonDB/'
root_dir = 'D:/Projects/marketdata/'

INFOMAX_HEADER = {"Authorization" : f'bearer {infomax_key}'}


KRX_HEADER = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "http://data.krx.co.kr/"
    }

KRX_ISIN_HEADER = {
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://isin.krx.co.kr/srch/srch.do?method=srchList"
    }