from decorators import log_action, validate_price, notify_client
from typing import List, Optional
import re
from models_db import (
    add_client, add_service, create_order,
    get_orders_with_details, update_order_status,
    get_all_orders
)
from database import get_connection, init_db
from exceptions import (
    ClientNotFoundError,
    InvalidPriceError,
    InvalidMenuChoiceError
)
from models.service import Service
from models.client import Client
from models.order import Order
import sys
import os

# Додаємо кореневу папку проєкту до sys.path
current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


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
            Client(
                row['id'],
                row['name'],
                row['phone'],
                row['email']
            )
            for row in cursor.fetchall()
        ]

        # Завантажуємо послуги
        cursor.execute("SELECT * FROM services")
        self.__services = [
            Service(
                row['id'],
                row['name'],
                row['price'],
                row['duration']
            )
            for row in cursor.fetchall()
        ]

        # Завантажуємо замовлення
        cursor.execute("SELECT * FROM orders")
        self.__orders = []
        for row in cursor.fetchall():
            # Знаходимо клієнта та послугу для замовлення
            cursor.execute("SELECT * FROM orders")
        self.__orders = []

        for row in cursor.fetchall():
            cursor.execute(
                "SELECT name FROM clients WHERE id = ?",
                (row['client_id'],)
            )
            client_row = cursor.fetchone()
            client_name = client_row['name'] if client_row else "Unknown"

            cursor.execute(
                "SELECT name FROM services WHERE id = ?",
                (row['service_id'],)
            )
            service_row = cursor.fetchone()
            service_name = service_row['name'] if service_row else "Unknown"

            order = Order(
                row['id'],
                client_name,
                service_name,
                "Unknown",
                row['status'],
                "",
                row['total_price']
            )
            self.__orders.append(order)

        conn.close()

    # Властивості для доступу до даних
    @property
    def clients(self):
        """Повертає список клієнтів"""
        return self.__clients

    @property
    def services(self):
        """Повертає список послуг"""
        return self.__services

    @property
    def orders(self):
        """Повертає список замовлень"""
        return self.__orders

    @property
    def clients_count(self) -> int:
        return len(self.__clients)

    @property
    def orders_count(self) -> int:
        return len(self.__orders)

    # Допоміжні методи для клієнта
    @staticmethod
    def normalize_phone(phone: str) -> str:
        """
        Нормалізує український номер телефону.
        Приймаються, наприклад:
        +380-67-123-45-67
        +380671234567
        380671234567
        80671234567
        0671234567
        067 123 45 67
        +380 67 123 45 67

        Результат:
        +380-67-123-45-67
        """

        if not isinstance(phone, str):
            raise ValueError("Номер телефону має бути текстом")
        # Прибираємо все, крім цифр
        digits = re.sub(r"\D", "", phone)
        # 380XXXXXXXXX
        if len(digits) == 12 and digits.startswith("380"):
            digits = digits[3:]
        # 80XXXXXXXXX
        elif len(digits) == 11 and digits.startswith("80"):
            digits = digits[2:]
        # 0XXXXXXXXX
        elif len(digits) == 10 and digits.startswith("0"):
            digits = digits[1:]
        # 8XXXXXXXXX
        elif len(digits) == 10 and digits.startswith("8"):
            digits = digits[1:]
        else:
            raise ValueError(
                "Невірний номер телефону. "
                "Введіть український номер, наприклад "
                "+380-67-123-45-67 або 067 123 45 67"
            )
        if len(digits) != 9:
            raise ValueError(
                "Невірний номер телефону. "
                "Український номер повинен містити 9 цифр "
                "після коду 380"
            )
        return (
            f"+380-{digits[:2]}-{digits[2:5]}-"
            f"{digits[5:7]}-{digits[7:9]}"
        )

    @staticmethod
    def validate_email(email: str) -> str:
        """Перевіряє та повертає email."""

        if not isinstance(email, str):
            raise ValueError("Email має бути текстом")
        email = email.strip()
        email_pattern = (
            r"^[a-zA-Z0-9._%+-]+@"
            r"[a-zA-Z0-9.-]+\."
            r"[a-zA-Z]{2,}$"
        )
        if not re.fullmatch(email_pattern, email):
            raise ValueError("Невірний формат email")
        banned_domains = [".ru", ".su", ".рф"]
        email_lower = email.lower()
        for domain in banned_domains:
            if email_lower.endswith(domain):
                raise ValueError(
                    f"Використання email з доменом "
                    f"{domain} заборонено"
                )
        return email

    # Додавання клієнта через консоль
    @log_action
    def add_client(self) -> None:
        """Додати клієнта через консоль."""
        try:
            name = input("Client name: ").strip()
            if name == "":
                raise ValueError("Name cannot be empty")

            for client in self.__clients:
                if client.name.lower() == name.lower():
                    raise ValueError("Client already exists")
            phone = input(
                "Phone (format: +380-XX-XXX-XX-XX): "
            ).strip()
            phone = self.normalize_phone(phone)
            email = input("Email: ").strip()
            email = self.validate_email(email)
            client_id = add_client(name, phone, email)
            client = Client(
                client_id,
                name,
                phone,
                email
            )
            self.__clients.append(client)
            print(
                f"Client '{name}' added with ID: {client.id}"
            )
        except ValueError as e:
            print(f"Помилка: {e}")

    # Додавання клієнта через Telegram
    @log_action
    def add_client_with_params(
        self,
        name: str,
        phone: str,
        email: str
    ) -> int:
        """Додає клієнта з готовими параметрами."""
        name = name.strip()
        if not name:
            raise ValueError(
                "Ім'я клієнта не може бути порожнім"
            )
        for client in self.__clients:
            if client.name.lower() == name.lower():
                raise ValueError(
                    f"Клієнт '{name}' вже існує"
                )
        phone = self.normalize_phone(phone)
        email = self.validate_email(email)
        client_id = add_client(
            name,
            phone,
            email
        )
        client = Client(
            client_id,
            name,
            phone,
            email
        )
        self.__clients.append(client)
        return client_id

    # Клієнти
    def list_clients(self) -> None:
        """Перегляд списку клієнтів."""
        if len(self.__clients) == 0:
            print("No clients yet")
            return
        print("\n--- Clients ---")
        for i, client in enumerate(self.__clients):
            print(
                f"{i + 1}. ID: {client.id} | {client}"
            )

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

    # Замовлення
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
                "Status (Created/Scheduled/In Progress/Done/Completed/Cancelled): ").strip()
            valid_statuses = ["Created", "Scheduled",
                              "In Progress", "Done", "Completed", "Cancelled"]
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
            print("1. Created")
            print("2. Scheduled")
            print("3. In Progress")
            print("4. Done")
            print("5. Completed")
            print("6. Cancelled")
            status_choice = input("Choose new status: ")

            status_map = {
                "1": "Created",
                "2": "Scheduled",
                "3": "In Progress",
                "4": "Done",
                "5": "Completed",
                "6": "Cancelled"
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

    # Синхронізація
    def save_data(self) -> None:
        """Збереження даних в базу даних"""
        self.load_from_db()
        print("Data synchronized with database")

    def load_data(self) -> None:
        """Завантаження даних з бази даних"""
        self.load_from_db()
        print("Data loaded from database")
