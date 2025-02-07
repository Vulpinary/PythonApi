import os
from enum import auto
from strenum import StrEnum

# Константы
"""
Константы
"""

# находим абсолютный путь до корня проекта
curr_dir = os.path.dirname(__file__)
ROOT_PATH = os.path.join(curr_dir, '..')

ENV_FOLDER = "env_folder"
TEST_FOLDER = "tests"

# Имя таблицы продавцов
USERS_TABLE_NAME = "sellers"  # Имя таблицы с данными продавцов

# Заголовки для таблицы продавцов
USERS_TABLE_HEADERS = [
    "username", "hashed_password", "name",
    "email"
]


def get_env_file_path(env_name):
    return os.path.join(ROOT_PATH, ENV_FOLDER, env_name, ".env")


class EnvName(StrEnum):
    """Названия ENV переменных в файле .env"""

    # DB
    DB_NAME = auto()
    DB_USER = auto()
    DB_PASSWORD = auto()
    DB_HOST = auto()
    DB_PORT = auto()


# Если нужно протестировать функции
if __name__ == "__main__":
    print(get_env_file_path("test"))