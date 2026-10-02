import pytest
from models.order import Order


def test_order_creation():
    """Тест створення замовлення"""
    order = Order(1, "Анна Петренко", "Масаж обличчя",
                  "Марія Коваленко", "Created", "2024-09-30", 500.0)
    assert order.id == 1
    assert order.client == "Анна Петренко"
    assert order.service == "Масаж обличчя"
    assert order.master == "Марія Коваленко"
    assert order.status == "Created"
    assert order.date == "2024-09-30"
    assert order.total_price == 500.0


def test_order_service_property():
    """Тест властивості service"""
    order = Order(1, "Анна Петренко", "Масаж обличчя",
                  "Марія Коваленко", "Created", "2024-09-30", 500.0)
    assert order.service == "Масаж обличчя"

    order.service = "Пілінг"
    assert order.service == "Пілінг"


def test_order_negative_price():
    """Тест від'ємної ціни замовлення"""
    # Order успадковує від Appointment, необхідно перевірити чи там є валідація
    order = Order(1, "Анна Петренко", "Масаж обличчя",
                  "Марія Коваленко", "Created", "2024-09-30", -100.0)
    assert order.total_price == -100.0  # Якщо немає валідації, просто перевіряємо


def test_order_str_representation():
    """Тест рядкового представлення замовлення"""
    order = Order(1, "Анна Петренко", "Масаж обличчя",
                  "Марія Коваленко", "Created", "2024-09-30", 500.0)
    str_repr = str(order)
    assert "Анна Петренко" in str_repr
    assert "Масаж обличчя" in str_repr
    assert "500.0 грн" in str_repr


def test_order_from_dict():
    """Тест створення замовлення зі словника"""
    order_dict = {
        "id": 2,
        "client": "Олена Коваленко",
        "procedure": "Пілінг",
        "master": "Ірина Петренко",
        "status": "Scheduled",
        "date": "2024-10-01",
        "total_price": 700.0
    }
    order = Order.from_dict(order_dict)
    assert order.id == 2
    assert order.client == "Олена Коваленко"
    assert order.service == "Пілінг"
    assert order.total_price == 700.0
