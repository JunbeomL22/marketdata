from krx_io import save_krx_etf_pdf
import xlwings as xw

def save_main(
        wb = None,):
    ws = wb.sheets['EtfPdf']
    conf = dict(ws.range('PdfConf').value)
    parameter_date = conf['parameter date']
    base_file = conf['krx base info']
    pdf_file = conf['krx pdf file']
    min_cap = conf['min cap (억)']
    market_type = conf['market type']
    sleep_time = conf['sleep time']
    save_krx_etf_pdf(
        wb = wb,
        sheet_name = 'EtfPdf',
        parameter_date = parameter_date,
        etf_pdf_add_list_range= 'EtfPdfAddList',
        combined_base_file = base_file,
        pdf_file = pdf_file,
        min_cap = min_cap,
        market_type = market_type,
        sleep_time = sleep_time,
    )

if __name__ == '__main__':
    wb = xw.Book('D:/Projects/marketdata/MarketData.xlsm')
    save_main(wb = wb)