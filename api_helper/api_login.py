import json
import logging
import re

import allure
import requests
from allure_commons.types import AttachmentType

from config import api_login_url, base_url

logger = logging.getLogger(__name__)


class ApiHelper:
    def __init__(self):
        self.session = requests.Session()

    @staticmethod
    def log_request_and_response(request, response):
        request_info = f"Request Method: {request.method}\nRequest URL: {request.url}\n"

        if request.body:
            request_info += f"Request Body: {request.body}\n"
        if request.headers:
            request_info += f"Request Headers: {json.dumps(dict(request.headers), indent=4, sort_keys=True)}\n"
        allure.attach(
            body=request_info,
            name="Request Info",
            attachment_type=AttachmentType.TEXT,
            extension="txt",
        )

        allure.attach(
            body=str(response.status_code),
            name="Response Status Code",
            attachment_type=AttachmentType.TEXT,
            extension="txt",
        )

        try:
            resp_body_json = response.json()
            resp_body_str = json.dumps(resp_body_json, indent=4, sort_keys=True)

            if "updateflyoutcartsectionhtml" in resp_body_json:
                html_code = resp_body_json["updateflyoutcartsectionhtml"]
                formatted_html = re.sub(
                    r">\s+<", "><", html_code
                )  # Удаляем лишние пробелы между тегами
                formatted_html = re.sub(
                    r">\s+", ">", formatted_html
                )  # Удаляем лишние пробелы после тегов
                formatted_html = re.sub(
                    r"\s+<", "<", formatted_html
                )  # Удаляем лишние пробелы перед тегами
                resp_body_json["updateflyoutcartsectionhtml"] = formatted_html
                resp_body_str = json.dumps(resp_body_json, indent=4, sort_keys=True)
        except ValueError:
            resp_body_str = str(response.text)

        allure.attach(
            body=resp_body_str,
            name="Response Body",
            attachment_type=AttachmentType.JSON,
            extension="json",
        )

        allure.attach(
            body=str(response.cookies),
            name="Response Cookies",
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

            self.log_request_and_response(response.request, response)
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
            self.log_request_and_response(response.request, response)
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

            self.log_request_and_response(response.request, response)
            assert response.json().get(
                "success"
            ), "API не вернул успешное добавление ноутбука"

        return response.cookies.get("Nop.customer")
