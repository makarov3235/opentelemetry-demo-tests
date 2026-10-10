from config import BASE_URL

import pytest

@pytest.fixture
def shop_page(page):
    page.goto(BASE_URL, wait_until="domcontentloaded")
    page.locator('[data-cy="currency-switcher"]').select_option("USD")
    yield page