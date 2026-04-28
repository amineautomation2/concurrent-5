from selenium.webdriver.chrome.webdriver import WebDriver
from json import dump
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from utils import find_element_or_none, find_elements, setup_driver
from re import compile, findall


def get_total_funds(url: str) -> int:
    driver = setup_driver(True)
    driver.get(url)
    wait = WebDriverWait(driver=driver, timeout=5)
    pages_xpath = "//div[@id='search-results-top']/p[1]/em[last()]"
    total_pages = find_element_or_none(wait, pages_xpath)
    if total_pages:
        pages = int(total_pages.text)
        return pages
    print("total_pages not found")
    return 0
