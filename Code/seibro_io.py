from seibro_data import get_seibro_dividend
from code_config import jsondb_dir
import pandas as pd
import os
import xlwings as xw


def save_seibro_dividend(
        parameter_date = '20240517',
        retrieval_date = '20240518',
        start_date = '20240517',
        end_date = '20241017',
        etf_dividend_type = 'profit sharing',
        sleep_time = 3,
        file_name = "seibro_dividend.json",
        ):
    print("saving seibro dividend data...")
    directory = os.path.join(jsondb_dir, parameter_date)
    if not os.path.exists(directory):
        os.makedirs(directory)

    if etf_dividend_type == 'profit sharing':
        etf_dividend_type = '이익분배'

    df = get_seibro_dividend(
        start_date = start_date,
        end_date = end_date,
        etf_dividend_type = etf_dividend_type,
        sleep_time = int(sleep_time)
    )
    df.insert(0, 'retrieval_date', retrieval_date)
    df.to_json(f'{directory}/{file_name}', orient='records')

def load_seibro_dividend(
        wb = None,
        sheet_name = 'Dividend',
        parameter_date = '20240517',
        file_name = "seibro_dividend.json",
        output_head = 'F4',):
    directory = os.path.join(jsondb_dir, parameter_date)
    df = pd.read_json(f'{directory}/{file_name}', orient='records')
    if wb is None:
        wb = xw.Book.caller()

    ws = wb.sheets[sheet_name]
    ws.range(output_head).options(index=False).value = df


