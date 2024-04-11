from pykrx import stock

tickers = stock.get_index_ticker_list("20240405", market = 'KOSPI')
tickers += stock.get_index_ticker_list("20240405", market = 'KOSDAQ')

ticker_dict = {}
for ticker in tickers:
    ticker_dict[ticker] = stock.get_index_ticker_name(ticker)

pdf = stock.get_index_portfolio_deposit_file("1001")
print(len(pdf), pdf)

df = stock.get_etf_trading_volume_and_value("20220908", "20220916", "580011")
print(df.head())

df = stock.get_etf_ohlcv_by_date("20170101", "20240405", "069500")
print(df.head())