import requests
import allure
import json
from config.urls import URLs
from data.expected_responses import CommonResponses


class StellarBurgersAPI:
    """Базовый класс для работы с API Stellar Burgers"""
    
    def __init__(self):
        self.base_url = URLs.BASE_URL
    
    @allure.step("POST запрос к {endpoint}")
    def post(self, endpoint, data=None, headers=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.post(url, json=data, headers=headers, timeout=10)
            self._attach_request_response_data("POST", url, data, headers, response)
            return response
        except requests.exceptions.ConnectionError as e:
            allure.attach(f"Connection error: {str(e)}", "Connection Error", allure.attachment_type.TEXT)
            # Используем текст из дата-модуля
            return MockResponse(503, {"success": False, "message": CommonResponses.CONNECTION_FAILED})
        except requests.exceptions.Timeout as e:
            allure.attach(f"Timeout error: {str(e)}", "Timeout Error", allure.attachment_type.TEXT)
            # Используем текст из дата-модуля
            return MockResponse(408, {"success": False, "message": CommonResponses.REQUEST_TIMEOUT})
    
    @allure.step("DELETE запрос к {endpoint}")
    def delete(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.delete(url, headers=headers, timeout=10)
            self._attach_request_response_data("DELETE", url, None, headers, response)
            return response
        except requests.exceptions.ConnectionError as e:
            allure.attach(f"Connection error: {str(e)}", "Connection Error", allure.attachment_type.TEXT)
            return MockResponse(503, {"success": False, "message": CommonResponses.CONNECTION_FAILED})
    
    @allure.step("GET запрос к {endpoint}")
    def get(self, endpoint, headers=None):
        url = f"{self.base_url}{endpoint}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            self._attach_request_response_data("GET", url, None, headers, response)
            return response
        except requests.exceptions.ConnectionError as e:
            allure.attach(f"Connection error: {str(e)}", "Connection Error", allure.attachment_type.TEXT)
            return MockResponse(503, {"success": False, "message": CommonResponses.CONNECTION_FAILED})
    
    def _attach_request_response_data(self, method, url, data, headers, response):
        """Прикрепление данных запроса и ответа к Allure отчету"""
        request_info = f"Method: {method}\nURL: {url}\nHeaders: {headers}"
        allure.attach(request_info, "Request Info", allure.attachment_type.TEXT)
        
        if data:
            formatted_data = json.dumps(data, indent=2, ensure_ascii=False)
            allure.attach(formatted_data, "Request Data", allure.attachment_type.JSON)
        
        response_info = f"Status Code: {response.status_code}\nContent-Type: {response.headers.get('content-type', 'unknown')}"
        allure.attach(response_info, "Response Info", allure.attachment_type.TEXT)
        
        try:
            if hasattr(response, 'json'):
                formatted_json = json.dumps(response.json(), indent=2, ensure_ascii=False)
                allure.attach(formatted_json, "Response Body", allure.attachment_type.JSON)
        except:
            # Если ответ не JSON, прикрепляем как текст
            response_text = response.text if hasattr(response, 'text') else str(response)
            allure.attach(response_text[:1000], "Response Body (text)", allure.attachment_type.TEXT)


class MockResponse:
    """Mock response для случаев когда API недоступно"""
    def __init__(self, status_code, json_data):
        self.status_code = status_code
        self._json_data = json_data
        self.text = json.dumps(json_data)
        self.headers = {'content-type': 'application/json'}
    
    def json(self):
        return self._json_data


class UserAPI(StellarBurgersAPI):
    """Класс для работы с эндпоинтами пользователя"""
    
    @allure.step("Создание пользователя с email: {email}")
    def create_user(self, email, password, name):
        data = {
            "email": email,
            "password": password,
            "name": name
        }
        return self.post(URLs.REGISTER, data)
    
    @allure.step("Логин пользователя с email: {email}")
    def login_user(self, email, password):
        data = {
            "email": email,
            "password": password
        }
        return self.post(URLs.LOGIN, data)
    
    @allure.step("Удаление пользователя")
    def delete_user(self, token):
        headers = {"Authorization": token}
        return self.delete(URLs.USER, headers=headers)


class OrderAPI(StellarBurgersAPI):
    """Класс для работы с эндпоинтами заказов"""
    
    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        return self.get(URLs.INGREDIENTS)
    
    @allure.step("Создание заказа")
    def create_order(self, ingredients, token=None):
        data = {"ingredients": ingredients}
        headers = {"Authorization": token} if token else None
        allure.dynamic.description(f"Создание заказа с {len(ingredients)} ингредиентами")
        return self.post(URLs.ORDERS, data, headers)
    
    @allure.step("Получение свежих ингредиентов")
    def get_fresh_ingredients(self, count=3):
        """Получение указанного количества свежих ингредиентов"""
        response = self.get_ingredients()
        ingredients_data = response.json()
        return [ingredient["_id"] for ingredient in ingredients_data["data"][:count]]