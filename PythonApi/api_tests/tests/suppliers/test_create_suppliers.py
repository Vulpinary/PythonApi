from http import HTTPStatus

from categories.categories_api_func import CategoriesApiFunc
from seller.seller_api_func import UserApiFunc
from suppliers.suppliers_api_func import SuppliersApiFunc



def test_create_supplier(api_client, registration_data, token_data,
                         random_category_name,
                         registration_headers, db_client_with_supplier):
    """Тест на создание поставщика."""
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
    # 4. Устанавливаем данные для поставщика с фиксированными значениями
    supplier_data = {
        "name": "Test Supplier",
        "email": "supplier@example.com",
        "phone": "+1234567890",
        "address": "123 Supplier St",
        "category_id": created_category_id,
        "seller_id": seller_id
    }
    # 5. Создание поставщика с данными и ID категории и продавца
    create_supplier_response = SuppliersApiFunc.create_supplier(supplier_data=supplier_data,
                                                                headers={"Authorization": f"Bearer {token}"})
    assert create_supplier_response.status_code == HTTPStatus.CREATED, "Создание поставщика не удалось."
    created_supplier_info = create_supplier_response.json()
    # Проверка наличия всех необходимых полей
    assert created_supplier_info["name"] == supplier_data["name"], "Имя поставщика не совпадает."
    assert created_supplier_info["email"] == supplier_data["email"], "Email поставщика не совпадает."
    assert created_supplier_info["phone"] == supplier_data["phone"], "Телефон поставщика не совпадает."
    assert created_supplier_info["address"] == supplier_data["address"], "Адрес поставщика не совпадает."
    # Проверка ID категории и ID продавца
    assert created_supplier_info["category"]["id"] == supplier_data["category_id"], "ID категории не совпадает."
    assert created_supplier_info["seller_id"] == supplier_data["seller_id"], "ID продавца не совпадает."

# # Баг. Поле Name поставщика, обязателен к заполнению
# def test_create_supplier_with_empty_name(api_client, registration_data, token_data,
#                                          random_category_name,
#                                          registration_headers, db_client_with_supplier):
#     """Тест на создание поставщика с пустым именем."""
#     # 1. Регистрация продавца
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
#     # 3. Создание категории с рандомным названием
#     category_data = {"name": random_category_name}
#     create_category_response = CategoriesApiFunc.create_category(category_data=category_data,
#                                                                  headers={"Authorization": f"Bearer {token}"})
#     assert create_category_response.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
#     created_category_id = create_category_response.json().get("id")
#     assert created_category_id is not None, "Отсутствует ID созданной категории в ответе."
#     # 4. Устанавливаем данные для поставщика с пустым именем
#     supplier_data = {
#         "name": "",  # Пустое имя
#         "email": "supplier@example.com",
#         "phone": "+1234567890",
#         "address": "123 Supplier St",
#         "category_id": created_category_id,
#         "seller_id": seller_id
#     }
#     # 5. Попытка создания поставщика с пустым именем
#     create_supplier_response = SuppliersApiFunc.create_supplier(supplier_data=supplier_data,
#                                                                 headers={"Authorization": f"Bearer {token}"})
#     assert create_supplier_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, "Создание поставщика с пустым именем должно было завершиться с ошибкой."