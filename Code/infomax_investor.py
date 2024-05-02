import requests
from code_config import INFOMAX_HEADER
import pandas as pd
import xlwings as xw



res = get_investor(investor="1000", code="", start_date="20240101", end_date="20240430")