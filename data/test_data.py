import random
import string


def generate_random_email():
    """Генерация случайного email"""
    username = ''.join(random.choices(string.ascii_lowercase, k=8))
    domain = ''.join(random.choices(string.ascii_lowercase, k=6))
    return f"{username}@{domain}.com"


def generate_random_name():
    """Генерация случайного имени"""
    return ''.join(random.choices(string.ascii_letters, k=10))


class UserData:
    """Тестовые данные для пользователей"""
    
    BASE_PASSWORD = "password123"
    
    # Существующий пользователь для тестов - используем уникальный email
    EXISTING_USER = {
        "email": f"test_user_{random.randint(1000, 9999)}@example.com",
        "password": "test_password_123",
        "name": "Test User"
    }
    
    # Неполные данные пользователя - исправляем структуру
    @staticmethod
    def get_incomplete_users():
        """Возвращает неполные данные пользователя с правильной структурой"""
        return [
            {"email": "", "password": UserData.BASE_PASSWORD, "name": "Test User"},  # пустой email
            {"email": "test@example.com", "password": "", "name": "Test User"},  # пустой password
            {"email": "test@example.com", "password": UserData.BASE_PASSWORD, "name": ""}  # пустое name
        ]
    
    # Неверные учетные данные
    @staticmethod
    def get_invalid_credentials():
        """Возвращает неверные учетные данные"""
        return [
            {"email": "wrong@example.com", "password": UserData.BASE_PASSWORD},
            {"email": "nonexistent@example.com", "password": "wrong_password"},
            {"email": "wrong@example.com", "password": "wrong_password"}
        ]


class OrderData:
    """Тестовые данные для заказов"""
    
    # Невалидные ингредиенты - используем заведомо несуществующие ID
    INVALID_INGREDIENTS = ["invalid_ingredient_1", "invalid_ingredient_2"]
    EMPTY_INGREDIENTS = []