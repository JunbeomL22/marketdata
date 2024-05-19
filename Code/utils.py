import QuantLib as ql

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

custom_sk = ql.SouthKorea()