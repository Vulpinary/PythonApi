from http import HTTPStatus

from seller.seller_api_func import UserApiFunc


def test_delete_seller_by_id_with_token(api_client, registration_data, token_data, registration_headers, db_client):
    """Тест удаления продавца по ID."""
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
    assert token is not None, "Отсутствует токен доступа в ответе."
    # 3. Запрос на удаление продавца по ID
    delete_response = UserApiFunc.delete_seller_by_id(seller_id=seller_id, headers={"Authorization": f"Bearer {token}"})
    assert delete_response.status_code == HTTPStatus.NO_CONTENT, "Удаление продавца не удалось."
    # 4. Проверка, что ресурс удален
    verify_response = UserApiFunc.get_seller_by_id(seller_id=seller_id, headers={"Authorization": f"Bearer {token}"})
    assert verify_response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, "Продавец все еще существует после удаления."


def test_delete_another_seller(api_client, registration_data, token_data, registration_headers, db_client):
    """Тест на удаление другого продавца."""
    # 1. Регистрация первого продавца
    registration_response1 = UserApiFunc.register(credential_body=registration_data)
    assert registration_response1.status_code == HTTPStatus.CREATED, "Регистрация первого продавца не удалась."
    seller_id1 = registration_response1.json().get("id")
    assert seller_id1 is not None, "Отсутствует ID первого продавца в ответе."
    # 2. Получение токена для первого продавца
    token_response1 = UserApiFunc.token(
        credential_body=token_data,
        headers=registration_headers
    )
    assert token_response1.status_code == HTTPStatus.OK, "Получение токена для первого продавца не удалось."
    token1 = token_response1.json().get("access_token")
    assert token1 is not None, "Отсутствует токен доступа для первого продавца в ответе."
    # 3. Регистрация второго продавца
    registration_data2 = {
        "username": "sell7412",
        "name": "Seller Two",
        "email": "sell132@example.com",
        "password": "pa1ssword123"
    }
    registration_response2 = UserApiFunc.register(credential_body=registration_data2)
    assert registration_response2.status_code == HTTPStatus.CREATED, "Регистрация второго продавца не удалась."
    seller_id2 = registration_response2.json().get("id")
    assert seller_id2 is not None, "Отсутствует ID второго продавца в ответе."
    # 4. Попытка удаления второго продавца первым продавцом
    delete_response = UserApiFunc.delete_seller_by_id(seller_id=seller_id2,
                                                      headers={"Authorization": f"Bearer {token1}"})
    assert delete_response.status_code == HTTPStatus.FORBIDDEN, "Удаление другого продавца должно было завершиться с ошибкой доступа."