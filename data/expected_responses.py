class AuthResponses:
    """Ожидаемые ответы для эндпоинтов авторизации"""
    
    USER_ALREADY_EXISTS = {
        "success": False,
        "message": "User already exists"
    }
    
    REQUIRED_FIELD_MISSING = {
        "success": False,
        "message": "Email, password and name are required fields"
    }
    
    INVALID_CREDENTIALS = {
        "success": False,
        "message": "email or password are incorrect"
    }
    
    # Новые тексты ответов
    EMAIL_PASSWORD_INCORRECT = "email or password are incorrect"
    REQUIRED_FIELDS = "Email, password and name are required fields"


class OrderResponses:
    """Ожидаемые ответы для эндпоинтов заказов"""
    
    INGREDIENTS_REQUIRED = {
        "success": False,
        "message": "Ingredient ids must be provided"
    }
    
    INVALID_INGREDIENTS = {
        "success": False,
        "message": "One or more ingredient ids are invalid"
    }


class CommonResponses:
    """Общие ожидаемые ответы"""
    
    SUCCESS_TRUE = {"success": True}
    SUCCESS_FALSE = {"success": False}
    
    # Новые тексты ответов
    INTERNAL_SERVER_ERROR = "Internal Server Error"
    CONNECTION_FAILED = "Connection failed"
    REQUEST_TIMEOUT = "Request timeout"