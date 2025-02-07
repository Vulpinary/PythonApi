import random
from http import HTTPStatus

import pytest

from categories.categories_api_func import CategoriesApiFunc
from products.products_api_func import ProductsApiFunc
from seller.seller_api_func import UserApiFunc
from suppliers.suppliers_api_func import SuppliersApiFunc


# Баг. Создание продукта с пустым именем должно было завершиться с ошибкой
def test_create_product_with_empty_name(api_client, registration_data, token_data, random_category_name,
                                        random_product_data, registration_headers, db_client_with_product):
    """Тест создания продукта с пустым именем."""
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
    # 4. Создание продукта с пустым именем
    product_data = random_product_data.copy()  # Копируем данные продукта
    product_data["name"] = ""  # Устанавливаем пустое имя
    product_data["category_id"] = created_category_id  # Устанавливаем ID категории
    create_product_response = ProductsApiFunc.create_product(product_data=product_data,
                                                             headers={"Authorization": f"Bearer {token}"})
    assert create_product_response.status_code == HTTPStatus.BAD_REQUEST, "Создание продукта с пустым именем должно было завершиться с ошибкой."

# # Баг, после изменения данных продукта, данные не обновляются
def test_update_product(api_client, registration_data, token_data, random_category_name,
                        random_product_data, registration_headers):
    """Тест обновления продукта с использованием токена."""
    # 1. Регистрация продавца
    registration_response = UserApiFunc.register(credential_body=registration_data)
    assert registration_response.status_code == HTTPStatus.CREATED, "Регистрация продавца не удалась."
    seller_id = registration_response.json().get("id")
    # 2. Получение токена
    token_response = UserApiFunc.token(credential_body=token_data, headers=registration_headers)
    assert token_response.status_code == HTTPStatus.OK, "Получение токена не удалось."
    token = token_response.json().get("access_token")
    # 3. Создание категории с рандомным названием
    category_data = {"name": random_category_name}
    create_category_response = CategoriesApiFunc.create_category(category_data=category_data,
    headers = {"Authorization": f"Bearer {token}"})
    assert create_category_response.status_code == HTTPStatus.CREATED, "Создание категории не удалось."
    created_category_id = create_category_response.json().get("id")
    # Заполняем category_id в product_data перед созданием продукта
    random_product_data["category_id"] = created_category_id
    # 4. Создание продукта в созданной категории
    create_product_response = ProductsApiFunc.create_product(product_data=random_product_data,
    headers = {"Authorization": f"Bearer {token}"})
    assert create_product_response.status_code == HTTPStatus.CREATED, "Создание продукта не удалось."
    product_id = create_product_response.json().get("id")
    updated_product_data = {
    "name": "Обновлённый продукт",
    "manufacturer": "Обновлённый производитель",
    "price": round(random.uniform(1, 500), 2),
    "description": "Обновлённое описание",
    "category_id": created_category_id  # Указываем актуальный ID категории
    }
    # Обновление продукта по ID
    update_response = ProductsApiFunc.update_product_by_id(product_id=product_id,
    product_data = updated_product_data,
    headers = {"Authorization": f"Bearer {token}"})
    assert update_response.status_code == HTTPStatus.OK, "Обновление продукта не удалось."
    # 5. Проверка, что данные продукта были обновлены корректно
    updated_product_info = update_response.json()
    assert updated_product_info["name"] == updated_product_data["name"], "Имя продукта не совпадает."
    assert updated_product_info["manufacturer"] == updated_product_data[
    "manufacturer"], "Производитель продукта не совпадает."
    assert float(updated_product_info["price"]) == updated_product_data["price"], "Цена продукта не совпадает."
    assert updated_product_info["description"] == updated_product_data["description"], "Описание продукта не совпадает."

#Баг. Можно поменять поле Usrename
def test_update_seller_username(api_client, registration_data, token_data, registration_headers, db_client):
    """Тест на обновление имени пользователя (должно завершиться с ошибкой)."""
    # 1. Регистрация
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
    # 3. Обновление имени пользователя (должно завершиться с ошибкой)
    new_username = "new_username"
    update_data = {
        "username": new_username,
    }
    update_response = UserApiFunc.put_seller_by_id(seller_id=seller_id, json=update_data,
                                                   headers={"Authorization": f"Bearer {token}"})
    assert update_response.status_code == HTTPStatus.BAD_REQUEST, "Обновление имени пользователя должно было завершиться с ошибкой."



# Определите набор не валидных данных для тестирования
invalid_password_data = [
        {"username": "Polzovatel", "name": "John", "email": "lilitkin@example.com", "password": "short"},
        # Пароль слишком короткий
        {"username": "Seller", "name": "Jane", "email": "seve12@example.com", "password": "onlylowercase"},
        # Пароль без верхнего регистра и цифр
        {"username": "Yser", "name": "Alex", "email": "pochta@example.com", "password": "ONLYUPPERCASE"},
        # Пароль без нижнего регистра и цифр
        {"username": "Resu", "name": "Bob", "email": "granula@example.com", "password": "12345678"},
        # Пароль без букв
        {"username": "Relles", "name": "Alice", "email": "emailik@example.com", "password": "NoDigits"},
        # Пароль без цифр
]
#Баг. Пароль без верхнего регистра и цифр, Пароль без нижнего регистра и цифр, Пароль без букв, Пароль без цифр проходит регистрацию
@pytest.mark.parametrize("invalid_data", invalid_password_data)
def test_seller_register_with_invalid_password(api_client, invalid_data, db_client):
        """Тест регистрации пользователя с не валидным паролем."""
        # 1. Регистрация пользователя
        registration_response = UserApiFunc.register(credential_body=invalid_data)
        assert registration_response.status_code == HTTPStatus.BAD_REQUEST, "Регистрация пользователя не должна пройти."

# Баг. Поле Name поставщика, обязателен к заполнению
def test_create_supplier_with_empty_name(api_client, registration_data, token_data,
                                         random_category_name,
                                         registration_headers, db_client_with_supplier):
    """Тест на создание поставщика с пустым именем."""
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
    # 4. Устанавливаем данные для поставщика с пустым именем
    supplier_data = {
        "name": "",  # Пустое имя
        "email": "supplier@example.com",
        "phone": "+1234567890",
        "address": "123 Supplier St",
        "category_id": created_category_id,
        "seller_id": seller_id
    }
    # 5. Попытка создания поставщика с пустым именем
    create_supplier_response = SuppliersApiFunc.create_supplier(supplier_data=supplier_data,
                                                                headers={"Authorization": f"Bearer {token}"})
    assert create_supplier_response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY, "Создание поставщика с пустым именем должно было завершиться с ошибкой."