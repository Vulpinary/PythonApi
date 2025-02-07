from http import HTTPStatus

from products.products_api_func import ProductsApiFunc
from seller.seller_api_func import UserApiFunc


def test_get_products(api_client, registration_data, token_data, random_category_name,
                        random_product_data, registration_headers):
    """Тест получения продуктов с использованием токена."""

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

    # 3. Получение всех продуктов
    response = ProductsApiFunc.get(headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == HTTPStatus.OK, "Получение всех продуктов не удалось."

    # 4. Проверка структуры ответа
    products_data = response.json()
    assert isinstance(products_data, list), "Ответ должен быть списком."
