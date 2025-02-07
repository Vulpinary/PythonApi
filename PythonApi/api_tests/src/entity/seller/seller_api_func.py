from src.clients.api_client import APIClient
from seller.seller_paths import SellerFullPath

class UserApiFunc:
    @staticmethod
    def register(credential_body: dict, **kwargs):
        """Регистрируем Sellers."""
        return APIClient.post(url=SellerFullPath.register.value, json=credential_body, **kwargs)

    @staticmethod
    def token(credential_body: dict, **kwargs):
        """Аутентифицирует продавца и возвращает токен доступа."""
        return APIClient.post(url=SellerFullPath.token.value, data=credential_body, **kwargs)

    @staticmethod
    def get(**kwargs):
        """Получаем текущего seller."""
        return APIClient.get(url=SellerFullPath.get, **kwargs)

    @staticmethod
    def get_seller_by_id(seller_id: int, **kwargs):  # Corrected - seller_id is now the name of the argument
        """Получаем продавца по ID."""
        return APIClient.get(url=SellerFullPath.get_id.value.format(seller_id=seller_id), **kwargs)  # Use format

    @staticmethod
    def put_seller_by_id (seller_id: int, **kwargs):
        """Обновляем продавца по ID."""
        return APIClient.put(url=SellerFullPath.get_id.value.format(seller_id=seller_id), **kwargs)

    @staticmethod
    def delete_seller_by_id(seller_id: int, **kwargs):
        """Deletes a seller by ID."""
        return APIClient.delete(url=SellerFullPath.delete_id.value.format(seller_id=seller_id), **kwargs)