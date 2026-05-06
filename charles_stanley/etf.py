from utils import get_xlsx_filepath, setup_driver, delay, find_element_or_none, get_with_backoff, isin_from_pdf
from .url import get_page_urls
from .total import get_total_funds
from worker import get_data_by_worker_id, get_xlsx_data, write_csv_by_id
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver


def get_page_data(driver: WebDriver, data: list[dict]) -> list[dict]:
    keyword_xpath_p = '//p[contains(., "Invest in this")]'
    factsheet_xpath = '//a[contains(.,"FACTSHEET")]'
    wait = WebDriverWait(driver, timeout=10)
    for fund in data:
        url = fund["url"]
        try:
            get_with_backoff(driver, url)
        except Exception as e:
            print(f"error: {e}, {url}")
            fund.update(dict(keyword=None))

        keyword = find_element_or_none(wait, keyword_xpath_p)
        if keyword:
            fund.update(dict(keyword=keyword.text.strip()))

        factsheet = find_element_or_none(
            WebDriverWait(driver, timeout=3), factsheet_xpath)
        if factsheet:
            fact = factsheet.get_attribute("href")
            print("fact = ", fact)
            isin = None
            if fact:
                isin = isin_from_pdf(fact)
            fund.update(dict(isin=isin))

        delay(3, 7)
    return data


def url_etf(id_worker, max_workers):
    driver = setup_driver(True)
    print("[#] ETF URL [#]")
    base = "https://www.charles-stanley-direct.co.uk/InvestmentSearch/Search?sortdirection=DESC&searchtext=ETF&category=Equities&submit=Search&pagesize=50"
    url = f"{base}&Page=1"
    total_pages = get_total_funds(url)
    pages = [p for p in range(1, total_pages+1)]
    pages_per_worker = pages[id_worker::max_workers]
    worker_data = []
    csv_out = f"charles_stanley_{id_worker}_ETF_url.csv"
    for page in pages_per_worker:
        data = get_page_urls(driver, f"{base}&Page={page}", "ETF")
        worker_data.extend(data)
        delay(2, 3)
        break
    write_csv_by_id(csv_out, worker_data, ["name", "isin", "url"])
    driver.quit()


def etf_keyword_runner(id_worker, max_worker):
    xlsx = get_xlsx_filepath("charles_stanley.xlsx")
    data = get_xlsx_data(xlsx, "ETF")
    data_per_worker = get_data_by_worker_id(
        id=id_worker,
        max_worker=max_worker,
        data=data,
    )
    driver = setup_driver(True)
    driver.capabilities["pageLoadStrategy"] = "eager"
    print("[#] ETF ISIN & Keywords [#]")

    page_data_per_worker = get_page_data(driver, data_per_worker[:1])

    csv_out = f"charles_stanley_{id_worker}_ETF_keyword.csv"

    fields = ["name", "isin", "url", "keyword"]
    write_csv_by_id(csv_out,
                    page_data_per_worker,
                    fields,
                    )

    driver.quit()
