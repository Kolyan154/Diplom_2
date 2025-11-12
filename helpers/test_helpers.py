import allure
from helpers.api_client import UserAPI


class TestHelpers:
    """Вспомогательные методы для тестов"""
    
    @staticmethod
    @allure.step("Создание тестового пользователя")
    def create_test_user(user_api, email_prefix="test_user"):
        """Создание тестового пользователя и возврат данных"""
        import random
        user_data = {
            "email": f"{email_prefix}_{random.randint(100000, 999999)}@example.com",
            "password": "test_password_123",
            "name": "Test User"
        }
        
        response = user_api.create_user(**user_data)
        return user_data, response
    
    @staticmethod
    @allure.step("Выполнение тестов с неполными данными")
    def test_incomplete_users(user_api, test_cases):
        """Выполнение тестов с неполными данными пользователя"""
        results = []
        for test_case in test_cases:
            response = user_api.create_user(
                email=test_case["email"],
                password=test_case["password"], 
                name=test_case["name"]
            )
            results.append({
                "test_case": test_case,
                "response": response
            })
        return results
    
    @staticmethod
    @allure.step("Выполнение тестов с неверными учетными данными")
    def test_invalid_credentials(user_api, test_cases):
        """Выполнение тестов с неверными учетными данными"""
        results = []
        for test_case in test_cases:
            response = user_api.login_user(
                test_case["email"],
                test_case["password"]
            )
            results.append({
                "test_case": test_case,
                "response": response
            })
        return results