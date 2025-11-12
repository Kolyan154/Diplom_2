import pytest
import allure
import random
from helpers.api_client import UserAPI
from data.test_data import UserData
from data.expected_responses import AuthResponses, CommonResponses


@allure.feature("Создание пользователя")
class TestCreateUser:
    
    @allure.title("Создание уникального пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_unique_user_success(self, random_user_data, user_api):
        """Тест успешного создания уникального пользователя"""
        with allure.step("Создать нового пользователя"):
            response = user_api.create_user(**random_user_data)
        
        with allure.step("Проверить статус код ответа"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        with allure.step("Проверить структуру ответа"):
            response_data = response.json()
            assert response_data["success"] == True, "Флаг success должен быть True"
            assert "accessToken" in response_data, "В ответе должен быть accessToken"
            assert "refreshToken" in response_data, "В ответе должен быть refreshToken"
        
        with allure.step("Проверить данные пользователя в ответе"):
            user_in_response = response_data["user"]
            assert user_in_response["email"] == random_user_data["email"]
            assert user_in_response["name"] == random_user_data["name"]
    
    @allure.title("Создание пользователя, который уже зарегистрирован")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_existing_user_fail(self, user_api):
        """Тест попытки создания уже существующего пользователя"""
        # Сначала создаем пользователя
        user_data = {
            "email": f"existing_{random.randint(100000, 999999)}@example.com",
            "password": "test_password_123", 
            "name": "Existing User"
        }
        
        with allure.step("Создать первоначального пользователя"):
            create_response = user_api.create_user(**user_data)
            assert create_response.status_code == 200
        
        with allure.step("Попытаться создать пользователя с существующими данными"):
            response = user_api.create_user(**user_data)
        
        with allure.step("Проверить статус код 403"):
            assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
        
        with allure.step("Проверить сообщение об ошибке"):
            response_data = response.json()
            assert response_data["success"] == False, "Флаг success должен быть False"
            assert "already exists" in response_data["message"].lower()
    
    @allure.title("Создание пользователя с пустым email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_empty_email_fail(self, user_api):
        """Тест создания пользователя с пустым email"""
        response = user_api.create_user(
            email="",
            password="test_password_123",
            name="Test User"
        )
        
        assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
        response_data = response.json()
        assert response_data["success"] == False, "Флаг success должен быть False"
    
    @allure.title("Создание пользователя с пустым паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_empty_password_fail(self, user_api):
        """Тест создания пользователя с пустым паролем"""
        response = user_api.create_user(
            email="test@example.com",
            password="",
            name="Test User"
        )
        
        assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
        response_data = response.json()
        assert response_data["success"] == False, "Флаг success должен быть False"
    
    @allure.title("Создание пользователя с пустым именем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_user_empty_name_fail(self, user_api):
        """Тест создания пользователя с пустым именем"""
        response = user_api.create_user(
            email="test@example.com",
            password="test_password_123",
            name=""
        )
        
        assert response.status_code == 403, f"Ожидался статус 403, получен {response.status_code}"
        response_data = response.json()
        assert response_data["success"] == False, "Флаг success должен быть False"