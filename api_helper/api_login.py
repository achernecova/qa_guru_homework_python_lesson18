import logging

import allure
import requests
from allure_commons.types import AttachmentType

from config import api_login_url, base_url

logger = logging.getLogger(__name__)


class ApiHelper:
    def __init__(self):
        self.session = requests.Session()

    @staticmethod
    def get_attach_data_response(response):
        allure.attach(
            body=response.text,
            name="Response",
            attachment_type=AttachmentType.TEXT,
            extension="txt",
        )
        allure.attach(
            body=str(response.cookies),
            name="Cookies",
            attachment_type=AttachmentType.JSON,
            extension="json",
        )

    def login(self, email, password):
        with allure.step("Авторизуемся через API"):
            response = self.session.post(
                url=api_login_url,
                data={"Email": email, "Password": password, "RememberMe": False},
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                allow_redirects=False,
            )
            logger.info("Отправили запрос на авторизацию")
            self.get_attach_data_response(response)
            assert (
                    "NOPCOMMERCE.AUTH" in response.cookies
            ), "Сервер не вернул куки NOPCOMMERCE.AUTH"
            return response.cookies.get_dict()

    def add_product_book(self, cookies):
        with allure.step("Добавляем 2 книги в корзину"):
            response = self.session.post(
                url=base_url + "addproducttocart/details/13/1",
                data={"addtocart_13.EnteredQuantity": "2"},
                headers={"Accept": "application/json"},
                cookies=cookies,
                allow_redirects=False,
            )
            logger.info("Отправили запрос на добавление книги в корзину")
            self.get_attach_data_response(response)
            assert response.json().get(
                "success"
            ), "API не вернул успешное добавление книг в корзину"

        return response.cookies.get("Nop.customer")

    def add_product_notebook(self, cookies):
        with allure.step("Добавляем ноутбук в корзину"):
            response = self.session.post(
                url=base_url + "addproducttocart/catalog/31/1/1",
                headers={"Accept": "application/json"},
                cookies=cookies,
                allow_redirects=False,
            )
            logger.info("Отправили запрос на добавление ноута в корзину")
            self.get_attach_data_response(response)
            assert response.json().get(
                "success"
            ), "API не вернул успешное добавление ноутбука"

        return response.cookies.get("Nop.customer")
