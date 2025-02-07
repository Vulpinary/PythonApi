from http import HTTPStatus

from categories.categories_api_func import CategoriesApiFunc
from seller.seller_api_func import UserApiFunc
from suppliers.suppliers_api_func import SuppliersApiFunc


def test_update_supplier(api_client, registration_data, token_data,
                         random_category_name, registration_headers):
    """Тест на обновление поставщика по ID (PUT)"""
    # 1. Регистрация продавца
    registration_response = UserApiFunc.register(credential_body=registration_data)
    assert registration_response.status_code == HTTPStatus.CREATED, "Регистрация продавца не удалась."
    seller_id = registration_response.json().get("id")
    assert seller_id is not None, "Отсутствует ID продавца в ответе."
    # 2. Получение токена
    token_response = UserApiFunc.token(
        credential_body=token_data,
        headers=registration_headers)
    assert token_response.status_code == HTTPStatus.OK, "Получение токена не удалось."
    token = token_response.json().get("access_token")
    assert token is not None, "Отсутствует токен доступа в ответе."
    # 3. Создание категории с рандомным названием
    category_data = {"name": random_category_name}
    create_category_response = CategoriesApiFunc.create_category(category_data=category_data,
                                                                 headers={"Authorization": f"Bearer {token}"})
    assert create_category_response.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
    created_category_id = create_category_response.json().get("id")
    assert created_category_id is not None, "Отсутствует ID созданной категории в ответе."
    # 4. Создание поставщика
    supplier_data = {
        "name": "Test Supplier",
        "email": "supplier@example.com",
        "phone": "+1234567890",
        "address": "123 Supplier St",
        "category_id": created_category_id,
        "seller_id": seller_id
    }
    create_supplier_response = SuppliersApiFunc.create_supplier(supplier_data=supplier_data,
                                                                headers={"Authorization": f"Bearer {token}"})
    assert create_supplier_response.status_code == HTTPStatus.CREATED, "Создание поставщика не удалось."
    created_supplier_id = create_supplier_response.json().get("id")
    assert created_supplier_id is not None, "Отсутствует ID созданного поставщика в ответе."
    # 5. Обновление данных поставщика по ID
    updated_supplier_data = {
        "name": "Updated Supplier Name",
        "email": "updated@example.com",
        "phone": "+0987654321",
        "address": "321 Updated Supplier St",
        # category_id не обновляем, оставляем прежним
        "category_id": created_category_id,
        "seller_id": seller_id  # Убедитесь, что seller_id также передается при обновлении (если требуется)
    }
    update_response = SuppliersApiFunc.update_supplier_by_id(supplier_id=created_supplier_id,
                                                         supplier_data=updated_supplier_data,
                                                         headers={"Authorization": f"Bearer {token}"})
    assert update_response.status_code == HTTPStatus.OK, "Обновление данных поставщика не удалось."
    # Проверка обновленных данных
    updated_info_response = SuppliersApiFunc.get_supplier_by_id(supplier_id=created_supplier_id,
                                                            headers={"Authorization": f"Bearer {token}"})
    assert updated_info_response.status_code == HTTPStatus.OK, "Получение обновленного поставщика не удалось."
    updated_info = updated_info_response.json()
    assert updated_info["name"] == updated_supplier_data["name"], "Имя обновленного поставщика не совпадает."
    assert updated_info["email"] == updated_supplier_data["email"], "Email обновленного поставщика не совпадает."
    assert updated_info["phone"] == updated_supplier_data["phone"], "Телефон обновленного поставщика не совпадает."
    assert updated_info["address"] == updated_supplier_data["address"], "Адрес обновленного поставщика не совпадает."


def test_update_supplier_with_invalid_id(api_client, registration_data, token_data,
                                         random_category_name, registration_headers):
    """Тест на обновление поставщика с неверным ID."""
    # 1. Регистрация продавца
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
    # 3. Попытка обновления поставщика с неверным ID
    non_existent_id = 999999  # ID, которого не должно быть в базе данных
    updated_supplier_data = {
        "name": "Updated Supplier Name",
        "email": "updated@example.com",
        "phone": "+0987654321",
        "address": "321 Updated Supplier St",
        "category_id": 1,  # Любой существующий или несуществующий ID категории
        "seller_id": seller_id
    }
    update_response = SuppliersApiFunc.update_supplier_by_id(supplier_id=non_existent_id,
                                                             supplier_data=updated_supplier_data,
                                                             headers={"Authorization": f"Bearer {token}"})
    assert update_response.status_code == HTTPStatus.NOT_FOUND, "Обновление поставщика с неверным ID должно было завершиться с ошибкой."


def test_update_supplier_with_empty_fields(api_client, registration_data, token_data,
                                           random_category_name, registration_headers):
    """Тест на обновление поставщика с пустыми обязательными полями."""

    # 1. Регистрация продавца
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
    create_category_response = CategoriesApiFunc.create_category(category_data=category_data,
                                                                 headers={"Authorization": f"Bearer {token}"})
    assert create_category_response.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
    created_category_id = create_category_response.json().get("id")
    assert created_category_id is not None, "Отсутствует ID созданной категории в ответе."

    # 4. Создание поставщика
    supplier_data = {
        "name": "Test Supplier",
        "email": "supplier@example.com",
        "phone": "+1234567890",
        "address": "123 Supplier St",
        "category_id": created_category_id,
        "seller_id": seller_id
    }
    create_supplier_response = SuppliersApiFunc.create_supplier(supplier_data=supplier_data,
                                                                headers={"Authorization": f"Bearer {token}"})
    assert create_supplier_response.status_code == HTTPStatus.CREATED, "Создание поставщика не удалось."
    created_supplier_id = create_supplier_response.json().get("id")
    assert created_supplier_id is not None, "Отсутствует ID созданного поставщика в ответе."

    # 5. Обновление поставщика с пустыми полями
    updated_supplier_data = {
        "name": "",  # Пустое имя
        "email": "",  # Пустой email
        "phone": "",  # Пустой телефон
        "address": "адрес 32",
        "category_id": created_category_id,
        "seller_id": seller_id
    }
    update_response = SuppliersApiFunc.update_supplier_by_id(supplier_id=created_supplier_id,
                                                             supplier_data=updated_supplier_data,
                                                             headers={"Authorization": f"Bearer {token}"})
    assert update_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, "Обновление поставщика с пустыми полями должно было завершиться с ошибкой."