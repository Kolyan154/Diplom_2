import pytest
import allure
import random
from helpers.api_client import UserAPI
from data.test_data import UserData
from data.expected_responses import AuthResponses, CommonResponses


@allure.feature("Логин пользователя")
class TestLoginUser:
    
    @allure.title("Успешный вход под существующим пользователем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_existing_user_success(self, user_api):
        """Тест успешного входа под существующим пользователем"""
        # Сначала создаем пользователя
        user_data = {
            "email": f"login_test_{random.randint(100000, 999999)}@example.com",
            "password": "test_password_123",
            "name": "Login Test User"
        }
        
        with allure.step("Создать тестового пользователя"):
            create_response = user_api.create_user(**user_data)
            assert create_response.status_code == 200
        
        with allure.step("Выполнить логин с корректными данными"):
            response = user_api.login_user(user_data["email"], user_data["password"])
        
        with allure.step("Проверить статус код 200"):
            assert response.status_code == 200, f"Ожидался статус 200, получен {response.status_code}"
        
        with allure.step("Проверить успешность операции"):
            response_data = response.json()
            assert response_data["success"] == True, "Флаг success должен быть True"
            assert "accessToken" in response_data, "В ответе должен быть accessToken"
        
        with allure.step("Проверить данные пользователя в ответе"):
            assert response_data["user"]["email"] == user_data["email"]
            assert response_data["user"]["name"] == user_data["name"]
    
    @allure.title("Вход с неверным email")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_email_fail(self, user_api):
        """Тест входа с неверным email"""
        # Сначала создаем пользователя
        user_data = {
            "email": f"wrong_email_test_{random.randint(100000, 999999)}@example.com",
            "password": "correct_password_123",
            "name": "Wrong Email Test User"
        }
        
        with allure.step("Создать тестового пользователя"):
            create_response = user_api.create_user(**user_data)
            assert create_response.status_code == 200
        
        response = user_api.login_user("wrong@example.com", user_data["password"])
        
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
        response_data = response.json()
        assert response_data["success"] == False, "Флаг success должен быть False"
        assert AuthResponses.EMAIL_PASSWORD_INCORRECT in response_data["message"].lower()
    
    @allure.title("Вход с неверным паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_password_fail(self, user_api):
        """Тест входа с неверным паролем"""
        # Сначала создаем пользователя
        user_data = {
            "email": f"wrong_password_test_{random.randint(100000, 999999)}@example.com",
            "password": "correct_password_123",
            "name": "Wrong Password Test User"
        }
        
        with allure.step("Создать тестового пользователя"):
            create_response = user_api.create_user(**user_data)
            assert create_response.status_code == 200
        
        response = user_api.login_user(user_data["email"], "wrong_password")
        
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
        response_data = response.json()
        assert response_data["success"] == False, "Флаг success должен быть False"
        assert AuthResponses.EMAIL_PASSWORD_INCORRECT in response_data["message"].lower()
    
    @allure.title("Вход с неверным email и паролем")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_wrong_email_and_password_fail(self, user_api):
        """Тест входа с неверным email и паролем"""
        # Сначала создаем пользователя
        user_data = {
            "email": f"wrong_both_test_{random.randint(100000, 999999)}@example.com",
            "password": "correct_password_123",
            "name": "Wrong Both Test User"
        }
        
        with allure.step("Создать тестового пользователя"):
            create_response = user_api.create_user(**user_data)
            assert create_response.status_code == 200
        
        response = user_api.login_user("wrong@example.com", "wrong_password")
        
        assert response.status_code == 401, f"Ожидался статус 401, получен {response.status_code}"
        response_data = response.json()
        assert response_data["success"] == False, "Флаг success должен быть False"
        assert AuthResponses.EMAIL_PASSWORD_INCORRECT in response_data["message"].lower()