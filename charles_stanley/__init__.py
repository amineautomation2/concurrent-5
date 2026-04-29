from utils import get_xlsx_filepath, setup_driver, delay
from .url import get_page_urls
from .total import get_total_funds
from .keyword import get_keyword
from worker import get_data_by_worker_id, get_xlsx_data, write_csv_by_id


def url_runner(id_worker, max_workers):
    driver = setup_driver(True)
    print("[#]       Charles Stanley        [#]")
    base = "https://www.charles-stanley-direct.co.uk/InvestmentSearch/Search?SearchType=KeywordSearch&Category=Funds&SortColumn=Name&SortDirection=Asc&Pagesize=50"
    url = f"{base}&Page=1"
    total_pages = get_total_funds(url)
    pages = [p for p in range(1, total_pages+1)]
    pages_per_worker = pages[id_worker::max_workers]
    worker_data = []
    csv_out = f"charles_stanley_{id_worker}_url.csv"
    for page in pages_per_worker:
        data = get_page_urls(driver, f"{base}&Page={page}")
        worker_data.extend(data)
        delay(2, 3)
    write_csv_by_id(csv_out, worker_data, ["name", "isin", "url"])

    driver.quit()


def keyword_runner(id_worker, max_worker):
    xlsx = get_xlsx_filepath("charles_stanley.xlsx")
    data = get_xlsx_data(xlsx, "Funds")
    print("length data =", len(data))
    data_per_worker = get_data_by_worker_id(
        id=id_worker,
        max_worker=max_worker,
        data=data,
    )
    print("length worker data =", len(data_per_worker))
    driver = setup_driver(True)
    print("[#] Keywords [#]")
    keyword_per_worker = get_keyword(driver, data_per_worker)
    csv_out = f"charles_stanley_{id_worker}_keyword.csv"

    fields = ["name", "isin", "url", "keyword"]
    write_csv_by_id(csv_out,
                    keyword_per_worker,
                    fields,
                    )

    driver.quit()
