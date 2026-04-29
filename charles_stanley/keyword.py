
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.webdriver import WebDriver
from utils import delay, find_element_or_none, get_with_backoff


def get_keyword(driver: WebDriver, data: list[dict]) -> list[dict]:
    keyword_xpath_p = '//p[contains(., "Invest in this")]'
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
        delay(3, 7)
    return data
