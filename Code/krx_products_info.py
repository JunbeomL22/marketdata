from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_krx_derivative_info(url, max_table=2):
    driver = webdriver.Chrome()  # Make sure you have the appropriate WebDriver installed
    driver.get(url)

    try:
        # Wait for the tables to be present in the DOM
        tables = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.design-table1 table"))
        )

        derivative_info = {}
        for ith, table in enumerate(tables):
            if ith > max_table:
                break
            # Find all the table rows
            rows = table.find_elements(By.TAG_NAME, "tr")

            row_results = {}
            for j, row in enumerate(rows):
                # Find all the cells in each row
                cells = row.find_elements(By.TAG_NAME, "th") + row.find_elements(By.TAG_NAME, "td")

                row_result = []
                for k, cell in enumerate(cells):
                    row_result.append(cell.get_attribute("innerText").strip())

                row_results[j] = row_result
        
            derivative_info[ith] = row_results

        return derivative_info
    finally:
        driver.quit()

# URL of the page
urls = {
    "KOSPI200": "https://open.krx.co.kr/contents/OPN/01/01040201/OPN01040201.jsp",
    "KTBF": "https://open.krx.co.kr/contents/OPN/01/01040501/OPN01040501.jsp"
}

res = get_krx_derivative_info(urls['KTBF'])
for key, value in res.items():
    print(f"{key}: {value}")