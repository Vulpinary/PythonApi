from http import HTTPStatus

from categories.categories_api_func import CategoriesApiFunc
from products.products_api_func import ProductsApiFunc
from seller.seller_api_func import UserApiFunc


def test_get_id_products(api_client, registration_data, token_data, random_category_name,
                      random_product_data, registration_headers):
    """Тест получения продукта по ID с использованием токена."""
    # 1. Регистрация продавца
    registration_response = UserApiFunc.register(credential_body=registration_data)
    assert registration_response.status_code == HTTPStatus.CREATED, "Регистрация продавца не удалась."
    seller_id = registration_response.json().get("id")
    # 2. Получение токена
    token_response = UserApiFunc.token(
        credential_body=token_data,
        headers=registration_headers)
    assert token_response.status_code == HTTPStatus.OK, "Получение токена не удалось."
    token = token_response.json().get("access_token")
    # 3. Создание категории с рандомным названием
    category_data = {"name": random_category_name}
    response = CategoriesApiFunc.create_category(category_data=category_data,
                                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
    created_category_id = response.json().get("id")
    # 4. Заполняем category_id в product_data перед созданием продукта
    random_product_data["category_id"] = created_category_id
    # 5. Создание продукта в созданной категории
    response = ProductsApiFunc.create_product(product_data=random_product_data,
                                          headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.CREATED, "Создание продукта не удалось."
    # Получаем ID созданного продукта
    product_id = response.json().get("id")
    # 6. Получение продукта по ID
    response = ProductsApiFunc.get_product_by_id(product_id=product_id,
                                             headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK, "Получение продукта по ID не удалось."
    # Проверяем, что данные продукта совпадают с отправленными данными
    product_info = response.json()
    assert product_info["name"] == random_product_data["name"], "Имя продукта не совпадает."
    assert product_info["manufacturer"] == random_product_data["manufacturer"], "Производитель продукта не совпадает."
    assert float(product_info["price"]) == random_product_data["price"], "Цена продукта не совпадает."


def test_get_product_by_non_existent_id(api_client, registration_data, token_data, random_category_name,
                                        random_product_data, registration_headers):
    """Тест получения продукта по не существующему ID."""
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
    # 3. Попытка получить продукт по не существующему ID
    non_existent_id = 999999  # ID, которого не должно быть в базе данных
    response = ProductsApiFunc.get_product_by_id(product_id=non_existent_id,
                                                 headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.NOT_FOUND, "Получение продукта по не существующему ID должно было завершиться с ошибкой."