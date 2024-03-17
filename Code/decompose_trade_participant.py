from pykrx import stock, bond

code_name = dict([['190620', 'ACE 단기통안채'],
                  ['459580', 'KODEX CD금리액티브(합성)'],
                  ['196230', 'KBSTAR 단기통안'],
                  ['157450', 'TIGER 단기통안채'],
                  ['153130', 'KODEX 단기채권'],
                  ['122630', 'KODEX 레버리지'],
                  ['251340', 'KODEX 코스닥150선물인버스'],
                  ['233740', 'KODEX 코스닥150레버리지']])

df = stock.get_etf_trading_volume_and_value("20230601", "20231130", '122630')/100000000
