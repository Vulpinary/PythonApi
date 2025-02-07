from enum import Enum
from strenum import StrEnum
from src.config import BASE_URL  # Убедитесь, что эта переменная определена в вашем конфиге

class SellerPath(StrEnum):
    """Локальные пути"""
    register = "sellers/register"
    token = "/token"
    get = "/sellers/"
    get_id = "/sellers/{seller_id}"
    put_id = "/sellers/{seller_id}"
    delete_id = "/sellers/{seller_id}"

class SellerFullPath(Enum):
    """Полные пути"""
    register = BASE_URL + "/" + SellerPath.register  # Используйте + для конкатенации строк
    token = BASE_URL + "/" + SellerPath.token
    get = BASE_URL + "/" + SellerPath.get
    get_id = BASE_URL + "/" + SellerPath.get_id
    put_id = BASE_URL + "/" + SellerPath.put_id
    delete_id = BASE_URL + "/" + SellerPath.delete_id