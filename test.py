from utils import fetch_with_backoff, get_isin, isin_from_pdf

url = "https://documents.financialexpress.net/Literature/BDE7664927BD32BDD434F6A219844CD9/240180503.pdf"
url2 = "https://documents.financialexpress.net/Literature/DEB6CCD4CB981A5692B7372D61A57836/241242076.pdf"
res = isin_from_pdf(url)
print(res)
res = isin_from_pdf(url2)
print(res)
