import sys
import os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, current_dir)

from models.order import Order
from models.client import Client
from models.service import Service
from exceptions import (
    ClientNotFoundError,
    InvalidPriceError,
    InvalidMenuChoiceError
)
from database import get_connection, init_db
from models_db import (
    add_client, add_service, create_order,
    get_orders_with_details, update_order_status,
    get_all_orders
)
import re
from typing import List, Optional
from decorators import log_action, validate_price, notify_client


class ServiceManager:
    """Клас керуючого Beauty Clinic"""

    def __init__(self):
        init_db()  # Ініціалізуємо базу даних
        self.__clients = []
        self.__orders = []
        self.__services = []
        self.load_from_db()  # Завантажуємо дані з бази

    def load_from_db(self):
        """Завантажує дані з бази даних"""
        conn = get_connection()
        cursor = conn.cursor()

        # Завантажуємо клієнтів
        cursor.execute("SELECT * FROM clients")
        self.__clients = [
            Client(row['id'], row['name'], row['phone'], row['email'])
            for row in cursor.fetchall()
        ]

        # Завантажуємо послуги
        cursor.execute("SELECT * FROM services")
        self.__services = [
            Service(row['id'], row['name'], row['price'], row['duration'])
            for row in cursor.fetchall()
        ]

        # Завантажуємо замовлення
        cursor.execute("SELECT * FROM orders")
        self.__orders = []
        for row in cursor.fetchall():
            # Знаходимо клієнта та послугу для замовлення
            cursor.execute(
                "SELECT name FROM clients WHERE id = ?", (row['client_id'],))
            client_name = cursor.fetchone()['name']

            cursor.execute(
                "SELECT name FROM services WHERE id = ?", (row['service_id'],))
            service_name = cursor.fetchone()['name']

            order = Order(
                row['id'], client_name, service_name, "Unknown",
                row['status'], "", row['total_price']
            )
            self.__orders.append(order)

        conn.close()

    @property
    def clients_count(self) -> int:
        return len(self.__clients)

    @property
    def orders_count(self) -> int:
        return len(self.__orders)

    @log_action
    def add_client(self) -> None:
        """Додати клієнта"""
        try:
            name = input("Client name: ").strip()
            if name == "":
                raise ValueError("Name cannot be empty")

            for client in self.__clients:
                if client.name == name:
                    raise ValueError("Client already exists")

            phone = input("Phone (format: +380-XX-XXX-XX-XX): ").strip()
            if not re.fullmatch(r"\+\d{3}-\d{2}-\d{3}-\d{2}-\d{2}", phone):
                raise ValueError("Invalid phone format. Use +380-XX-XXX-XX-XX")

            email = input("Email: ").strip()
            if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email):
                raise ValueError("Invalid email format")

            banned_domains = [".ru", ".su", ".рф"]
            email_lower = email.lower()
            for domain in banned_domains:
                if email_lower.endswith(domain):
                    raise ValueError(
                        f"The use of email with the {domain} domain is prohibited")

            # Додаємо в базу даних
            client_id = add_client(name, phone, email)
            client = Client(client_id, name, phone, email)
            self.__clients.append(client)
            print(f"Client '{name}' added with ID: {client.id}")

        except ValueError as e:
            print(f"Помилка: {e}")

    def list_clients(self) -> None:
        """Перегляд списку клієнтів"""
        if len(self.__clients) == 0:
            print("No clients yet")
            return

        print("\n--- Clients ---")
        for i, client in enumerate(self.__clients):
            print(f"{i + 1}. ID: {client.id} | {client}")

    @log_action
    def delete_client(self) -> None:
        """Видалити клієнта"""
        try:
            if len(self.__clients) == 0:
                raise ValueError("No clients to delete")

            self.list_clients()
            raw = input("Enter client ID number to delete: ")
            if not raw.isdigit():
                raise ValueError("Please enter a ID number")

            client_id = int(raw)  # Отримуємо ID

            # Знаходимо клієнта за ID
            client_to_delete = None
            index = -1
            for i, client in enumerate(self.__clients):
                if client.id == client_id:
                    client_to_delete = client
                    index = i
                    break

            if client_to_delete is None:
                raise ValueError("Client not found")

            # Видаляємо зі списку
            self.__clients.pop(index)

            # Видаляємо з бази даних
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clients WHERE id = ?", (client_id,))
            conn.commit()
            conn.close()

            # Перезавантажуємо дані з бази даних
            self.load_from_db()

            print(
                f"Deleted: ID {client_to_delete.id} | {client_to_delete.name}")

        except ValueError as e:
            print(f"Помилка: {e}")

    @log_action
    @validate_price
    def create_order(self) -> None:
        """Створити замовлення"""
        try:
            if len(self.__clients) == 0:
                raise ValueError("No clients yet. Add a client first.")

            print("Clients:", [client.name for client in self.__clients])
            client_name = input("Client name: ").strip()

            client = None
            for c in self.__clients:
                if c.name == client_name:
                    client = c
                    break

            if client is None:
                raise ClientNotFoundError(f"Client '{client_name}' not found")

            if len(self.__services) == 0:
                raise ValueError("No services yet. Add services first.")

            print("Services:", [service.name for service in self.__services])
            service_name = input("Service name: ").strip()

            service = None
            for s in self.__services:
                if s.name == service_name:
                    service = s
                    break

            if service is None:
                raise ValueError(f"Service '{service_name}' not found")

            # Валідація статусу
            status_input = input(
                "Status (Scheduled/In Progress/Done/Cancelled): ").strip()
            valid_statuses = ["Scheduled", "In Progress", "Done", "Cancelled"]
            if status_input not in valid_statuses:
                raise ValueError(
                    f"Invalid status. Must be one of: {valid_statuses}")

            # Створюємо замовлення в базі даних
            order_id = create_order(client.id, service.id)

            # Оновлюємо статус замовлення
            update_order_status(order_id, status_input)

            # Перезавантажуємо дані з бази
            self.load_from_db()

            print(f"Order created with ID: {order_id}!")

        except (ValueError, ClientNotFoundError, InvalidPriceError) as e:
            print(f"Помилка: {e}")

    @log_action
    @notify_client
    def update_status(self) -> None:
        """Оновити статус замовлення"""
        try:
            if len(self.__orders) == 0:
                raise ValueError("No orders yet")

            self.list_orders()
            raw = input("Enter order ID to update status: ")
            if not raw.isdigit():
                raise ValueError("Please enter a number")

            order_id = int(raw)

            # Знаходимо замовлення за ID
            order_to_update = None
            for order in self.__orders:
                if order.id == order_id:
                    order_to_update = order
                    break

            if order_to_update is None:
                raise ValueError("Order not found")

            print("\nStatus options:")
            print("1. Scheduled")
            print("2. In Progress")
            print("3. Done")
            print("4. Cancelled")
            status_choice = input("Choose new status: ")

            status_map = {
                "1": "Scheduled",
                "2": "In Progress",
                "3": "Done",
                "4": "Cancelled"
            }

            if status_choice in status_map:
                new_status = status_map[status_choice]
                update_order_status(order_id, new_status)
                self.load_from_db()  # Перезавантажуємо дані
                print(f"Status changed to {new_status}")
            else:
                raise ValueError("Invalid choice")

        except ValueError as e:
            print(f"Помилка: {e}")

    @log_action
    def delete_order(self) -> None:
        """Видалити замовлення"""
        try:
            if len(self.__orders) == 0:
                raise ValueError("Nothing to delete")

            self.list_orders()
            raw = input("Enter order ID to delete: ")
            if not raw.isdigit():
                raise ValueError("Please enter a ID number")

            order_id = int(raw)

            # Знаходимо замовлення за ID
            order_to_delete = None
            for i, order in enumerate(self.__orders):
                if order.id == order_id:
                    order_to_delete = order
                    index = i
                    break

            if order_to_delete is None:
                raise ValueError("Order not found")

            # Видаляємо з бази даних
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
            conn.commit()
            conn.close()

            self.load_from_db()  # Перезавантажуємо дані
            print(f"Deleted order with ID: {order_id}")

        except ValueError as e:
            print(f"Помилка: {e}")

    def list_orders(self) -> None:
        """Показати список замовлень"""
        if len(self.__orders) == 0:
            print("No orders yet")
            return

        print("\n--- Orders ---")
        for i, order in enumerate(self.__orders):
            print(f"{i + 1}. ID: {order.id} | {order}")

    def save_data(self) -> None:
        """Збереження даних в базу даних"""
        self.load_from_db()
        print("Data synchronized with database")

    def load_data(self) -> None:
        """Завантаження даних з бази даних"""
        self.load_from_db()
        print("Data loaded from database")
