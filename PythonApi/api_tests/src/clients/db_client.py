"""
Клиент для работы с DB Postgres.
"""
import os
import psycopg2
from psycopg2 import DatabaseError, OperationalError

from consts import EnvName, USERS_TABLE_NAME  # Убедитесь, что USERS_TABLE_NAME установлено в "sellers"



class DBClient:
    """Клиент для работы с БД."""

    def __init__(self):
        self.connection = None

    def create_connection(self):
        """Создаем connection к PostgreSQL"""
        db_name = os.getenv(EnvName.DB_NAME, "postgres")
        db_user = os.getenv(EnvName.DB_USER, "postgres")
        db_password = os.getenv(EnvName.DB_PASSWORD, "qwerty12")
        db_host = os.getenv(EnvName.DB_HOST, "localhost")
        db_port = os.getenv(EnvName.DB_PORT, "5432")  # Значение по умолчанию для порта

        print(f"DB Credentials: {db_name}, {db_user}, {db_password}, {db_host}, {db_port}")  # Для отладки

        try:
            self.connection = psycopg2.connect(
                database=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=int(db_port),  # Преобразуем порт в целое число
            )
            self.connection.set_session(readonly=False, autocommit=True)
            print("Connection to PostgreSQL DB successful")
        except OperationalError as e:
            raise DatabaseError("The error on create_connection to PostgreSQL DB") from e

    def close_connection(self):
        """Закрываем подключение к PostgreSQL."""
        try:
            if self.connection:
                self.connection.close()
                print("Close connection to PostgreSQL DB successful")
        except Exception as e:
            raise DatabaseError("The error on close_connection to PostgreSQL DB") from e

    def execute_read_query(self, query):
        """Посылаем SQL запрос и ждем ответ от БД."""
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchall()
                    return result
        except Exception as e:
            raise DatabaseError("The error on execute_read_query to PostgreSQL DB") from e

    def read_row(self, query):
        """Отправляем запрос и получаем 1 строку из результата."""
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
                    result = cursor.fetchone()
                    return result
        except Exception as e:
            raise DatabaseError("The error on execute_read_query to PostgreSQL DB") from e

    def execute_query(self, query):
        """Посылаем SQL запрос и НЕ ждем ответ от БД."""
        try:
            with self.connection:
                with self.connection.cursor() as cursor:
                    cursor.execute(query)
        except Exception as e:
            raise DatabaseError("The error on execute_query to PostgreSQL DB") from e


if __name__ == "__main__":
    # Для теста: подключаемся к БД
    db_client = DBClient()
    db_client.create_connection()

    # Пример простого запроса на выборку пользователей
    select_users_sql = f"SELECT * FROM {USERS_TABLE_NAME};"
    result = db_client.execute_read_query(select_users_sql)
    print(result[:2])  # Печатаем первые две записи

    # Вставляем нового пользователя
    USERS_TABLE_HEADERS = ["id", "username", "password", "name", "email", "is_active"]

    last_id_query = f"SELECT MAX(id) FROM {USERS_TABLE_NAME};"
    last_id_result = db_client.read_row(last_id_query)

    last_id = last_id_result[0] if last_id_result and last_id_result[0] else 0
    user_id = last_id + 1

    insert_user_sql = f"""
    INSERT INTO {USERS_TABLE_NAME} (id, username, password, name, email, is_active) 
    VALUES ({user_id}, 'del@mail.ru', 'del_hash', 'del_fullname', 'test@example.com', true);
    """

    db_client.execute_query(insert_user_sql)

    # Удаляем запись после теста
    delete_user_sql = f"DELETE FROM {USERS_TABLE_NAME} WHERE id={user_id};"
    db_client.execute_query(delete_user_sql)

    db_client.close_connection()
