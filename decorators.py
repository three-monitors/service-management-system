import logging
import functools
from datetime import datetime
import time
import os

# Створюємо папку logs якщо не існує
LOGS_DIR = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(LOGS_DIR, exist_ok=True)

# Налаштування логування для Service Management System
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, "service_manager.log"), encoding="utf-8"),
        logging.StreamHandler()
    ]
)


# Декоратор 1: @log_action
def log_action(func):
    """
    Логує операції над сутностями системи: замовлення, клієнти, послуги.
    Рівень логування — INFO.
    Формат: [ДІЯ] назва_функції | аргументи | час виконання мс
    Використовується на: create_order, update_status, delete_order, add_client
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # в мілісекундах

        logging.info(
            f"[ДІЯ] {func.__name__} | {args} | {execution_time:.1f} мс")
        return result
    return wrapper


# Декоратор 2: @validate_price
def validate_price(func):
    """
    Перевіряє аргумент price:
    — має бути int або float
    — має бути >= 0 (безкоштовні послуги дозволені)
    Якщо ні — логує WARNING і повертає None.
    Використовується на: create_order, add_service, add_part
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Знаходимо price в args або kwargs
        price = None
        if args and len(args) > 0:
            # Припускаємо що price перший аргумент
            price = args[0]
        elif 'price' in kwargs:
            price = kwargs['price']

        if price is not None:
            if not isinstance(price, (int, float)):
                logging.warning(f"Ціна має бути числом, отримано: {price}")
                return None
            if price < 0:
                logging.warning(f"Ціна має бути >= 0, отримано: {price}")
                return None

        return func(*args, **kwargs)
    return wrapper


# Декоратор 3: @notify_client (заглушка)
def notify_client(func):
    """
    ЗАГЛУШКА — буде реалізовано у Занятті 25 (HTTP + Telegram Bot API).
    Майбутня логіка:
    — після зміни статусу замовлення — надіслати клієнту повідомлення
    — через requests.post до Telegram Bot API
    Зараз: логує DEBUG "Сповіщення ще не налаштовано" і виконує функцію.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        logging.debug(
            f"[notify_client] Сповіщення клієнта після {func.__name__}: "
            f"ще не реалізовано (Заняття 25)"
        )
        return result
    return wrapper
