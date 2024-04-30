import requests
import pandas as pd
from bs4 import BeautifulSoup

def get_klca_dividend(
        year = 2024,
        month = 4,
        day = 1,):
    month = str(month).zfill(2)

    url = f"https://www.klca.or.kr/sub/info/record_date.asp?rWork=TblList&d=m&F_Year={year}&F_Month={month}&rDay={day}"

    response = requests.post(
        url = url,
        verify = False
        )

    response.encoding = 'euc-kr'
    contents = response.text

    # Parse the HTML content
    soup = BeautifulSoup(contents, 'html.parser')

    # Find the table containing the dividend data
    table = soup.find('table', class_='board_compact')

    # Extract the table headers
    headers = []
    for th in table.find_all('th'):
        header = th.get_text(strip=True)
        headers.append(header)

    # Extract the table data
    data = []
    for row in table.find_all('tr')[1:]:  # Skip the header row
        row_data = []
        for td in row.find_all('td'):
            cell_data = td.get_text(strip=True)
            row_data.append(cell_data)
        data.append(row_data)

    # Create a DataFrame from the extracted data
    res = pd.DataFrame(data, columns=headers)

    return res