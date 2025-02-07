from enum import Enum
from strenum import StrEnum
from src.config import BASE_URL  # Убедитесь, что эта переменная определена в вашем конфиге

class SuppliersPath(StrEnum):
    """Локальные пути"""
    get = "/suppliers/"
    get_id = "/suppliers/{supplier_id}"
    post = "/suppliers/"
    put_id = "/suppliers/{supplier_id}"
    delete_id = "/suppliers/{supplier_id}"

class SuppliersFullPath(Enum):
    """Полные пути"""
    get = BASE_URL + "/" + SuppliersPath.get
    get_id = BASE_URL + "/" + SuppliersPath.get_id
    post = BASE_URL + "/" + SuppliersPath.post
    put_id = BASE_URL + "/" + SuppliersPath.put_id
    delete_id = BASE_URL + "/" + SuppliersPath.delete_id