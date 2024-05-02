import requests
import zipfile
import io
import pandas as pd
from api_keys import dart_key

def save_corp_codes():
    url = "https://opendart.fss.or.kr/api/corpCode.xml"

    response = requests.get(
        url = url, 
        verify = False,
        params = {"crtfc_key": dart_key},
        )

    # Create a BytesIO object from the content
    zip_file = zipfile.ZipFile(io.BytesIO(response.content))

    # Open the first file in the zip file
    xml_file = zip_file.open(zip_file.namelist()[0])

    # Read the content of the xml file
    xml_content = xml_file.read()

    company_codes = pd.read_xml(xml_content)
    company_codes['corp_code'] = company_codes['corp_code'].astype(str).str.zfill(8)
    
    company_codes.to_json('Data/corp_codes.json', orient='records')

def get_tangible_asset(
        name_part1: str ="",
        name_part2: str =None,
        side = "acquisition other corporation", # "acquisition" or "disposal"
        bgn_de: str = "20210101",
        end_de: str = "20211231",
        corp_code_file: str = "Data/corp_codes.json",
        ):
    """
    side: str
    1) "acquisition tangible asset": 유형자산 취득내역
    2) "transfer tangible asset": 유형자산 처분내역
    3) "acquisition other corporation": 타법인 투자자산 취득내역
    4) "transfer other corporation": 타법인 투자자산 처분내역
    5) "acquisition own shares": 자기주식 취득내역
    6) "transfer own shares": 자기주식 처분내역
    """
    if side == "acquisition tangible asset":
        url = 'https://opendart.fss.or.kr/api/tgastInhDecsn.json'
    elif side == "transfer tangible asset":
        url = 'https://opendart.fss.or.kr/api/tgastTrfDecsn.json'
    elif side == "acquisition other corporation":
        url = 'https://opendart.fss.or.kr/api/otcprStkInvscrInhDecsn.json'
    elif side == "transfer other corporation":
        url = 'https://opendart.fss.or.kr/api/otcprStkInvscrTrfDecsn.json'
    elif side == "acquisition own shares":
        url = '	https://opendart.fss.or.kr/api/tsstkAqDecsn.json'
    elif side == "transfer own shares":
        url = 'https://opendart.fss.or.kr/api/tsstkDpDecsn.json'
    else:
        raise ValueError("Invalid side. side must be one of the following: acquisition tangible asset, transfer tangible asset, acquisition other corporation, transfer other corporation, acquisition own shares, transfer own shares.")
        

    company_codes = pd.read_json(corp_code_file)
    company_codes['corp_code'] = company_codes['corp_code'].astype(str).str.zfill(8)
    company_codes = company_codes[company_codes['corp_name'].str.contains(name_part1, case=False)]

    if name_part2:
        company_codes = company_codes[company_codes['corp_name'].str.contains(name_part2, case=False)]

    codes = company_codes['corp_code'].unique().tolist()
    if len(codes) == 0:
        print(f"No company found with name {name_part1} {name_part2}")
        return None
    
    if len(codes) > 1:
        print(f"Multiple companies found with name {name_part1} {name_part2}")
        print(company_codes)
        return None
    
    code = codes[0]

    response = requests.get(
        url=url,
        verify=False,
        params={
            "crtfc_key": dart_key,
            "corp_code": str(code),
            "bgn_de": bgn_de,
            "end_de": end_de,
        },
    )  

    r = response.json()
    if r['status'] != "000":
        print(f"Error: {r['message']}")
        return None
    else:
        res = pd.DataFrame(r['list'])
    return res
    