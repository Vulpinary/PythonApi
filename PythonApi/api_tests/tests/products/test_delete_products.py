from http import HTTPStatus

from categories.categories_api_func import CategoriesApiFunc
from products.products_api_func import ProductsApiFunc
from seller.seller_api_func import UserApiFunc


def test_delete_product(api_client, registration_data, token_data, random_category_name,
                        random_product_data, registration_headers):
    """Тест удаления продукта с использованием токена."""
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
    # Заполняем category_id в product_data перед созданием продукта
    random_product_data["category_id"] = created_category_id
    # 4. Создание продукта в созданной категории
    create_product_response = ProductsApiFunc.create_product(product_data=random_product_data,
                                                             headers={"Authorization": f"Bearer {token}"})
    assert create_product_response.status_code == HTTPStatus.CREATED, "Создание продукта не удалось."
    product_id = create_product_response.json().get("id")
    # 5. Удаление продукта по ID
    delete_response = ProductsApiFunc.delete_product_by_id(product_id=product_id,
                                                           headers={"Authorization": f"Bearer {token}"})
    assert delete_response.status_code == HTTPStatus.NO_CONTENT, "Удаление продукта не удалось."
    # 6. Проверка, что продукт был удалён
    get_response = ProductsApiFunc.get_product_by_id(product_id=product_id,
                                                     headers={"Authorization": f"Bearer {token}"})
    assert get_response.status_code == HTTPStatus.NOT_FOUND, "Продукт все еще существует после удаления."


def test_delete_another_seller_product(api_client, registration_data, token_data, random_category_name,
                                       random_product_data, registration_headers):
    """Тест удаления продукта другого продавца."""
    # 1. Регистрация первого продавца
    registration_response1 = UserApiFunc.register(credential_body=registration_data)
    assert registration_response1.status_code == HTTPStatus.CREATED, "Регистрация первого продавца не удалась."
    seller_id1 = registration_response1.json().get("id")
    # 2. Получение токена для первого продавца
    token_response1 = UserApiFunc.token(
        credential_body=token_data,
        headers=registration_headers
    )
    assert token_response1.status_code == HTTPStatus.OK, "Получение токена для первого продавца не удалось."
    token1 = token_response1.json().get("access_token")
    # 3. Регистрация второго продавца
    registration_data2 = {
        "username": "semplik421",
        "name": "Seller Two",
        "email": "seller244421@example.com",
        "password": "password1123"
    }
    registration_response2 = UserApiFunc.register(credential_body=registration_data2)
    assert registration_response2.status_code == HTTPStatus.CREATED, "Регистрация второго продавца не удалась."
    seller_id2 = registration_response2.json().get("id")
    # 4. Получение токена для второго продавца
    token_response2 = UserApiFunc.token(
        credential_body=registration_data2,
        headers=registration_headers
    )
    assert token_response2.status_code == HTTPStatus.OK, "Получение токена для второго продавца не удалось."
    token2 = token_response2.json().get("access_token")
    # 5. Создание категории с рандомным названием для первого продавца
    category_data = {"name": random_category_name}
    create_category_response = CategoriesApiFunc.create_category(category_data=category_data,
                                                                 headers={"Authorization": f"Bearer {token1}"})
    assert create_category_response.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
    created_category_id = create_category_response.json().get("id")
    # 6. Создание продукта в созданной категории для первого продавца
    random_product_data["category_id"] = created_category_id
    create_product_response = ProductsApiFunc.create_product(product_data=random_product_data,
                                                             headers={"Authorization": f"Bearer {token1}"})
    assert create_product_response.status_code == HTTPStatus.CREATED, "Создание продукта не удалось."
    product_id = create_product_response.json().get("id")
    # 7. Попытка удаления продукта первого продавца вторым продавцом
    delete_response = ProductsApiFunc.delete_product_by_id(product_id=product_id,
                                                           headers={"Authorization": f"Bearer {token2}"})
    assert delete_response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR, "Удаление продукта другого продавца должно было завершиться с ошибкой доступа."