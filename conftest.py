import os
import sys
import pytest
import logging


# Створюємо папку logs якщо не існує
LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)


# Налаштування конфігурації логування
logging.basicConfig(

    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Виведення в консоль
        logging.FileHandler(os.path.join(
            LOGS_DIR, "example.log"), encoding="utf-8")  # Запис у файл
    ]
)


@pytest.fixture
def sample_client():
    """Фікстура для тестового клієнта"""
    client_data = {
        "name": "Анна Петренко",
        "phone": "+380991234567",
        "email": "anna@example.com"
    }
    yield client_data
    del client_data


@pytest.fixture
def sample_service():
    """Фікстура для тестової послуги"""
    service_data = {
        "name": "Масаж обличчя",
        "price": 500.0,
        "duration": 60
    }
    yield service_data
    del service_data


@pytest.fixture
def sample_order():
    """Фікстура для тестового замовлення"""
    order_data = {
        "client_id": 1,
        "service_id": 1,
        "status": "Created",
        "total_price": 500.0
    }
    yield order_data
    del order_data
