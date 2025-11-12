import pytest
import allure
import random
from helpers.api_client import UserAPI, OrderAPI
from data.test_data import UserData, generate_random_email, generate_random_name


@pytest.fixture
@allure.step("Генерация данных случайного пользователя")
def random_user_data():
    return {
        "email": generate_random_email(),
        "password": UserData.BASE_PASSWORD,
        "name": generate_random_name()
    }


@pytest.fixture
def user_api():
    """Фикстура для создания API клиента пользователя"""
    return UserAPI()


@pytest.fixture
@allure.step("Создание тестового пользователя")
def test_user_data():
    """Фикстура для генерации тестовых данных пользователя"""
    return {
        "email": f"test_user_{random.randint(100000, 999999)}@example.com",
        "password": "test_password_123",
        "name": "Test User"
    }


@pytest.fixture
@allure.step("Аутентификация пользователя")
def authenticated_user(user_api, test_user_data):
    """Фикстура для создания и аутентификации пользователя"""
    # Создаем пользователя
    response = user_api.create_user(**test_user_data)
    
    # Убираем условие if-else
    token = response.json().get("accessToken") if response.status_code == 200 else None
    allure.attach(f"Создан пользователь: {test_user_data['email']}", "User Created", allure.attachment_type.TEXT)
    
    # Возвращаем словарь с данными
    return {
        "user_api": user_api,
        "token": token,
        "user_data": test_user_data
    }


@pytest.fixture(autouse=True)
def cleanup_user(authenticated_user):
    """Фикстура для автоматической очистки пользователя после тестов"""
    yield
    # Очистка после теста
    user_api = authenticated_user["user_api"]
    token = authenticated_user["token"]
    with allure.step("Удалить тестового пользователя"):
        delete_response = user_api.delete_user(token)
        allure.attach("Запрос на удаление пользователя выполнен", "User Delete Request", allure.attachment_type.TEXT)


@pytest.fixture
@allure.step("Получение валидных ингредиентов")
def valid_ingredients():
    order_api = OrderAPI()
    
    with allure.step("Запросить список ингредиентов"):
        response = order_api.get_ingredients()
        
        # Убираем условие if-else
        ingredients_data = response.json()
        valid_ids = [ingredient["_id"] for ingredient in ingredients_data.get("data", [])[:2]]
        allure.attach(f"Valid ingredients: {valid_ids}", "Ingredients", allure.attachment_type.TEXT)
        return valid_ids