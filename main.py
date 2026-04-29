import argparse
import time
from charles_stanley import keyword_runner, url_runner
from charles_stanley.url import get_page_urls
from charles_stanley.total import get_total_funds
from utils import delay, get_xlsx_filepath, setup_driver
from worker import (
    merge_csv_to_xlsx,
)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", type=str, help="id worker")
    parser.add_argument("--max", type=str, help="max workers")
    parser.add_argument("--merge", action="store_true",
                        help="merge csv files into spreadsheet")
    parser.add_argument("--url", action="store_true", help="get funds url")
    parser.add_argument("--total", action="store_true", help="get total funds")
    parser.add_argument("--keyword", action="store_true",
                        help="get funds keyword")

    args = parser.parse_args()
    xlsx_out = get_xlsx_filepath("charles_stanley.xlsx")
    if args.total:
        return

    if args.url and args.id and args.max:
        url_runner(int(args.id), int(args.max))
        return
    if args.keyword and args.id and args.max:
        keyword_runner(int(args.id), int(args.max))
        return

    elif args.merge and args.keyword:
        merge_csv_to_xlsx(
            xlsx_out, ["name", "isin", "url", "keyword"], "Funds", "keyword.csv")
        return

    elif args.merge and args.url:
        merge_csv_to_xlsx(
            xlsx_out, ["name", "isin", "url"], "Funds", "url.csv")
        return


if __name__ == "__main__":
    start = time.perf_counter()
    main()
    elapsed = time.perf_counter() - start
    print(f"Execution time: {elapsed:.2f} seconds.")
