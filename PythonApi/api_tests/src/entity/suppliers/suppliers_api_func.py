from api_client import APIClient
from suppliers.suppliers_paths import SuppliersFullPath


class SuppliersApiFunc:
    @staticmethod
    def get(**kwargs):
        """Получаем всех поставщиков."""
        return APIClient.get(url=SuppliersFullPath.get.value, **kwargs)

    @staticmethod
    def get_supplier_by_id(supplier_id: int, **kwargs):
        """Получаем поставщика по ID."""
        return APIClient.get(url=SuppliersFullPath.get_id.value.format(supplier_id=supplier_id), **kwargs)

    @staticmethod
    def create_supplier(supplier_data: dict, **kwargs):
        """Создаем нового поставщика."""
        return APIClient.post(url=SuppliersFullPath.post.value, json=supplier_data, **kwargs)

    @staticmethod
    def update_supplier_by_id(supplier_id: int, supplier_data: dict, **kwargs):
        """Обновляем поставщика по ID."""
        return APIClient.put(url=SuppliersFullPath.put_id.value.format(supplier_id=supplier_id), json=supplier_data, **kwargs)

    @staticmethod
    def delete_supplier_by_id(supplier_id: int, **kwargs):
        """Удаляем поставщика по ID."""
        return APIClient.delete(url=SuppliersFullPath.delete_id.value.format(supplier_id=supplier_id), **kwargs)