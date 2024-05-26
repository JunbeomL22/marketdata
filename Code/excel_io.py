import xlwings as xw
import pandas as pd
import os
from code_config import jsondb_dir

def save_bond_maseter_excel(
        wb = None,
        parameter_date = "20240524",
        sheet_name = "BondMaster",
        vrt_bnd_range = "VrtBndMaster",
        bond_master_range = "BondMaster",
        output_file = "bond_master.json"):
    if wb is None:
        wb = xw.Book.caller()
    sht = wb.sheets[sheet_name]
    vrt_bnd = sht.range(vrt_bnd_range).value
    vrt_bnd = [v for v in vrt_bnd if v[0] is not None]
    vrt_df = pd.DataFrame(vrt_bnd[1:], columns = vrt_bnd[0])

    bnd = sht.range(bond_master_range).value
    bnd = [v for v in bnd if v[0] is not None]
    bnd_df = pd.DataFrame(bnd[1:], columns = bnd[0])

    bnd_df = pd.concat([vrt_df, bnd_df])
    # print if there is any duplicated isin
    dup = bnd_df[bnd_df.duplicated(subset = 'isin', keep = False)]
    if len(dup) > 0:
        print(dup)
    bnd_df.drop_duplicates(subset = 'isin', keep = 'first', inplace = True)

    directory = os.path.join(jsondb_dir, parameter_date)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    bnd_df.to_json(os.path.join(directory, output_file), orient = "records")

if __name__ == "__main__":
    xw.Book("D:/Projects/marketdata/MarketData.xlsm").set_mock_caller()
    save_bond_maseter_excel()
    bnd = pd.read_json(os.path.join(jsondb_dir, "20240524", "bond_master.json"), orient = "records")