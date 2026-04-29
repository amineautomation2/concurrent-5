
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from utils import delay, find_element_or_none, get_with_backoff


def get_keyword(driver: WebDriver, data: list[dict]) -> list[dict]:
    keyword_xpath_p = '//p[contains(., "Invest in this")]'
    wait = WebDriverWait(driver, timeout=5)
    keyword = None
    for fund in data:
        url = fund["url"]
        try:
            get_with_backoff(driver, url)
        except:
            print("error: ", url)
            fund.update(dict(keyword=keyword))
            continue
        keyword = find_element_or_none(wait, keyword_xpath_p)
        if keyword:
            fund.update(dict(keyword=keyword.text.strip()))
        delay(3, 5)
    return data
