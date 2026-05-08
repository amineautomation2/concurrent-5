from charles_stanley.etf import url_etf
from utils import save_xlsx
from worker import get_xlsx_data


out = "spreadsheet/b.xlsx"
data_xlsx = get_xlsx_data("spreadsheet/b.xlsx", "ETF")
data_url = url_etf(0, 1)
for url in data_url:
    for x in data_xlsx:
        if url["name"] == x["name"]:
            url.update(dict(isin=x["isin"], keyword=x["keyword"]))
save_xlsx(out, data_url, ["name", "isin",
          "symbol", "url", "keyword"], "ETF", 2)
print(data_url[0])
