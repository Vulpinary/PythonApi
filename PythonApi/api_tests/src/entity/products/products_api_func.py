from api_client import APIClient
from products.products_paths import ProductsFullPath


class ProductsApiFunc:
    @staticmethod
    def get(**kwargs):
        """Получаем все продукты."""
        return APIClient.get(url=ProductsFullPath.get.value, **kwargs)

    @staticmethod
    def get_product_by_id(product_id: int, **kwargs):
        """Получаем продукт по ID."""
        return APIClient.get(url=ProductsFullPath.get_id.value.format(product_id=product_id), **kwargs)

    @staticmethod
    def create_product(product_data: dict, **kwargs):
        """Создаем новый продукт."""
        return APIClient.post(url=ProductsFullPath.post.value, json=product_data, **kwargs)

    @staticmethod
    def update_product_by_id(product_id: int, product_data: dict, **kwargs):
        """Обновляем продукт по ID."""
        return APIClient.put(url=ProductsFullPath.put_id.value.format(product_id=product_id), json=product_data, **kwargs)

    @staticmethod
    def delete_product_by_id(product_id: int, **kwargs):
        """Удаляем продукт по ID."""
        return APIClient.delete(url=ProductsFullPath.delete_id.value.format(product_id=product_id), **kwargs)