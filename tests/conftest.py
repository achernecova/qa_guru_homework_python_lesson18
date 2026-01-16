import pytest
from selene import browser as selene_browser
from selenium import webdriver
from selenium.webdriver import ChromeOptions

from api_helper.api_login import ApiHelper
from config import LOGIN, PASSWORD
from pages.cart_page import CartPage
from utils.logger import setup_logger


@pytest.fixture(scope="function")
def browser_setup():
    options = ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    selene_browser.config.driver = driver
    return driver


@pytest.fixture(scope="function")
def prepared_cart(browser_setup):
    driver = browser_setup
    cart = CartPage()
    yield cart
    cart.delete_all_product_in_cart()
    driver.quit()


@pytest.fixture(scope="session")
def api_login():
    return ApiHelper()


@pytest.fixture(scope="session")
def cookies(api_login):
    return api_login.login(LOGIN, PASSWORD)


def pytest_configure():
    setup_logger()
