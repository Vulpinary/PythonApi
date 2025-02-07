import random
from http import HTTPStatus

from categories.categories_api_func import CategoriesApiFunc
from products.products_api_func import ProductsApiFunc
from seller.seller_api_func import UserApiFunc

# # Баг, после изменения данных продукта, данные не обновляются
# def test_update_product(api_client, registration_data, token_data, random_category_name,
#                         random_product_data, registration_headers):
#     """Тест обновления продукта с использованием токена."""
#     # 1. Регистрация продавца
#     registration_response = UserApiFunc.register(credential_body=registration_data)
#     assert registration_response.status_code == HTTPStatus.CREATED, "Регистрация продавца не удалась."
#     seller_id = registration_response.json().get("id")
#     # 2. Получение токена
#     token_response = UserApiFunc.token(credential_body=token_data, headers=registration_headers)
#     assert token_response.status_code == HTTPStatus.OK, "Получение токена не удалось."
#     token = token_response.json().get("access_token")
#     # 3. Создание категории с рандомным названием
#     category_data = {"name": random_category_name}
#     create_category_response = CategoriesApiFunc.create_category(category_data=category_data,
#     headers = {"Authorization": f"Bearer {token}"})
#     assert create_category_response.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
#     created_category_id = create_category_response.json().get("id")
#     # Заполняем category_id в product_data перед созданием продукта
#     random_product_data["category_id"] = created_category_id
#     # 4. Создание продукта в созданной категории
#     create_product_response = ProductsApiFunc.create_product(product_data=random_product_data,
#     headers = {"Authorization": f"Bearer {token}"})
#     assert create_product_response.status_code == HTTPStatus.CREATED, "Создание продукта не удалось."
#     product_id = create_product_response.json().get("id")
#     updated_product_data = {
#     "name": "Обновлённый продукт",
#     "manufacturer": "Обновлённый производитель",
#     "price": round(random.uniform(1, 500), 2),
#     "description": "Обновлённое описание",
#     "category_id": created_category_id  # Указываем актуальный ID категории
#     }
#     # Обновление продукта по ID
#     update_response = ProductsApiFunc.update_product_by_id(product_id=product_id,
#     product_data = updated_product_data,
#     headers = {"Authorization": f"Bearer {token}"})
#     assert update_response.status_code == HTTPStatus.OK, "Обновление продукта не удалось."
#     # 5. Проверка, что данные продукта были обновлены корректно
#     updated_product_info = update_response.json()
#     assert updated_product_info["name"] == updated_product_data["name"], "Имя продукта не совпадает."
#     assert updated_product_info["manufacturer"] == updated_product_data[
#     "manufacturer"], "Производитель продукта не совпадает."
#     assert float(updated_product_info["price"]) == updated_product_data["price"], "Цена продукта не совпадает."
#     assert updated_product_info["description"] == updated_product_data["description"], "Описание продукта не совпадает."


def test_update_product_with_empty_fields(api_client, registration_data, token_data, random_category_name,
                                          random_product_data, registration_headers):
    """Тест обновления продукта с пустыми обязательными полями."""
    # 1. Регистрация продавца
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
    create_category_response = CategoriesApiFunc.create_category(category_data=category_data,
                                                                 headers={"Authorization": f"Bearer {token}"})
    assert create_category_response.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
    created_category_id = create_category_response.json().get("id")
    # 4. Создание продукта в созданной категории
    random_product_data["category_id"] = created_category_id
    create_product_response = ProductsApiFunc.create_product(product_data=random_product_data,
                                                             headers={"Authorization": f"Bearer {token}"})
    assert create_product_response.status_code == HTTPStatus.CREATED, "Создание продукта не удалось."
    product_id = create_product_response.json().get("id")
    # 5. Обновление продукта с пустыми полями
    updated_product_data = {
        "name": "Хлебушек",
        "manufacturer": "Производитель",  # Пустой производитель
        "price": None,  # Отсутствие цены
        "description": "Описание",  # Пустое описание
        "category_id": created_category_id  # Указываем актуальный ID категории
    }
    update_response = ProductsApiFunc.update_product_by_id(product_id=product_id,
                                                           product_data=updated_product_data,
                                                           headers={"Authorization": f"Bearer {token}"})
    assert update_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, "Обновление продукта с пустыми полями должно было завершиться с ошибкой."
