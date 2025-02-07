
from http import HTTPStatus

from categories.categories_api_func import CategoriesApiFunc
from products.products_api_func import ProductsApiFunc
from seller.seller_api_func import UserApiFunc


def test_create_product(api_client, registration_data, token_data, random_category_name,
                        random_product_data, registration_headers, db_client_with_product):
    """Тест создания продукта с использованием токена."""
    # 1. Регистрация продавца
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
    # 3. Создание категории с рандомным названием
    category_data = {"name": random_category_name}
    create_category_response = CategoriesApiFunc.create_category(category_data=category_data,
                                                                 headers={"Authorization": f"Bearer {token}"})
    assert create_category_response.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
    created_category_id = create_category_response.json().get("id")
    # Заполняем category_id в product_data перед созданием продукта
    random_product_data["category_id"] = created_category_id
    # 4. Создание продукта в созданной категории
    create_product_response = ProductsApiFunc.create_product(product_data=random_product_data,
                                                             headers={"Authorization": f"Bearer {token}"})
    # 5. Проверка статуса ответа на создание продукта
    assert create_product_response.status_code == HTTPStatus.CREATED, "Создание продукта не удалось."
    # 6. Проверка, что продукт создан с правильными данными
    created_product_id = create_product_response.json().get("id")
    product_info = create_product_response.json()
    assert product_info["name"] == random_product_data["name"], "Имя продукта не совпадает."
    assert product_info["manufacturer"] == random_product_data["manufacturer"], "Производитель продукта не совпадает."
    assert float(product_info["price"]) == random_product_data["price"], "Цена продукта не совпадает."

# # Баг. Создание продукта с пустым именем должно было завершиться с ошибкой
# def test_create_product_with_empty_name(api_client, registration_data, token_data, random_category_name,
#                                         random_product_data, registration_headers, db_client_with_product):
#     """Тест создания продукта с пустым именем."""
#     # 1. Регистрация продавца
#     registration_response = UserApiFunc.register(credential_body=registration_data)
#     assert registration_response.status_code == HTTPStatus.CREATED, "Регистрация продавца не удалась."
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
#     # 4. Создание продукта с пустым именем
#     product_data = random_product_data.copy()  # Копируем данные продукта
#     product_data["name"] = ""  # Устанавливаем пустое имя
#     product_data["category_id"] = created_category_id  # Устанавливаем ID категории
#     create_product_response = ProductsApiFunc.create_product(product_data=product_data,
#                                                              headers={"Authorization": f"Bearer {token}"})
#     assert create_product_response.status_code == HTTPStatus.BAD_REQUEST, "Создание продукта с пустым именем должно было завершиться с ошибкой."


def test_create_product_with_invalid_ids(api_client, registration_data, token_data, random_category_name,
                                         random_product_data, registration_headers, db_client_with_product):
    """Тест создания продукта с неверным category_id или supplier_id."""
    # 1. Регистрация продавца
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
    # 3. Создание продукта с неверным category_id
    product_data = random_product_data.copy()  # Копируем данные продукта
    product_data["category_id"] = 999999  # Устанавливаем неверный ID категории
    create_product_response = ProductsApiFunc.create_product(product_data=product_data,
                                                             headers={"Authorization": f"Bearer {token}"})
    assert create_product_response.status_code == HTTPStatus.BAD_REQUEST, "Создание продукта с неверным category_id должно было завершиться с ошибкой."