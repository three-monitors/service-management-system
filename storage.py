import json
import os
from typing import List, Dict, Optional
from models.client import Client
from models.service import Service
from models.order import Order


def load_clients(filepath: str) -> List[Client]:
    """Завантажує клієнтів з JSON файлу"""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            clients_data = json.load(file)
            return [Client.from_dict(data) for data in clients_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Помилка при розборі JSON з файлу {filepath}")
        return []


def save_clients(filepath: str, clients: List[Client]) -> None:
    """Зберігає клієнтів у JSON файл"""
    try:
        clients_data = [client.to_dict() for client in clients]
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(clients_data, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Помилка при збереженні клієнтів: {e}")


def load_services(filepath: str) -> List[Service]:
    """Завантажує послуги з JSON файлу"""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            services_data = json.load(file)
            return [Service.from_dict(data) for data in services_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Помилка при розборі JSON з файлу {filepath}")
        return []


def save_services(filepath: str, services: List[Service]) -> None:
    """Зберігає послуги у JSON файл"""
    try:
        services_data = [service.to_dict() for service in services]
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(services_data, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Помилка при збереженні послуг: {e}")


def load_orders(filepath: str) -> List[Order]:
    """Завантажує замовлення з JSON файлу"""
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            orders_data = json.load(file)
            return [Order.from_dict(data) for data in orders_data]
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print(f"Помилка при розборі JSON з файлу {filepath}")
        return []


def save_orders(filepath: str, orders: List[Order]) -> None:
    """Зберігає замовлення у JSON файл"""
    try:
        orders_data = [order.to_dict() for order in orders]
        with open(filepath, "w", encoding="utf-8") as file:
            json.dump(orders_data, file, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"Помилка при збереженні замовлень: {e}")
