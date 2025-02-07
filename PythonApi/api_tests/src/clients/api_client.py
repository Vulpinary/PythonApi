import requests

from src.clients.requests_kwargs_func import convert_url_to_str, separate_kwargs


import requests

class APIClient:
    """Класс-обертка для requests"""

    @staticmethod
    def post(**kwargs):
        """Отправляем POST запрос"""
        request_kwargs, other_kwargs = APIClient._preprocess_kwargs(kwargs)
        response = requests.post(**request_kwargs)
        return response

    @staticmethod
    def _preprocess_kwargs(kwargs):
        """Предобрабатываем kwargs для request-а"""
        # Здесь вы можете добавить логику для обработки URL и других параметров
        return kwargs, {}

    @staticmethod
    def put(**kwargs):
        """Отправляем PUT запрос"""
        request_kwargs, other_kwargs = APIClient._preprocess_kwargs(kwargs)
        response = requests.put(**request_kwargs)
        return response

    @staticmethod
    def get(**kwargs):
        """Отправляем GET запрос"""
        request_kwargs, other_kwargs = APIClient._preprocess_kwargs(kwargs)
        response = requests.get(**request_kwargs)
        return response

    @staticmethod
    def delete(**kwargs):
        """Отправляем DELETE запрос"""
        request_kwargs, other_kwargs = APIClient._preprocess_kwargs(kwargs)
        response = requests.delete(**request_kwargs)
        return response

    @staticmethod
    def patch(**kwargs):
        """Отправляем PATCH запрос"""
        request_kwargs, other_kwargs = APIClient._preprocess_kwargs(kwargs)
        response = requests.patch(**request_kwargs)
        return response

    @staticmethod
    def _preprocess_kwargs(kwargs):
        """Предобрабатываем kwargs для request-а"""
        convert_url_to_str(kwargs)
        return separate_kwargs(kwargs)