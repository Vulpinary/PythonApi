import random

import pytest
from faker import Faker
import string

from src.clients.api_client import APIClient
from src.clients.db_client import DBClient

fake = Faker('ru_RU')

@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8000"

@pytest.fixture(scope="module")
def api_client():
    return APIClient()

@pytest.fixture()
def password():
    """Рандомный пароль длиной от 4 до 16 символов."""
    return fake.password(length=10)

@pytest.fixture()
def username():
    """Рандомное username"""
    return fake.user_name()


@pytest.fixture()
def registration_data():
    """Генерирует случайные данные для регистрации."""
    return {
        'username': fake.user_name(),
        'password': fake.password(length=10),
        'name': fake.name(),
        'email': fake.email()
    }

@pytest.fixture()
def token_data(registration_data):
    """Данные для создания токена авторизации."""
    return {
        "username": registration_data["username"],
        "password": registration_data["password"]
    }

@pytest.fixture()
def registration_headers():
    """Хэдеры запроса POST /seller/register."""
    return {
        'Authorization': 'Bearer null',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

@pytest.fixture()
def random_product_data(random_product_name, random_manufacturer, random_description):
    """Генерирует случайные данные для продукта."""
    return {
        "name": random_product_name,
        "manufacturer": random_manufacturer,
        "price": round(random.uniform(1, 500), 2),  # Генерируем случайную цену от 1 до 500
        "description": random_description,
        "category_id": None  # Это поле будет заполнено позже в тесте
    }
@pytest.fixture()
def random_category_name():
    """Генерирует случайное название категории."""
    length = random.randint(5, 15)  # Генерируем длину названия от 5 до 15 символов
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@pytest.fixture()
def random_product_name():
    """Генерирует случайное название продукта."""
    length = random.randint(5, 15)  # Генерируем длину названия от 5 до 15 символов
    return ''.join(random.choices(string.ascii_letters + ' ', k=length)).strip()

@pytest.fixture()
def random_manufacturer():
    """Генерирует случайное имя производителя."""
    length = random.randint(5, 15)  # Генерируем длину имени производителя от 5 до 15 символов
    return ''.join(random.choices(string.ascii_letters + ' ', k=length)).strip()

@pytest.fixture()
def random_description():
    """Генерирует случайное описание продукта."""
    length = random.randint(10, 30)  # Генерируем длину описания от 10 до 30 символов
    return ''.join(random.choices(string.ascii_letters + string.digits + ' ', k=length)).strip()

@pytest.fixture()
def random_supplier_data():
    """Генерирует случайные данные для поставщика."""
    return {
        "name": ''.join(random.choices(string.ascii_letters + ' ', k=random.randint(5, 15))).strip(),
        "email": f"{''.join(random.choices(string.ascii_letters, k=5))}@example.com",
        "phone": f"+{random.randint(1000000000, 9999999999)}",  # Генерация случайного номера телефона
        "address": ''.join(random.choices(string.ascii_letters + ' ', k=random.randint(10, 30))).strip(),
    }


@pytest.fixture()
def db_client(registration_data):
    """Фикстура для работы с базой данных."""

    db_client = DBClient()
    db_client.create_connection()  # Создаем соединение с БД

    yield db_client  # Возвращаем клиент для использования в тестах

    # Удаляем пользователя из базы данных после теста
    if registration_data:
        delete_user_sql = f"DELETE FROM sellers WHERE username='{registration_data['username']}';"
        db_client.execute_query(delete_user_sql)
        print(f"Deleted user with username {registration_data['username']} from database.")

    # Закрываем соединение после теста
    db_client.close_connection()



@pytest.fixture()
def db_client_with_category(registration_data):
    """Фикстура для работы с базой данных: сначала удаляет категории, затем продавцов."""

    db_client = DBClient()
    db_client.create_connection()  # Создаем соединение с БД

    yield db_client  # Возвращаем клиент для использования в тестах

    # Удаляем категорию из базы данных после теста
    if registration_data:
        delete_category_sql = f"DELETE FROM categories WHERE seller_id=(SELECT id FROM sellers WHERE username='{registration_data['username']}');"
        db_client.execute_query(delete_category_sql)
        print(f"Deleted category for user {registration_data['username']} from database.")

    # Удаляем пользователя из базы данных после теста
    if registration_data:
        delete_user_sql = f"DELETE FROM sellers WHERE username='{registration_data['username']}';"
        db_client.execute_query(delete_user_sql)
        print(f"Deleted user with username {registration_data['username']} from database.")

    # Закрываем соединение после теста
    db_client.close_connection()


@pytest.fixture()
def db_client_with_product(registration_data):
    """Фикстура для работы с базой данных: сначала удаляет продукт, затем продавца."""

    db_client = DBClient()
    db_client.create_connection()  # Создаем соединение с БД

    yield db_client  # Возвращаем клиент для использования в тестах

    # Удаляем продукт из базы данных после теста
    if registration_data:
        delete_product_sql = f"""
        DELETE FROM products 
        WHERE category_id IN (
            SELECT id FROM categories 
            WHERE seller_id=(SELECT id FROM sellers WHERE username='{registration_data['username']}')
        );
        """
        db_client.execute_query(delete_product_sql)
        print(f"Deleted product(s) for user {registration_data['username']} from database.")

        # Удаляем категорию из базы данных после теста
        if registration_data:
            delete_category_sql = f"DELETE FROM categories WHERE seller_id=(SELECT id FROM sellers WHERE username='{registration_data['username']}');"
            db_client.execute_query(delete_category_sql)
            print(f"Deleted category for user {registration_data['username']} from database.")

        # Удаляем пользователя из базы данных после теста
        if registration_data:
            delete_user_sql = f"DELETE FROM sellers WHERE username='{registration_data['username']}';"
            db_client.execute_query(delete_user_sql)
            print(f"Deleted user with username {registration_data['username']} from database.")

        # Закрываем соединение после теста
        db_client.close_connection()


@pytest.fixture()
def db_client_with_supplier(registration_data):
    """Фикстура для работы с базой данных: удаляет поставщика и продавца после теста."""

    db_client = DBClient()
    db_client.create_connection()  # Создаем соединение с БД

    yield db_client  # Возвращаем клиент для использования в тестах

    # Удаляем продукт из базы данных после теста
    if registration_data:
        delete_product_sql = f"""
        DELETE FROM products 
        WHERE category_id IN (
            SELECT id FROM categories 
            WHERE seller_id=(SELECT id FROM sellers WHERE username='{registration_data['username']}')
        );
        """


    # Удаляем поставщика из базы данных после теста
    if registration_data:
        # Удаляем поставщика по ID продавца
        delete_supplier_sql = f"""
        DELETE FROM suppliers 
        WHERE seller_id=(SELECT id FROM sellers WHERE username='{registration_data['username']}');
        """
        db_client.execute_query(delete_supplier_sql)
        print(f"Deleted supplier for user {registration_data['username']} from database.")

    db_client.execute_query(delete_product_sql)
    print(f"Deleted product(s) for user {registration_data['username']} from database.")

    # Удаляем категорию из базы данных после теста
    if registration_data:
        delete_category_sql = f"DELETE FROM categories WHERE seller_id=(SELECT id FROM sellers WHERE username='{registration_data['username']}');"
        db_client.execute_query(delete_category_sql)
        print(f"Deleted category for user {registration_data['username']} from database.")

    # Удаляем пользователя из базы данных после теста
    if registration_data:
        delete_user_sql = f"DELETE FROM sellers WHERE username='{registration_data['username']}';"
        db_client.execute_query(delete_user_sql)
        print(f"Deleted user with username {registration_data['username']} from database.")

    # Закрываем соединение после теста
    db_client.close_connection()
