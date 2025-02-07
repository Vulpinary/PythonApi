from http import HTTPStatus


from seller.seller_api_func import UserApiFunc


def test_get_seller_by_id_with_token(api_client, registration_data, token_data, registration_headers, db_client):
    """Тест получения информации о продавце по ID."""

    # 1. Регистрация
    registration_response = UserApiFunc.register(credential_body=registration_data)
    assert registration_response.status_code == HTTPStatus.CREATED, "Регистрация продавца не удалась."

    seller_id = registration_response.json().get("id")
    assert seller_id is not None, "Отсутствует ID продавца в ответе."

    # 2. Получение токена
    token_response = UserApiFunc.token(
        credential_body=token_data,
        headers=registration_headers
    )

    assert token_response.status_code == HTTPStatus.OK, "Получение токена не удалось."

    token = token_response.json().get("access_token")

    # 3. Запрос GET с использованием извлеченного seller_id
    seller_response = UserApiFunc.get_seller_by_id(seller_id=seller_id, headers={"Authorization": f"Bearer {token}"})

    assert seller_response.status_code == HTTPStatus.OK, "Получение продавца по ID не удалось."

    # 4. Проверка тела ответа
    response_data = seller_response.json()

    assert isinstance(response_data, dict), "Ответ должен быть словарем."

    # Проверка наличия и соответствия значений полей
    assert response_data['id'] == seller_id, "ID продавца не совпадает."
    assert response_data['username'] == registration_data['username'], "Имя пользователя не совпадает."
    assert response_data['name'] == registration_data['name'], "Имя не совпадает."
    assert response_data['email'] == registration_data['email'], "Email не совпадает."
    assert response_data['is_active'] is True, "Статус активности неверен."


def test_get_seller_by_non_existent_id(api_client, registration_data, token_data, registration_headers, db_client):
    """Тест получения информации о продавце по не существующему ID."""
    # 1. Регистрация
    registration_response = UserApiFunc.register(credential_body=registration_data)
    assert registration_response.status_code == HTTPStatus.CREATED, "Регистрация продавца не удалась."
    # 2. Получение токена
    token_response = UserApiFunc.token(
        credential_body=token_data,
        headers=registration_headers
    )
    assert token_response.status_code == HTTPStatus.OK, "Получение токена не удалось."
    token = token_response.json().get("access_token")
    # 3. Запрос GET с не существующим ID
    non_existent_id = 999999  # ID, которого не должно быть в базе данных
    response = UserApiFunc.get_seller_by_id(seller_id=non_existent_id, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND, "Получение продавца по не существующему ID должно было завершиться с ошибкой."