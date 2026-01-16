def test_add_product_book_and_assert_qty_and_count_product(
    prepared_cart, api_login, cookies
):
    cart = prepared_cart

    get_cookies_after_add_product = api_login.add_product_book(cookies)
    cart.set_cookies_and_refresh_browser(cookies, get_cookies_after_add_product)

    cart.assert_qty_product_in_cart()
    assert cart.get_len_count_prodict_in_cart() == 1


def test_add_two_products_and_assert_data_product_in_cart(
    prepared_cart, api_login, cookies
):
    cart = prepared_cart

    api_login.add_product_book(cookies)
    get_cookies_after_add_product_notebook = api_login.add_product_notebook(cookies)
    cart.set_cookies_and_refresh_browser(cookies, get_cookies_after_add_product_notebook)

    assert cart.get_len_count_prodict_in_cart() == 2
    cart.assert_data_prodict_in_card(0, "Computing and Internet", "10.00")
    cart.assert_data_prodict_in_card(1, "14.1-inch Laptop", "1590.00")
