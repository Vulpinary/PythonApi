from http import HTTPStatus

from seller.seller_api_func import UserApiFunc
from categories.categories_api_func import CategoriesApiFunc


def test_get_category_by_id_with_token(api_client, registration_data, token_data, registration_headers, db_client_with_category, random_category_name):
    """Тест получения категории по ID с использованием токена."""
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
    # 3. Создание категории с рандомным названием
    category_data = {"name": random_category_name}
    create_response = CategoriesApiFunc.create_category(category_data=category_data,
                                                        headers={"Authorization": f"Bearer {token}"})
    assert create_response.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
    # 4. Получение ID созданной категории
    created_category_id = create_response.json().get("id")
    assert created_category_id is not None, "Отсутствует ID созданной категории в ответе."
    # 5. Запрос GET для получения категории по ID
    response = CategoriesApiFunc.get_category_by_id(category_id=created_category_id,
                                                    headers={"Authorization": f"Bearer {token}"})
    # 6. Проверка статуса ответа на получение категории
    assert response.status_code == HTTPStatus.OK, "Получение категории по ID не удалось."
    # 7. Проверка, что возвращенные данные соответствуют запрашиваемой категории
    supplier_info = response.json()
    assert supplier_info.get("id") == created_category_id, "ID категории не совпадает."
    assert supplier_info.get("name") == random_category_name, "Название категории не совпадает."


def test_get_category_by_non_existent_id(api_client, registration_data, token_data, registration_headers,
                                         db_client_with_category):
    """Тест получения категории по не существующему ID."""
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
    assert token is not None, "Отсутствует токен доступа в ответе."
    # 3. Попытка получить категорию по не существующему ID
    non_existent_id = 999999  # ID, которого не должно быть в базе данных
    response = CategoriesApiFunc.get_category_by_id(category_id=non_existent_id,
                                                    headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, "Получение категории по не существующему ID должно было завершиться с ошибкой."