from http import HTTPStatus

from categories.categories_api_func import CategoriesApiFunc
from seller.seller_api_func import UserApiFunc
from suppliers.suppliers_api_func import SuppliersApiFunc



def test_get_suppliers(api_client, registration_data, token_data,
                       random_category_name, registration_headers, db_client_with_supplier):
    """Тест на получение всех поставщиков (GET)"""
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
    # 5. Получение поставщика по ID
    response = SuppliersApiFunc.get_supplier_by_id(supplier_id=created_supplier_id,
                                                   headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK
    supplier_info = response.json()
    assert supplier_info["name"] == supplier_data["name"]


def test_get_supplier_by_non_existent_id(api_client, registration_data, token_data,
                                         random_category_name, registration_headers):
    """Тест на получение поставщика по не существующему ID."""
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
    # 3. Попытка получить поставщика по не существующему ID
    non_existent_id = 999999  # ID, которого не должно быть в базе данных
    response = SuppliersApiFunc.get_supplier_by_id(supplier_id=non_existent_id,
                                                   headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND, "Получение поставщика по не существующему ID должно было завершиться с ошибкой."