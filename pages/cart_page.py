import logging

import allure
from selene import browser as selene_browser
from selene import by
from selene.api import browser, have

from config import cart_page_url

logger = logging.getLogger(__name__)


class CartPage:
    def __init__(self):
        self.browser = selene_browser
        self.order_summary = ".order-summary-content"
        self.title_in_cart = "h1"
        self.button_update_cart = "input[name='updatecart']"
        self.count_product_all = ".cart-item-row"

    def open(self):
        with allure.step("Открываем страницу с корзиной"):
            logger.info("Открываем страницу корзины")
            self.browser.open(cart_page_url)

    def set_cookies_and_refresh_browser(self, cookies, nop_customer_cookie=None):
        with allure.step("Ставим куки и обновляем браузер"):
            logger.info("Ставим куки и обновляем браузер")
            self.browser.open(cart_page_url)
            self.browser.config.driver.add_cookie(
                {"name": "NOPCOMMERCE.AUTH", "value": cookies["NOPCOMMERCE.AUTH"]}
            )
            if nop_customer_cookie:
                self.browser.config.driver.add_cookie(
                    {"name": "Nop.customer", "value": nop_customer_cookie}
                )
            self.browser.driver.refresh()

    def assert_data_prodict_in_card(self, index, name_product, price_product):
        with allure.step("Проверяем данные в продуктах"):
            logger.info("Проверяем данные в продуктах")
            self.browser.element(
                by.xpath(
                    f"(//*[@class='cart-item-row'])[{index + 1}]//*[@class='product-name']"
                )
            ).should(have.text(name_product))
            self.browser.element(
                by.xpath(
                    f"(//*[@class='cart-item-row'])[{index + 1}]//*[@class='product-unit-price']"
                )
            ).should(have.text(price_product))

    def get_len_count_prodict_in_cart(self):
        with allure.step("Получаем количество товаров в корзине"):
            count_product = len(self.browser.all(self.count_product_all))
            return count_product

    def assert_qty_product_in_cart(self):
        with allure.step("Получаем количество штук одного товара в корзине"):
            qty_product = self.browser.element(".qty-input").should(have.value("2"))
            return qty_product

    def delete_all_product_in_cart(self):
        with allure.step("Выбираем все товары в корзине"):
            count_product = self.get_len_count_prodict_in_cart()
            for i in range(count_product):
                checkboxes_product = browser.element(
                    by.css("input[name='removefromcart']")
                )
                checkboxes_product.click()
                logger.info(f"Выбрали товар {i + 1}")
                self.browser.element(self.button_update_cart).click()
                logger.info(f"Удалили товар {i + 1}")
        with allure.step("Проверяем, что корзина пуста"):
            self.browser.element(self.title_in_cart).should(have.text("Shopping cart"))
            self.browser.element(self.order_summary).should(
                have.text("Your Shopping Cart is empty!")
            )
