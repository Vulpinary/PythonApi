from enum import Enum
from strenum import StrEnum
from src.config import BASE_URL  # Убедитесь, что эта переменная определена в вашем конфиге

class ProductsPath(StrEnum):
    """Локальные пути"""
    get = "/products/"
    get_id = "/products/{product_id}"
    post = "/products/"
    put_id = "/products/{product_id}"
    delete_id = "/products/{product_id}"

class ProductsFullPath(Enum):
    """Полные пути"""
    get = BASE_URL + "/" + ProductsPath.get
    get_id = BASE_URL + "/" + ProductsPath.get_id
    post = BASE_URL + "/" + ProductsPath.post
    put_id = BASE_URL + "/" + ProductsPath.put_id
    delete_id = BASE_URL + "/" + ProductsPath.delete_id