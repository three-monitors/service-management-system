import pytest
from managers.service_manager import ServiceManager
from exceptions import ClientNotFoundError, InvalidPriceError

@pytest.fixture
def service_manager():
    """Фікстура для ServiceManager"""
    return ServiceManager()

def test_service_manager_initialization(service_manager):
    """Тест ініціалізації ServiceManager"""
    assert service_manager is not None
    assert hasattr(service_manager, 'clients_count')
    assert hasattr(service_manager, 'orders_count')

def test_service_manager_properties(service_manager):
    """Тест властивостей ServiceManager"""
    assert isinstance(service_manager.clients_count, int)
    assert isinstance(service_manager.orders_count, int)
    assert service_manager.clients_count >= 0
    assert service_manager.orders_count >= 0

def test_service_manager_load_from_db(service_manager):
    """Тест завантаження даних з бази"""
    service_manager.load_from_db()
    assert service_manager.clients_count >= 0
    assert service_manager.orders_count >= 0

def test_service_manager_save_data(service_manager):
    """Тест збереження даних"""
    service_manager.save_data()
    # Метод викликає load_from_db, перевірка що не падає
    assert True

def test_service_manager_load_data(service_manager):
    """Тест завантаження даних"""
    service_manager.load_data()
    # Метод викликає load_from_db, перевірка що не падає
    assert True
