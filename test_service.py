import pytest
from models.service import Service
from exceptions import InvalidPriceError
import logging

logger = logging.getLogger(__name__)


def test_service_creation():
    """Тест створення послуги"""
    # Arrange
    expected_id = 1
    expected_name = "Масаж обличчя"
    expected_price = 500.0
    expected_duration = 60

    # Act
    service = Service(expected_id, expected_name,
                      expected_price, expected_duration)

    # Assert
    assert service.id == expected_id
    assert service.name == expected_name
    assert service.price == expected_price
    assert service.duration == expected_duration


@pytest.mark.parametrize(
    "price, duration, expected_error, error_message",
    [
        (-100.0, 60, InvalidPriceError, "Price cannot be negative"),
        (500.0, 0, ValueError, "Duration must be positive"),
        (-100.0, 0, InvalidPriceError, "Price cannot be negative"),
    ],
    ids=[
        "negative_price",
        "zero_duration",
        "negative_price_zero_duration",
    ]
)
def test_service_validation(price, duration, expected_error, error_message):
    """Тест валідації послуги з параметризацією"""
    # Arrange
    test_id = 1
    test_name = "Тестова послуга"

    logger.debug(
        "Testing service validation: price=%s duration=%s expected_error=%s",
        price,
        duration,
        expected_error.__name__
    )

    # Act & Assert
    with pytest.raises(expected_error, match=error_message):
        Service(test_id, test_name, price, duration)
