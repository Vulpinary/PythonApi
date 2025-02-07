from http import HTTPStatus

from seller.seller_api_func import UserApiFunc
from categories.categories_api_func import CategoriesApiFunc


def test_get_categories_with_token(api_client, registration_data, token_data, registration_headers, db_client_with_category):
    """Тест получения всех категорий с использованием токена."""

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

    # 3. Запрос GET для получения всех категорий
    response = CategoriesApiFunc.get(headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.OK, "Получение списка категорий не удалось."

    # 4. Проверка структуры ответа
    categories_data = response.json()

    assert isinstance(categories_data, list), "Ответ должен быть списком."