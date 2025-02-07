from api_client import APIClient
from categories.categories_paths import CategoriesFullPath


class CategoriesApiFunc:
    @staticmethod
    def get(**kwargs):
        """Получаем все категории."""
        return APIClient.get(url=CategoriesFullPath.get.value, **kwargs)

    @staticmethod
    def get_category_by_id(category_id: int, **kwargs):
        """Получаем категорию по ID."""
        return APIClient.get(url=CategoriesFullPath.get_id.value.format(category_id=category_id), **kwargs)

    @staticmethod
    def create_category(category_data: dict, **kwargs):
        """Создаем новую категорию."""
        return APIClient.post(url=CategoriesFullPath.post.value, json=category_data, **kwargs)

    @staticmethod
    def update_category_by_id(category_id: int, category_data: dict, **kwargs):
        """Обновляем категорию по ID."""
        return APIClient.put(url=CategoriesFullPath.put_id.value.format(category_id=category_id), json=category_data, **kwargs)

    @staticmethod
    def delete_category_by_id(category_id: int, **kwargs):
        """Удаляем категорию по ID."""
        return APIClient.delete(url=CategoriesFullPath.delete_id.value.format(category_id=category_id), **kwargs)