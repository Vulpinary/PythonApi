from http import HTTPStatus

from seller.seller_api_func import UserApiFunc


def test_get_seller_with_token(api_client, registration_data, token_data, registration_headers, db_client):
    """Тест получения информации о продавце."""

    # 1. Регистрация
    registration_response = UserApiFunc.register(credential_body=registration_data)
    assert registration_response.status_code == HTTPStatus.CREATED, "Регистрация продавца не удалась."
    seller_id = registration_response.json().get("id")

    # 2. Получение токена
    token_response = UserApiFunc.token(
        credential_body=token_data,
        headers=registration_headers
    )
    assert token_response.status_code == HTTPStatus.OK, "Получение токена не удалось."
    token = token_response.json().get("access_token")

    # 3. Получение информации о продавце
    seller_response = UserApiFunc.get(headers={"Authorization": f"Bearer {token}"})
    assert seller_response.status_code == HTTPStatus.OK, "Получение информации о продавце не удалось."

    # 4. Проверка тела ответа
    seller_data = seller_response.json()
    assert isinstance(seller_data, list), "Ответ должен быть списком."

