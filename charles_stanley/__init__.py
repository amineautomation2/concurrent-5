from time import sleep
from random import uniform
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from utils import find_element_or_none, find_elements, get_xlsx_filepath, setup_driver, write_json
from .url import get_page_urls
from .total import get_total_funds
from worker import get_data_by_worker_id, write_csv_by_id
import openpyxl


def charles_stanley_runner(id_worker, max_workers):
    driver = setup_driver(True)
    print("[#]       Charles Stanley        [#]")
    wait = WebDriverWait(driver, timeout=5)
    xlsx = get_xlsx_filepath("charles_stanley.xlsx")
    base = "https://www.charles-stanley-direct.co.uk/InvestmentSearch/Search?SearchType=KeywordSearch&Category=Funds&SortColumn=Name&SortDirection=Asc&Pagesize=50"
    url = f"{base}&Page=1"
    total_pages = get_total_funds(url)
    pages = [p for p in range(1, total_pages+1)]
    pages_per_worker = pages[id_worker::max_workers]
    worker_data = []
    csv_out = f"charles_stanley_{id_worker}_url.csv"
    i = 0
    for page in pages_per_worker:
        print("Page = ", page)
        if i == 3:
            break
        data = get_page_urls(driver, f"{base}&Page={page}")
        worker_data.extend(data)
        i += 1
    write_csv_by_id(csv_out, worker_data, ["name", "isin", "url"])

    driver.quit()
