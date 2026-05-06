from charles_stanley.mutual import url_mf, mf_keyword_runner
from charles_stanley.etf import url_etf, etf_keyword_runner


def url_runner(id_worker: int, max_workers: int, sheet: str):
    if sheet == "ETF":
        url_etf(id_worker, max_workers)
        return
    elif sheet == "MF":
        url_mf(id_worker, max_workers)
        return


def keyword_runner(id_worker: int, max_worker: int, sheet: str):
    if sheet == "ETF":
        etf_keyword_runner(id_worker, max_worker)
        return
    elif sheet == "MF":
        mf_keyword_runner(id_worker, max_worker)
        return
