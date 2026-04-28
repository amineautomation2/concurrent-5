from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


from utils import find_element_or_none, find_elements
from re import compile, findall


def get_isin(s: str) -> str:
    isin_re = compile(r'[A-Z]{2}[A-Z0-9]{9}[0-9]{1}')
    found = isin_re.findall(s)
    if len(found) > 0:
        return found[0]
    return ""


def get_page_urls(driver: WebDriver, url: str) -> list[dict]:
    driver.get(url)
    table_name_xpath = '//*[@id="funds-table-first"]/tbody/tr'
    table_url_xpath = '//*[@id="funds-table-last"]/tbody/tr'
    wait = WebDriverWait(driver=driver, timeout=5)
    i = 0
    table_name = find_elements(wait, table_name_xpath)
    table_url = find_elements(wait, table_url_xpath)
    fund_data_per_page = []
    u = 'https://www.charles-stanley-direct.co.uk/ViewFund?InvestmentId=G9%2BpUE7%2BaEg%3D&Isin=GB00B2PB2C75&PreviousSearchResults=%2FInvestmentSearch%2FSearch%3FSearchType%3DKeywordSearch%26Category%3DFunds%26SortColumn%3DName%26SortDirection%3DAsc%26Pagesize%3D50%26Page%3D1'
    if table_name and table_url:
        for tr in table_name:
            name = tr.find_element(By.XPATH, "./td").text
            url_elm = table_url[i].find_element(
                By.XPATH, "./td/div[1]/a").get_attribute("href")
            fund_url = url_elm
            if fund_url:
                isin = get_isin(fund_url)
                fund = dict(name=name.strip(), url=fund_url, isin=isin)
                fund_data_per_page.append(fund)
            i += 1

    return fund_data_per_page
