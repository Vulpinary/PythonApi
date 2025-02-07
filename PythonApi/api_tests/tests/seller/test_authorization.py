from http import HTTPStatus

from seller.seller_api_func import UserApiFunc


def test_seller_authorization(api_client, registration_data, db_client):
    """Тест: авторизация продавца после регистрации."""
    # 1. Регистрация
    response = UserApiFunc.register(credential_body=registration_data)
    assert response.status_code == HTTPStatus.CREATED, "Регистрация продавца не удалась."
    # 2. Авторизация
    login_response = UserApiFunc.token(
        credential_body={
            "username": registration_data["username"],
            "password": registration_data["password"]
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login_response.status_code == HTTPStatus.OK
    # 3. Проверка наличия токена в ответе
    login_response_data = login_response.json()
    assert "access_token" in login_response_data


def test_seller_authorization_with_invalid_data(api_client, registration_data, db_client):
    """Тест: авторизация с невалидными данными."""
    # 1. Регистрация
    response = UserApiFunc.register(credential_body=registration_data)
    assert response.status_code == HTTPStatus.CREATED, "Регистрация продавца не удалась."
    # 2. Авторизация с невалидными данными
    invalid_login_response = UserApiFunc.token(
        credential_body={
            "username": registration_data["username"],
            "password": "wrong_password"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert invalid_login_response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, "Авторизация с невалидными данными должна была завершиться с ошибкой."