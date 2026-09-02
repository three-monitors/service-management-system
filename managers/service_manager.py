from models.order import Order
from models.client import Client
from exceptions import (
    ClientNotFoundError,
    InvalidPriceError,
    InvalidMenuChoiceError
)
import json
import re
from typing import List, Optional
import sys
import os

current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, current_dir)


class ServiceManager:
    """Клас керуючого Beauty Clinic"""

    def __init__(self):
        self.__clients: List[Client] = []
        self.__orders: List[Order] = []
        self.__next_client_id: int = 1
        self.__next_order_id: int = 1

    @property
    def clients_count(self) -> int:
        return len(self.__clients)

    @property
    def orders_count(self) -> int:
        return len(self.__orders)

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

            client = Client(self.__next_client_id, name, phone, email)
            self.__clients.append(client)
            self.__next_client_id += 1
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

    def delete_client(self) -> None:
        """Видалити клієнта"""
        try:
            if len(self.__clients) == 0:
                raise ValueError("No clients to delete")

            self.list_clients()
            raw = input("Enter client number to delete: ")
            if not raw.isdigit():
                raise ValueError("Please enter a number")

            index = int(raw) - 1
            if index < 0 or index >= len(self.__clients):
                raise ValueError("Client not found")

            removed = self.__clients.pop(index)
            print(f"Deleted: ID {removed.id} | {removed.name}")

        except ValueError as e:
            print(f"Помилка: {e}")

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

            service = input("Service (e.g. Facial Cleaning): ").strip()
            master = input("Master (e.g. Anna): ").strip()
            date = input("Date (YYYY-MM-DD): ").strip()

            try:
                total_price = float(input("Total price (UAH): ").strip())
                if total_price < 0:
                    raise InvalidPriceError("Price cannot be negative")
            except ValueError:
                raise InvalidPriceError("Invalid price format")

            # Валідація статусу
            status_input = input(
                "Status (Scheduled/In Progress/Done/Cancelled): ").strip()
            valid_statuses = ["Scheduled", "In Progress", "Done", "Cancelled"]
            if status_input not in valid_statuses:
                raise ValueError(
                    f"Invalid status. Must be one of: {valid_statuses}")

            order = Order(
                self.__next_order_id,
                client_name, service, master, status_input, date, total_price
            )
            self.__orders.append(order)
            self.__next_order_id += 1
            print(f"Order created with ID: {order.id}!")

        except (ValueError, ClientNotFoundError, InvalidPriceError) as e:
            print(f"Помилка: {e}")

    def update_status(self) -> None:
        """Оновити статус замовлення"""
        try:
            if len(self.__orders) == 0:
                raise ValueError("No orders yet")

            self.list_orders()
            raw = input("Enter order number to update status: ")
            if not raw.isdigit():
                raise ValueError("Please enter a number")

            index = int(raw) - 1
            if index < 0 or index >= len(self.__orders):
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
                self.__orders[index].status = status_map[status_choice]
                print(f"Status changed to {status_map[status_choice]}")
            else:
                raise ValueError("Invalid choice")

        except ValueError as e:
            print(f"Помилка: {e}")

    def delete_order(self) -> None:
        """Видалити замовлення"""
        try:
            if len(self.__orders) == 0:
                raise ValueError("Nothing to delete")

            self.list_orders()
            raw = input("Enter order number to delete: ")
            if not raw.isdigit():
                raise ValueError("Please enter a number")

            index = int(raw) - 1
            if index < 0 or index >= len(self.__orders):
                raise ValueError("Order not found")

            removed = self.__orders.pop(index)
            print(
                f"Deleted: ID {removed.id} | {removed.client} — {removed.service}")

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
        """Збереження даних в JSON"""
        try:
            clients_data = [client.to_dict() for client in self.__clients]
            orders_data = [order.to_dict() for order in self.__orders]

            with open("clients.json", "w") as file:
                json.dump(clients_data, file, indent=2)
            with open("orders.json", "w") as file:
                json.dump(orders_data, file, indent=2)

            print("Data saved to JSON files")

        except Exception as e:
            print(f"Помилка при збереженні: {e}")

    def load_data(self) -> None:
        """Завантаження даних з JSON"""
        try:
            with open("clients.json", "r") as file:
                clients_data = json.load(file)
                self.__clients = []
                for client_data in clients_data:
                    client = Client(
                        client_data["id"],
                        client_data["name"],
                        client_data["phone"],
                        client_data["email"]
                    )
                    self.__clients.append(client)

                    if self.__clients:
                        self.__next_client_id = max(
                            client.id for client in self.__clients) + 1
        except FileNotFoundError:
            self.__clients = []
            self.__next_client_id = 1
        except Exception as e:
            print(f"Помилка при завантаженні клієнтів: {e}")
            self.__clients = []
            self.__next_client_id = 1

        try:
            with open("orders.json", "r") as file:
                orders_data = json.load(file)
                self.__orders = []
                for order_data in orders_data:
                    order = Order(
                        order_data["id"],
                        order_data["client"],
                        order_data["procedure"],
                        order_data["master"],
                        order_data["status"],
                        order_data["date"],
                        order_data["total_price"]
                    )
                    self.__orders.append(order)

                    if self.__orders:
                        self.__next_order_id = max(
                            order.id for order in self.__orders) + 1
        except FileNotFoundError:
            self.__orders = []
            self.__next_order_id = 1
        except Exception as e:
            print(f"Помилка при завантаженні замовлень: {e}")
            self.__orders = []
            self.__next_order_id = 1
