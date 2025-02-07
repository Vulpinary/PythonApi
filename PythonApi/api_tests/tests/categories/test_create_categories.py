from http import HTTPStatus

from seller.seller_api_func import UserApiFunc
from categories.categories_api_func import CategoriesApiFunc


def test_create_category_with_token(api_client, registration_data, token_data, registration_headers, db_client_with_category, random_category_name):
    """Тест создания категории с использованием токена."""
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
    # 3. Создание категории с рандомным названием
    category_data = {"name": random_category_name}
    create_response = CategoriesApiFunc.create_category(category_data=category_data,
                                                        headers={"Authorization": f"Bearer {token}"})
    assert create_response.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
    # 4. Проверка созданной категории
    created_category_data = create_response.json()
    assert isinstance(created_category_data, dict), "Ответ должен быть словарем."
    assert created_category_data['name'] == random_category_name


def test_create_category_with_duplicate_name(api_client, registration_data, token_data, registration_headers,
                                             db_client_with_category):
    """Тест создания категории с уже существующим названием."""
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
    # 3. Создание категории с уникальным названием
    category_name = "Test Category"
    category_data = {"name": category_name}
    create_response1 = CategoriesApiFunc.create_category(category_data=category_data,
                                                         headers={"Authorization": f"Bearer {token}"})
    assert create_response1.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
    # 4. Попытка создать категорию с тем же названием
    create_response2 = CategoriesApiFunc.create_category(category_data=category_data,
                                                         headers={"Authorization": f"Bearer {token}"})
    assert create_response2.status_code == HTTPStatus.BAD_REQUEST, "Создание категории с дублирующимся названием должно было завершиться с ошибкой."
