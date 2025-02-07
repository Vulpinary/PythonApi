from enum import Enum
from strenum import StrEnum
from src.config import BASE_URL  # Убедитесь, что эта переменная определена в вашем конфиге

class CategoriesPath(StrEnum):
    """Локальные пути"""
    get = "/categories/"
    get_id = "/categories/{category_id}"
    post = "/categories/"
    put_id = "/categories/{category_id}"
    delete_id = "/categories/{category_id}"

class CategoriesFullPath(Enum):
    """Полные пути"""
    get = BASE_URL + "/" + CategoriesPath.get
    get_id = BASE_URL + "/" + CategoriesPath.get_id
    post = BASE_URL + "/" + CategoriesPath.post
    put_id = BASE_URL + "/" + CategoriesPath.put_id
    delete_id = BASE_URL + "/" + CategoriesPath.delete_id