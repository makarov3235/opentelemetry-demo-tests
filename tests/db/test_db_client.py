import allure

@allure.feature("DB")
@allure.story("DB connect")
def test_db_connection(db_client):
    result = db_client.execute(
        'SELECT * FROM accounting."order" LIMIT 1'
    )

    assert result