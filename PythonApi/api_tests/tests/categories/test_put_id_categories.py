from http import HTTPStatus

from seller.seller_api_func import UserApiFunc
from categories.categories_api_func import CategoriesApiFunc

def test_update_category_name_with_token(api_client, registration_data, token_data, registration_headers, db_client_with_category, random_category_name):
    """Тест обновления имени категории с использованием токена."""
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
    created_category_id = response.json().get("id")
    # 4. Обновление имени категории
    new_category_name = random_category_name  # Генерируем новое название для категории
    update_data = {"name": new_category_name}
    response = CategoriesApiFunc.update_category_by_id(category_id=created_category_id,
                                                       category_data=update_data,
                                                       headers={"Authorization": f"Bearer {token}"})
    # 5. Проверка статуса ответа на обновление имени категории
    assert response.status_code == HTTPStatus.OK, "Обновление имени категории не удалось."
    # 6. Проверка, что имя категории было обновлено корректно
    response = CategoriesApiFunc.get_category_by_id(category_id=created_category_id,
                                                    headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK, "Получение обновленной категории не удалось."
    updated_category_info = response.json()
    assert updated_category_info.get("name") == new_category_name, "Название обновленной категории не совпадает."


def test_update_category_by_non_existent_id(api_client, registration_data, token_data, registration_headers,
                                            db_client_with_category, random_category_name):
    """Тест обновления категории по не существующему ID."""
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
    # 3. Попытка обновления категории по не существующему ID
    non_existent_id = 999999  # ID, которого не должно быть в базе данных
    new_category_name = random_category_name  # Генерируем новое название для категории
    update_data = {"name": new_category_name}
    response = CategoriesApiFunc.update_category_by_id(category_id=non_existent_id,
                                                       category_data=update_data,
                                                       headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, "Обновление категории по не существующему ID должно было завершиться с ошибкой."