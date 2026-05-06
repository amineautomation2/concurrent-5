import argparse
import os
import time
from charles_stanley import keyword_runner, url_runner
from charles_stanley.etf import etf_keyword_runner, get_page_data
from charles_stanley.keyword import get_keyword
from charles_stanley.url import get_page_urls
from charles_stanley.total import get_total_funds
from utils import create_spreadsheet, delay, get_xlsx_filepath, setup_driver
from worker import (
    get_xlsx_data_empty,
    merge_csv_to_xlsx,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=str, help="id worker")
    parser.add_argument("--max", type=str, help="max workers")
    parser.add_argument("--sheet", type=str, help="sheet name")
    parser.add_argument("--merge", action="store_true",
                        help="merge csv files into spreadsheet")
    parser.add_argument("--url", action="store_true", help="get funds url")
    parser.add_argument("--keyword", action="store_true",
                        help="get funds keyword")
    args = parser.parse_args()
    filename = "charles_stanley.xlsx"
    xlsx = get_xlsx_filepath(filename)
    # xlsx = os.path.join("spreadsheet", filename)
    # create_spreadsheet(xlsx, ["ETF", "Funds"], [
    #    "Name", "ISIN", "URL", "Keyword"])

    if args.url and args.id and args.max and args.sheet:
        url_runner(int(args.id), int(args.max), args.sheet)
        return

    if args.keyword and args.id and args.max and args.sheet:
        keyword_runner(int(args.id), int(args.max), args.sheet)
        return

    elif args.merge and args.keyword and args.sheet:
        merge_csv_to_xlsx(
            xlsx, ["name", "isin", "url", "keyword"], args.sheet, f"{args.sheet}_keyword.csv")
        return

    elif args.merge and args.url and args.sheet:
        merge_csv_to_xlsx(
            xlsx, ["name", "isin", "url"], args.sheet, f"{args.sheet}_url.csv")
        return


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    # driver = setup_driver(True)
    # data = get_page_data(driver, [dict(
    #    name="abc", url="https://www.charles-stanley-direct.co.uk/ViewFund?InvestmentId=G9%2BpUE7%2BaEg%3D&Isin=GB00B2PB2C75&PreviousSearchResults=%2FInvestmentSearch%2FSearch%3Fsortdirection%3DASC%26SearchType%3DKeywordSearch%26Category%3DFunds%26SortColumn%3DName%26Pagesize%3D20%26page%3D1")])
    # print(data)
    # driver.quit()
    elapsed = time.perf_counter() - start
    print(f"Execution time: {elapsed:.2f} seconds.")
