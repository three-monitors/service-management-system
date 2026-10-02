import pytest
import sys
import os

# Додаємо поточну директорію в PYTHONPATH
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)


@pytest.fixture
def sample_client():
    """Фікстура для тестового клієнта"""
    return {
        "name": "Анна Петренко",
        "phone": "+380991234567",
        "email": "anna@example.com"
    }


@pytest.fixture
def sample_service():
    """Фікстура для тестової послуги"""
    return {
        "name": "Масаж обличчя",
        "price": 500.0,
        "duration": 60
    }


@pytest.fixture
def sample_order():
    """Фікстура для тестового замовлення"""
    return {
        "client_id": 1,
        "service_id": 1,
        "status": "Created",
        "total_price": 500.0
    }
