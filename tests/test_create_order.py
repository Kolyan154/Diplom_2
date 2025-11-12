import pytest
import allure
from helpers.api_client import OrderAPI
from data.test_data import OrderData
from data.expected_responses import OrderResponses, CommonResponses


@allure.feature("Создание заказа")
class TestCreateOrder:
    
    @allure.title("Создание заказа с авторизацией")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_auth_success(self, valid_ingredients, authenticated_user):
        """Тест успешного создания заказа с авторизацией"""
        order_api = OrderAPI()
        
        with allure.step("Создать заказ с авторизацией"):
            response = order_api.create_order(
                ingredients=valid_ingredients,
                token=authenticated_user["token"]
            )
        
        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        with allure.step("Проверить успешность создания заказа"):
            response_data = response.json()
            assert response_data["success"] == True, "Флаг success должен быть True"
            assert "order" in response_data, "В ответе должен быть объект order"
            assert "number" in response_data["order"], "В заказе должен быть номер"
    
    @allure.title("Создание заказа без авторизации")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_auth_success(self, valid_ingredients):
        """Тест создания заказа без авторизации"""
        order_api = OrderAPI()
        
        with allure.step("Создать заказ без авторизации"):
            response = order_api.create_order(ingredients=valid_ingredients)
        
        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        with allure.step("Проверить успешность создания заказа"):
            response_data = response.json()
            assert response_data["success"] == True, "Флаг success должен быть True"
            assert "order" in response_data, "В ответе должен быть объект order"
            assert "number" in response_data["order"], "В заказе должен быть номер"
    
    @allure.title("Создание заказа с ингредиентами и проверка структуры ответа")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_order_with_ingredients_structure(self, valid_ingredients, authenticated_user):
        """Тест создания заказа с проверкой структуры ответа"""
        order_api = OrderAPI()
        
        with allure.step("Создать заказ с ингредиентами"):
            response = order_api.create_order(
                ingredients=valid_ingredients,
                token=authenticated_user["token"]
            )
        
        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        with allure.step("Проверить успешность создания"):
            response_data = response.json()
            assert response_data["success"] == True, "Флаг success должен быть True"
            assert "order" in response_data, "В ответе должен быть объект order"
    
    @allure.title("Создание заказа с ингредиентами и проверка наличия ingredients в ответе")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_ingredients_in_response(self, valid_ingredients, authenticated_user):
        """Тест создания заказа с проверкой наличия ingredients в ответе"""
        order_api = OrderAPI()
        
        with allure.step("Создать заказ с ингредиентами"):
            response = order_api.create_order(
                ingredients=valid_ingredients,
                token=authenticated_user["token"]
            )
        
        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        with allure.step("Проверить наличие ingredients в ответе"):
            response_data = response.json()
            assert "order" in response_data, "В ответе должен быть объект order"
            # Проверяем что ingredients присутствует в ответе (без условия if)
            assert "ingredients" in response_data["order"], "В заказе должен быть список ingredients"
    
    @allure.title("Создание заказа без ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_without_ingredients_fail(self, authenticated_user):
        """Тест создания заказа без ингредиентов"""
        order_api = OrderAPI()
        
        with allure.step("Создать заказ без ингредиентов"):
            response = order_api.create_order(
                ingredients=OrderData.EMPTY_INGREDIENTS,
                token=authenticated_user["token"]
            )
        
        with allure.step("Проверить статус код 400"):
            assert response.status_code == 400, f"Ожидался статус 400, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке отсутствия ингредиентов"):
            response_data = response.json()
            assert response_data["success"] == False, "Флаг success должен быть False"
    
    @allure.title("Создание заказа с неверным хешем ингредиентов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_invalid_ingredients_hash_fail(self, authenticated_user):
        """Тест создания заказа с неверным хешем ингредиентов"""
        order_api = OrderAPI()
        
        with allure.step("Создать заказ с невалидными ингредиентами"):
            response = order_api.create_order(
                ingredients=OrderData.INVALID_INGREDIENTS,
                token=authenticated_user["token"]
            )
        
        with allure.step("Проверить статус код 500"):
            assert response.status_code == 500, f"Ожидался статус 500, получен {response.status_code}"
        
        with allure.step("Проверить HTML ответ с ошибкой"):
            content_type = response.headers.get('content-type', '')
            assert 'text/html' in content_type, "Ответ должен быть в формате HTML"
            assert CommonResponses.INTERNAL_SERVER_ERROR in response.text, "В ответе должна быть ошибка сервера"
    
    @allure.title("Создание заказа с получением ингредиентов в реальном времени")
    @allure.severity(allure.severity_level.NORMAL)
    def test_create_order_with_fresh_ingredients(self, authenticated_user):
        """Тест создания заказа с ингредиентами, полученными непосредственно перед созданием"""
        order_api = OrderAPI()
        
        with allure.step("Получить актуальные ингредиенты"):
            fresh_ingredients = order_api.get_fresh_ingredients(count=3)
        
        with allure.step("Создать заказ со свежими ингредиентами"):
            response = order_api.create_order(
                ingredients=fresh_ingredients,
                token=authenticated_user["token"]
            )
        
        with allure.step("Проверить успешность создания заказа"):
            assert response.status_code == 200
            response_data = response.json()
            assert response_data["success"] == True, "Флаг success должен быть True"