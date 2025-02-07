from http import HTTPStatus

from seller.seller_api_func import UserApiFunc
from categories.categories_api_func import CategoriesApiFunc


def test_delete_category_with_token(api_client, registration_data, token_data, registration_headers, db_client_with_category, random_category_name):
    """Тест удаления категории с использованием токена."""
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
    response = CategoriesApiFunc.create_category(category_data=category_data,
                                                 headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
    # 4. Получение ID созданной категории
    created_category_id = response.json().get("id")
    # 5. Удаление категории по ID
    delete_response = CategoriesApiFunc.delete_category_by_id(category_id=created_category_id,
                                                              headers={"Authorization": f"Bearer {token}"})
    assert delete_response.status_code == HTTPStatus.NO_CONTENT, "Удаление категории не удалось."
    # 6. Проверка, что категория была удалена
    get_response = CategoriesApiFunc.get_category_by_id(category_id=created_category_id,
                                                        headers={"Authorization": f"Bearer {token}"})
    assert get_response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, "Ожидается ошибка при попытке получить удаленную категорию."


def test_delete_category_by_non_existent_id(api_client, registration_data, token_data, registration_headers,
                                            db_client_with_category):
    """Тест удаления категории по не существующему ID."""
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
    # 3. Попытка удаления категории по не существующему ID
    non_existent_id = 999999  # ID, которого не должно быть в базе данных
    delete_response = CategoriesApiFunc.delete_category_by_id(category_id=non_existent_id,
                                                              headers={"Authorization": f"Bearer {token}"})
    assert delete_response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, "Удаление категории по не существующему ID должно было завершиться с ошибкой."