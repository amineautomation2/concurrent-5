from charles_stanley.keyword import get_keyword
from utils import get_with_backoff, setup_driver, find_element_or_none, isin_from_pdf
from worker import get_data_by_worker_id, get_xlsx_data, write_csv_by_id
from pathlib import Path
from os.path import join, dirname, basename
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
import csv


def get_csv_data(filepath: str) -> list:
    project_root = Path(__file__).resolve().parent.parent
    path = join(project_root, filepath)
    data = []
    try:
        with open(path, mode='r', encoding='utf-8-sig') as csvfile:
            # DictReader uses the first row as the keys for the dictionaries
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(dict(row))
        return data
    except FileNotFoundError:
        raise Exception("Error: The file was not found.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")


def investment_runner(id, max_worker):
    data = get_csv_data("spreadsheet/investment_trust.csv")
    print("### Charles Investment ##")
    worker_data = get_data_by_worker_id(id, max_worker, data)
    driver = setup_driver(True)
    for fund in worker_data:
        f = lookup_search(driver, fund)
        fund.update(f)
    out = f"charles_stanley_{id}_Investment.csv"
    fields = ["name", "isin", "ticker", "url", "keyword"]
    write_csv_by_id(out, worker_data, fields)
    driver.quit()


def lookup_search(driver: WebDriver, fund: dict) -> dict:
    has_isin = fund.get("isin")
    search_term = fund.get("isin") or fund.get(
        "ticker") or fund.get("name")
    url = f"https://www.charles-stanley-direct.co.uk/InvestmentSearch/Search?SearchText={search_term}&submit=Search"
    get_with_backoff(driver, url, max_retries=3)
    current_url = driver.current_url
    if current_url != url:
        """
            Found fund for current search term
            Get keywords and ISIN
        """
        fund.update(dict(url=current_url))
        keyword_xpath_p = '//p[contains(., "Invest in this")]'
        wait = WebDriverWait(driver, timeout=5)
        keyword = find_element_or_none(wait, keyword_xpath_p)
        if keyword:
            fund.update(dict(keyword=keyword.text.strip()))
        if not has_isin:
            factsheet_xpath = '//a[contains(.,"FACTSHEET")]'
            pass
            factsheet = find_element_or_none(
                WebDriverWait(driver, timeout=3), factsheet_xpath)
            if factsheet:
                fact = factsheet.get_attribute("href")
                isin = None
                if fact:
                    isin = isin_from_pdf(fact)
                fund.update(dict(isin=isin))
        return fund
    fund.update(dict(url=None, keyword=None))
    return fund
