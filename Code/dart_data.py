import requests
import zipfile
import io
import pandas as pd

api_key = "a4483b96ee3751c6f0214223e3de4df3a73449bd"

url = "https://opendart.fss.or.kr/api/corpCode.xml"

response = requests.get(
    url = url, 
    verify = False,
    params = {"crtfc_key": api_key},
    )

# Create a BytesIO object from the content
zip_file = zipfile.ZipFile(io.BytesIO(response.content))

# Open the first file in the zip file
xml_file = zip_file.open(zip_file.namelist()[0])

# Read the content of the xml file
xml_content = xml_file.read()

company_codes = pd.read_xml(xml_content)
company_codes['corp_code'] = company_codes['corp_code'].astype(str).str.zfill(8)

div_url = "https://opendart.fss.or.kr/api/alotMatter.json"

div_resp = requests.get(
    url = div_url, 
    verify = False,
    params = {
        "crtfc_key": api_key,
        "corp_code": "00126380",
        "bsns_year": "2023",
        "reprt_code": "11011",
        },
    )

res = pd.DataFrame(div_resp.json()['list'])
print(res)

