from http import HTTPStatus

from seller.seller_api_func import UserApiFunc
from suppliers.suppliers_api_func import SuppliersApiFunc



def test_get_suppliers(api_client, registration_data, token_data,
                       random_category_name, registration_headers, db_client_with_supplier):
    """Тест на получение всех поставщиков (GET)"""
    # 1. Регистрация продавца
    registration_response = UserApiFunc.register(credential_body=registration_data)
    assert registration_response.status_code == HTTPStatus.CREATED, "Регистрация продавца не удалась."
    # 2. Получение токена
    token_response = UserApiFunc.token(
        credential_body=token_data,
        headers=registration_headers)
    assert token_response.status_code == HTTPStatus.OK, "Получение токена не удалось."
    token = token_response.json().get("access_token")
    assert token is not None, "Отсутствует токен доступа в ответе."
    # 3. Получение всех поставщиков
    response = SuppliersApiFunc.get(headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == HTTPStatus.OK, "Получение всех поставщиков не удалось."
