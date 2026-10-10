from config import BASE_URL
from playwright.sync_api import expect
import allure

@allure.feature("UI")
@allure.story("Products displayed")
def test_products_are_displayed(shop_page):
    with allure.step("Open homepage"):
        expect(shop_page).to_have_url(BASE_URL.rstrip("/") + "/")
        expect(shop_page.locator('[data-cy="product-card"]')).to_have_count(10)

        product_cards = shop_page.locator('[data-cy="product-card"]')
        cnt = product_cards.count()
        for i in range(cnt):
            product_card = product_cards.nth(i)

            product_names = product_card.locator('[class*="ProductName"]')
            product_prices = product_card.locator('[class*="ProductPrice"]')
            product_name = product_names.inner_text().strip()
            product_price = product_prices.inner_text().strip()
            assert product_name != ''
            assert product_price != ''

        product_card_first = product_cards.first
        product_name_first = product_card_first.locator('[class*="ProductName"]')
        product_price_first = product_card_first.locator('[class*="ProductPrice"]')
        expect(product_name_first).to_have_text("Solar System Color Imager")
        expect(product_price_first.locator('[data-cy="product-price"]')).to_have_text("$ 175.00 ")