import pytest
from http import HTTPStatus
from seller.seller_api_func import UserApiFunc

def test_seller_register(api_client, registration_data, db_client):
        """Тест регистрации пользователя с рандомными данными."""
        response = UserApiFunc.register(credential_body=registration_data)
        assert response.status_code == HTTPStatus.CREATED, "Регистрация пользователя не удалась."
        response_data = response.json()

        # Проверка структуры и содержимого ответа
        assert response_data['username'] == registration_data['username'], "Имя пользователя не совпадает."
        assert response_data['name'] == registration_data['name'], "Имя не совпадает."
        assert response_data['email'] == registration_data['email'], "Email не совпадает."
        assert response_data['is_active'] is True, "Статус активности неверен."


# Определите набор валидных данных для тестирования
valid_registration_data = [
        {"username": "Mory011", "name": "Garryy 3Moll", "email": "us1er011@example.com", "password": "Password123"},
        {"username": "Polly011", "name": "Jone T3omb", "email": "use1r012@example.com", "password": "Password123"},
        {"username": "Plinka011", "name": "Alexin3ka", "email": "use1r013@example.com", "password": "password123"},
        {"username": "Lolilop101", "name": "Petro3vin Koner", "email": "us1er014@example.com", "password": "password123"},
        {"username": "Petrin011", "name": "Alice Br3own", "email": "user1015@example.com", "password": "password123"},
]
@pytest.mark.parametrize("valid_data", valid_registration_data)
def test_seller_register_with_valid_data(api_client, valid_data, db_client):
        """Тест регистрации пользователя с валидными данными."""
        # 1. Регистрация пользователя
        registration_response = UserApiFunc.register(credential_body=valid_data)
        assert registration_response.status_code == HTTPStatus.CREATED, "Регистрация пользователя не удалась."
        # 2. Проверка структуры и содержимого ответа
        response_data = registration_response.json()
        assert isinstance(response_data, dict), "Ответ должен быть словарем."
        # Проверка наличия и соответствия значений полей
        assert response_data.get('username') == valid_data['username'], "Имя пользователя не совпадает."
        assert response_data.get('name') == valid_data['name'], "Имя не совпадает."
        assert response_data.get('email') == valid_data['email'], "Email не совпадает."
        assert response_data.get('is_active') is True, "Статус активности неверен."


# # Определите набор не валидных данных для тестирования
# invalid_password_data = [
#         {"username": "Polzovatel", "name": "John", "email": "lilitkin@example.com", "password": "short"},
#         # Пароль слишком короткий
#         {"username": "Seller", "name": "Jane", "email": "seve12@example.com", "password": "onlylowercase"},
#         # Пароль без верхнего регистра и цифр
#         {"username": "Yser", "name": "Alex", "email": "pochta@example.com", "password": "ONLYUPPERCASE"},
#         # Пароль без нижнего регистра и цифр
#         {"username": "Resu", "name": "Bob", "email": "granula@example.com", "password": "12345678"},
#         # Пароль без букв
#         {"username": "Relles", "name": "Alice", "email": "emailik@example.com", "password": "NoDigits"},
#         # Пароль без цифр
# ]
# #Баг. Пароль без верхнего регистра и цифр, Пароль без нижнего регистра и цифр, Пароль без букв, Пароль без цифр проходит регистрацию
# @pytest.mark.parametrize("invalid_data", invalid_password_data)
# def test_seller_register_with_invalid_password(api_client, invalid_data, db_client):
#         """Тест регистрации пользователя с не валидным паролем."""
#         # 1. Регистрация пользователя
#         registration_response = UserApiFunc.register(credential_body=invalid_data)
#         assert registration_response.status_code == HTTPStatus.BAD_REQUEST, "Регистрация пользователя не должна пройти."