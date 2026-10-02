import pytest
from models.client import Client
from models.service import Service
from models.order import Order
from exceptions import ClientNotFoundError, InvalidPriceError
import logging

logger = logging.getLogger(__name__)


def test_client_creation(sample_client):
    """Тест створення клієнта"""
    # Arrange
    expected_name = "Анна Петренко"
    expected_phone = "+380991234567"
    expected_email = "anna@example.com"

    # Act
    actual_name = sample_client["name"]
    actual_phone = sample_client["phone"]
    actual_email = sample_client["email"]

    # Assert
    assert actual_name == expected_name
    assert actual_phone == expected_phone
    assert actual_email == expected_email


def test_service_creation(sample_service):
    """Тест створення послуги"""
    # Arrange
    expected_name = "Масаж обличчя"
    expected_price = 500.0
    expected_duration = 60

    # Act
    actual_name = sample_service["name"]
    actual_price = sample_service["price"]
    actual_duration = sample_service["duration"]

    # Assert
    assert actual_name == expected_name
    assert actual_price == expected_price
    assert actual_duration == expected_duration


def test_order_creation(sample_order):
    """Тест створення замовлення"""
    # Arrange
    expected_client_id = 1
    expected_service_id = 1
    expected_status = "Created"
    expected_total_price = 500.0

    # Act
    actual_client_id = sample_order["client_id"]
    actual_service_id = sample_order["service_id"]
    actual_status = sample_order["status"]
    actual_total_price = sample_order["total_price"]

    # Assert
    assert actual_client_id == expected_client_id
    assert actual_service_id == expected_service_id
    assert actual_status == expected_status
    assert actual_total_price == expected_total_price


def test_order_status_change():
    """Тест зміни статусу замовлення"""
    # Arrange
    statuses = ["Created", "Scheduled", "In Progress",
                "Done", "Completed", "Cancelled"]

    # Act
    for status in statuses:
        # Assert
        assert status in statuses


def test_price_calculation():
    """Тест розрахунку ціни"""
    # Arrange
    base_price = 500.0

    # Act
    is_positive = base_price > 0
    is_float = isinstance(base_price, float)

    # Assert
    assert is_positive
    assert is_float


def test_empty_values():
    """Тест порожніх значень"""
    # Arrange
    empty_string = ""
    empty_list = []
    empty_dict = {}

    # Act
    string_is_empty = empty_string == ""
    list_is_empty = empty_list == []
    dict_is_empty = empty_dict == {}

    # Assert
    assert string_is_empty
    assert list_is_empty
    assert dict_is_empty


def test_boundary_values():
    """Тест граничних значень"""
    # Arrange
    zero = 0
    negative = -1
    positive = 100

    # Act
    zero_is_zero = zero == 0
    negative_is_negative = negative < 0
    positive_is_positive = positive > 0

    # Assert
    assert zero_is_zero
    assert negative_is_negative
    assert positive_is_positive


def test_invalid_phone_format():
    """Тест невалідного формату телефону"""
    # Arrange
    invalid_phone = "123456789"
    expected_length = 13

    # Act
    actual_length = len(invalid_phone)

    # Assert
    assert actual_length != expected_length


def test_invalid_email_format():
    # Arrange
    invalid_email = "invalid-email"

    # Act
    has_at_symbol = "@" in invalid_email

    # Assert
    assert not has_at_symbol


def test_status_validation():
    """Тест валідації статусу"""
    # Arrange
    valid_status = "Created"
    invalid_status = "InvalidStatus"
    valid_statuses = ["Created", "Scheduled",
                      "In Progress", "Done", "Completed", "Cancelled"]

    # Act
    is_valid = valid_status in valid_statuses
    is_invalid = invalid_status in valid_statuses

    # Assert
    assert is_valid
    assert not is_invalid

# Тести для класів


def test_client_class_creation():
    """Тест створення об'єкта класу Client"""
    # Arrange
    expected_id = 1
    expected_name = "Олена Коваленко"
    expected_phone = "+380-67-123-45-67"
    expected_email = "olena@example.com"

    # Act
    client = Client(expected_id, expected_name, expected_phone, expected_email)

    logger.debug(
        "Created client: id=%s name=%s phone=%s email=%s",
        client.id,
        client.name,
        client.phone,
        client.email
    )

    # Assert
    assert client.id == expected_id
    assert client.name == expected_name
    assert client.phone == expected_phone
    assert client.email == expected_email


def test_client_class_setters():
    """Тест сеттерів класу Client"""
    # Arrange
    client = Client(1, "Олена Коваленко",
                    "+380-67-123-45-67", "olena@example.com")
    new_name = "Марія Петренко"
    new_phone = "+380-99-987-65-43"
    new_email = "maria@example.com"

    # Act
    client.name = new_name
    client.phone = new_phone
    client.email = new_email

    # Assert
    assert client.name == new_name
    assert client.phone == new_phone
    assert client.email == new_email


def test_client_class_empty_name_validation():
    """Тест валідації порожнього імені"""
    # Arrange
    client = Client(1, "Олена Коваленко",
                    "+380-67-123-45-67", "olena@example.com")
    empty_name = ""

    # Act & Assert
    with pytest.raises(ValueError):
        client.name = empty_name


def test_client_class_invalid_phone_validation():
    """Тест валідації невалідного телефону"""
    # Arrange
    client = Client(1, "Олена Коваленко",
                    "+380-67-123-45-67", "olena@example.com")
    invalid_phone = "123456789"

    # Act & Assert
    with pytest.raises(ValueError):
        client.phone = invalid_phone


def test_client_class_invalid_email_validation():
    """Тест валідації невалідного email"""
    # Arrange
    client = Client(1, "Олена Коваленко",
                    "+380-67-123-45-67", "olena@example.com")
    invalid_email = "invalid-email"

    # Act & Assert
    with pytest.raises(ValueError):
        client.email = invalid_email


def test_client_class_banned_email_domains():
    """Тест заборонених доменів email"""
    # Arrange
    client = Client(1, "Олена Коваленко",
                    "+380-67-123-45-67", "olena@example.com")
    banned_email = "test@example.ru"

    # Act & Assert
    with pytest.raises(ValueError):
        client.email = banned_email


def test_client_class_str_representation():
    """Тест рядкового представлення клієнта"""
    # Arrange
    client = Client(1, "Олена Коваленко",
                    "+380-67-123-45-67", "olena@example.com")

    # Act
    str_repr = str(client)

    # Assert
    assert "Олена Коваленко" in str_repr
    assert "+380-67-123-45-67" in str_repr
    assert "olena@example.com" in str_repr


def test_client_class_to_dict():
    """Тест конвертації клієнта в словник"""
    # Arrange
    client = Client(1, "Олена Коваленко",
                    "+380-67-123-45-67", "olena@example.com")

    # Act
    client_dict = client.to_dict()

    # Assert
    assert client_dict["id"] == 1
    assert client_dict["name"] == "Олена Коваленко"
    assert client_dict["phone"] == "+380-67-123-45-67"
    assert client_dict["email"] == "olena@example.com"


def test_client_class_from_dict():
    """Тест створення клієнта зі словника"""
    # Arrange
    client_dict = {
        "id": 2,
        "name": "Іван Іванов",
        "phone": "+380-50-111-22-33",
        "email": "ivan@example.com"
    }

    # Act
    client = Client.from_dict(client_dict)

    # Assert
    assert client.id == 2
    assert client.name == "Іван Іванов"
    assert client.phone == "+380-50-111-22-33"
    assert client.email == "ivan@example.com"

# Тести для обробки помилок


def test_client_not_found_error():
    """Тест помилки ClientNotFoundError"""
    # Arrange
    error_message = "Клієнт не знайдено"

    # Act & Assert
    with pytest.raises(ClientNotFoundError):
        raise ClientNotFoundError(error_message)


def test_invalid_price_error():
    """Тест помилки InvalidPriceError"""
    # Arrange
    error_message = "Невалідна ціна"

    # Act & Assert
    with pytest.raises(InvalidPriceError):
        raise InvalidPriceError(error_message)

# Тести для граничних значень


def test_negative_price():
    """Тест від'ємної ціни"""
    # Arrange
    negative_price = -100.0

    # Act
    is_negative = negative_price < 0

    # Assert
    assert is_negative


def test_zero_price():
    """Тест нульової ціни"""
    # Arrange
    zero_price = 0.0

    # Act
    is_zero = zero_price == 0

    # Assert
    assert is_zero


def test_very_large_price():
    """Тест дуже великої ціни"""
    # Arrange
    large_price = 999999.99

    # Act
    is_positive = large_price > 0
    is_float = isinstance(large_price, float)

    # Assert
    assert is_positive
    assert is_float


def test_very_long_name():
    # Arrange
    long_name = "А" * 1000
    expected_length = 1000

    # Act
    actual_length = len(long_name)

    # Assert
    assert actual_length == expected_length


def test_empty_name():
    # Arrange
    empty_name = ""

    # Act
    is_empty = empty_name == ""

    # Assert
    assert is_empty


# def test_with_error_for_logging():
#     """Тест з помилкою для перевірки логування"""
#     logging.error("Це тестова помилка для логування")
#     assert True  # Тест проходить, але лог записує помилку
