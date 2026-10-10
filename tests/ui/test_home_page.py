from playwright.sync_api import expect
from config import BASE_URL
import allure

@allure.feature("UI")
@allure.story("Homepage displayed")
def test_main_page_opens(shop_page):
    with allure.step("Open homepage"):
        expect(shop_page).to_have_url(BASE_URL.rstrip("/") + "/")
        expect(shop_page.get_by_role('heading', name = 'The best telescopes to see the world closer', level=1)).to_have_text('The best telescopes to see the world closer')