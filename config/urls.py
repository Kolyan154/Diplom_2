class URLs:
    """Класс для хранения всех URL endpoints API"""
    
    # Используем правильный домен из задания
    BASE_URL = "https://stellarburgers.education-services.ru/api"
    
    # Auth endpoints
    REGISTER = "/auth/register"
    LOGIN = "/auth/login"
    USER = "/auth/user"
    LOGOUT = "/auth/logout"
    TOKEN = "/auth/token"
    
    # Order endpoints
    ORDERS = "/orders"
    INGREDIENTS = "/ingredients"
    
    # User endpoints
    USER_ORDERS = "/orders/user"