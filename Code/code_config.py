import urllib3;urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

colors = ['yellowgreen', 'gold', 'lightblue', 'lightcoral', 'green',
          'gold', 'pink','magenta', 'violet', 'lightgreen', 'blue',
          'cyan', 'lightskyblue', 'pink']

data_path = 'C:\\Users\\junbe\\Dropbox\\02. Projects\\01. WebCralwer\\Data\\'

infomax_api_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiJFMjEwMzc0IiwiY291cG9uVHlwZSI6ImFwaSIsInN2YyI6ImluZm9tYXgiLCJpYXQiOjE3MDE5MjM1NTUsImV4cCI6MjY0ODAwMzU1NX0.4Hfd4LRerv3KaQ8Dygd7Lflv_FL2JrhvBcPRnwHBilg'

trade_history_data_path = 'C:\\Users\\junbe\\Dropbox\\02. Projects\\01. WebCralwer\\Data\\TradeHistory\\'

infomax_headers = {"Authorization" : f'bearer {infomax_api_token}'}
