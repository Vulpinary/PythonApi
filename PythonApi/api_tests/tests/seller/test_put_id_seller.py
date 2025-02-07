from http import HTTPStatus

from conftest import fake
from seller.seller_api_func import UserApiFunc


def test_get_seller_by_id_with_token(api_client, registration_data, token_data, registration_headers, db_client):
    """Тест получения информации о продавце по ID после обновления данных."""
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
    # 3. Обновление данных продавца
    new_name = fake.name()
    new_email = fake.email()
    update_data = {
        "name": new_name,
        "email": new_email,
    }
    update_response = UserApiFunc.put_seller_by_id(seller_id=seller_id, json=update_data,
                                                   headers={"Authorization": f"Bearer {token}"})
    assert update_response.status_code == HTTPStatus.OK, "Обновление данных продавца не удалось."
    # 4. Запрос GET с использованием извлеченного seller_id
    response = UserApiFunc.get_seller_by_id(seller_id=seller_id, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK, "Получение продавца по ID не удалось."
    # 5. Проверка обновленных полей
    response_data = response.json()
    assert isinstance(response_data, dict), "Ответ должен быть словарем."
    assert response_data['id'] == seller_id, "ID продавца не совпадает."
    assert response_data['name'] == new_name, "Имя продавца не совпадает."
    assert response_data['email'] == new_email, "Email продавца не совпадает."

# #Баг. Можно поменять поле Usrename
# def test_update_seller_username(api_client, registration_data, token_data, registration_headers, db_client):
#     """Тест на обновление имени пользователя (должно завершиться с ошибкой)."""
#     # 1. Регистрация
#     registration_response = UserApiFunc.register(credential_body=registration_data)
#     assert registration_response.status_code == HTTPStatus.CREATED, "Регистрация продавца не удалась."
#     seller_id = registration_response.json().get("id")
#     assert seller_id is not None, "Отсутствует ID продавца в ответе."
#     # 2. Получение токена
#     token_response = UserApiFunc.token(
#         credential_body=token_data,
#         headers=registration_headers
#     )
#     assert token_response.status_code == HTTPStatus.OK, "Получение токена не удалось."
#     token = token_response.json().get("access_token")
#     assert token is not None, "Отсутствует токен доступа в ответе."
#     # 3. Обновление имени пользователя (должно завершиться с ошибкой)
#     new_username = "new_username"
#     update_data = {
#         "username": new_username,
#     }
#     update_response = UserApiFunc.put_seller_by_id(seller_id=seller_id, json=update_data,
#                                                    headers={"Authorization": f"Bearer {token}"})
#     assert update_response.status_code == HTTPStatus.BAD_REQUEST, "Обновление имени пользователя должно было завершиться с ошибкой."
