from playwright.sync_api import expect
from faker import Faker
from config import BASE_URL
import allure

fake = Faker()

email = fake.email()
street_address = fake.street_address()
city = fake.city()
zipcode = fake.zipcode()


@allure.feature("UI")
@allure.story("Add new order")
def test_checkout_order_success(shop_page):
    with allure.step("Open homepage"):
        expect(shop_page).to_have_url(BASE_URL.rstrip("/") + "/")
        expect(shop_page.locator('[data-cy="product-card"]')).to_have_count(10)
        product_cards = shop_page.locator('[data-cy="product-card"]')
        shop_page.locator('[data-cy="currency-switcher"]').select_option("USD")
        product_card_first = product_cards.first
        product_name_first = product_card_first.locator('[class*="ProductName"]')
        product_price_first = product_card_first.locator('[class*="ProductPrice"]')
        expect(product_name_first).to_have_text("Solar System Color Imager")
        expect(product_price_first.locator('[data-cy="product-price"]')).to_have_text("$ 175.00 ")

    with allure.step("Open product"):
        product_cards.first.click()

        expect(shop_page.locator('[data-cy="product-name"]')).to_be_visible()
        expect(shop_page.locator('[data-cy="product-add-to-cart"]')).to_have_text("Add To Cart")
        button_add_to_cart = shop_page.locator('[data-cy="product-add-to-cart"]')

    with allure.step("Open cart"):
        button_add_to_cart.click()

        expect(shop_page.get_by_text("Solar System Color Imager", exact=True)).to_be_visible()
        expect(shop_page.locator('[data-cy="product-price"]').first).to_have_text("$ 175.00 ")
        shop_page.locator('#email').fill(email)
        shop_page.locator('#street_address').fill(street_address)
        shop_page.locator('#zip_code').fill(zipcode)
        shop_page.locator('#city').fill(city)
        shop_page.locator('#state').fill('CA')
        shop_page.locator('#country').fill('United States')
        shop_page.locator('#credit_card_number').fill('4432-8015-6152-0454')
        shop_page.locator('#credit_card_expiration_month').select_option('3')
        shop_page.locator('#credit_card_expiration_year').select_option('2032')
        shop_page.locator('#credit_card_cvv').fill('987')
        shop_page.locator('[data-cy="currency-switcher"]').select_option("USD")
        expect(shop_page.locator('#email')).to_have_value(email)
        expect(shop_page.locator('#street_address')).to_have_value(street_address)
        expect(shop_page.locator('#zip_code')).to_have_value(zipcode)
        expect(shop_page.locator('#city')).to_have_value(city)
        expect(shop_page.locator('[data-cy="checkout-place-order"]')).to_have_text("Place Order")
        expect(shop_page.locator('[data-cy="checkout-place-order"]')).to_be_enabled()

    with allure.step("Create order"):
        shop_page.locator('[data-cy="checkout-place-order"]').click()
        expect(shop_page.get_by_role("heading", name="Your order is complete!")).to_be_visible()
        expect(shop_page.get_by_text("Solar System Color Imager", exact=True)).to_be_visible()




