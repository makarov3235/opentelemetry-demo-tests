import allure

@allure.feature("Main Page")
@allure.story("Get mainpage HTML")
def test_get_main_page(mainpage_client):
    response = mainpage_client.get_mainpage()

    assert response.status_code == 200


@allure.feature("Main Page")
@allure.story("Get get_currencies")
def test_get_currencies(mainpage_client):
    response = mainpage_client.get_currencies()

    assert response.status_code == 500
    assert response.json()

