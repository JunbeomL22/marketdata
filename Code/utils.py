import QuantLib as ql
import xlwings as xw
import pandas as pd

def time_format(t, rounding = 1):
    h = int(t // 3600.0)
    t = t - 3600*h
    m = int(t // 60.0)
    s = t - m * 60.0
    res = f"{h}h " if h > 0 else ""
    add_res = f"{m}m " if m > 0 else ""
    res += add_res

    res += f"{round(s, rounding)}s"

    return res


def pandas_to_quantlib_date(inp):
    return ql.Date(inp.day, inp.month, inp.year)    

def get_krx_holidays(
        wb = None,
        sheet_name = 'BaseData',
        range_name = 'KrxHolidays',):
    if wb is None:
        wb = xw.Book.caller()
    ws = wb.sheets[sheet_name]
    rng = ws.range(range_name).value
    df = pd.DataFrame(rng, columns = ['ADD_HOL'])
    df.dropna(inplace = True)
    df['ADD_HOL'] = df['ADD_HOL'].apply(pandas_to_quantlib_date)

    cal = ql.SouthKorea()
    for date in df['ADD_HOL'].tolist():
        cal.addHoliday(date)

    return cal
