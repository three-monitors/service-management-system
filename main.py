import json
import csv
import re
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from functools import wraps


# Додано абстрактний базовий клас для всіх сутностей
class BaseEntity(ABC):
    """Абстрактний базовий клас для всіх сутностей"""
    
    def __init__(self, id: int):
        self._id = id  # protected атрибут
    
    @property
    def id(self) -> int:
        """Геттер для ID"""
        return self._id
    
    @abstractmethod
    def __str__(self) -> str:
        """Абстрактний метод — кожна сутність має описувати себе"""
        pass
    
    @abstractmethod
    def to_dict(self) -> Dict:
        """Абстрактний метод — конвертація в словник для JSON"""
        pass


# Додано інкапсуляцію та typing в клас Client
class Client(BaseEntity):
    """Клас клієнта Beauty Clinic з інкапсуляцією"""

    def __init__(self, id: int, name: str, phone: str, email: str):
        super().__init__(id)
        self.__name = name  # private атрибут
        self.__phone = phone  # private атрибут
        self.__email = email  # private атрибут
    
    @property
    def name(self) -> str:
        """Геттер для імені"""
        return self.__name
    
    @name.setter
    def name(self, value: str):
        """Сеттер для імені з валідацією"""
        if not value.strip():
            raise ValueError("Name cannot be empty")
        self.__name = value
    
    @property
    def phone(self) -> str:
        """Геттер для телефону"""
        return self.__phone
    
    @phone.setter
    def phone(self, value: str):
        """Сеттер для телефону з валідацією"""
        if not re.fullmatch(r"\+\d{3}-\d{2}-\d{3}-\d{2}-\d{2}", value):
            raise ValueError("Invalid phone format. Use +380-XX-XXX-XX-XX")
        self.__phone = value
    
    @property
    def email(self) -> str:
        """Геттер для email"""
        return self.__email
    
    @email.setter
    def email(self, value: str):
        """Сеттер для email з валідацією"""
        if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", value):
            raise ValueError("Invalid email format")
        
        banned_domains = [".ru", ".su", ".рф"]
        email_lower = value.lower()
        for domain in banned_domains:
            if email_lower.endswith(domain):
                raise ValueError(f"The use of email with the {domain} domain is prohibited")
        self.__email = value
    
    def __str__(self) -> str:
        """Опис клієнта"""
        return f"Client: {self.__name} | Phone: {self.__phone} | Email: {self.__email}"
    
    def to_dict(self) -> Dict:
        """Конвертація в словник для JSON"""
        return {
            "id": self._id,
            "name": self.__name,
            "phone": self.__phone,
            "email": self.__email
        }


# Додано інкапсуляцію та typing в клас Appointment
class Appointment(BaseEntity):
    """Клас запису на процедуру з інкапсуляцією"""

    def __init__(self, id: int, client: str, procedure: str, master: str, 
                 status: str, date: str, total_price: float):
        super().__init__(id)
        self.__client = client  # private атрибут
        self.__procedure = procedure  # private атрибут
        self.__master = master  # private атрибут
        self.__status = status  # private атрибут
        self.__date = date  # private атрибут
        self.__total_price = total_price  # private атрибут
    
    @property
    def client(self) -> str:
        """Геттер для клієнта"""
        return self.__client
    
    @client.setter
    def client(self, value: str):
        """Сеттер для клієнта"""
        if not value.strip():
            raise ValueError("Client name cannot be empty")
        self.__client = value
    
    @property
    def procedure(self) -> str:
        """Геттер для процедури"""
        return self.__procedure
    
    @procedure.setter
    def procedure(self, value: str):
        """Сеттер для процедури"""
        if not value.strip():
            raise ValueError("Procedure cannot be empty")
        self.__procedure = value
    
    @property
    def master(self) -> str:
        """Геттер для майстра"""
        return self.__master
    
    @master.setter
    def master(self, value: str):
        """Сеттер для майстра"""
        if not value.strip():
            raise ValueError("Master name cannot be empty")
        self.__master = value
    
    @property
    def status(self) -> str:
        """Геттер для статусу"""
        return self.__status
    
    @status.setter
    def status(self, value: str):
        """Сеттер для статусу з валідацією"""
        valid_statuses = ["Scheduled", "In Progress", "Done", "Cancelled"]
        if value not in valid_statuses:
            raise ValueError(f"Invalid status. Must be one of: {valid_statuses}")
        self.__status = value
    
    @property
    def date(self) -> str:
        """Геттер для дати"""
        return self.__date
    
    @date.setter
    def date(self, value: str):
        """Сеттер для дати з валідацією"""
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        self.__date = value
    
    @property
    def total_price(self) -> float:
        """Геттер для ціни"""
        return self.__total_price
    
    @total_price.setter
    def total_price(self, value: float):
        """Сеттер для ціни з валідацією"""
        if value < 0:
            raise ValueError("Price cannot be negative")
        self.__total_price = value
    
    def __str__(self) -> str:
        """Опис запису"""
        return f"{self.__client} | {self.__procedure} | {self.__master} | {self.__status} | {self.__date} | {self.__total_price} грн."
    
    def to_dict(self) -> Dict:
        """Конвертація в словник для JSON"""
        return {
            "id": self._id,
            "client": self.__client,
            "procedure": self.__procedure,
            "master": self.__master,
            "status": self.__status,
            "date": self.__date,
            "total_price": self.__total_price
        }


# Додано decorator для логування
def log_action(func):
    """Decorator для логування дій"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"🔄 Виконується: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            print(f"✅ Завершено: {func.__name__}")
            return result
        except Exception as e:
            print(f"❌ Помилка в {func.__name__}: {e}")
            raise
    return wrapper


# Додано інкапсуляцію, typing та обробку виключень в ServiceManager
class ServiceManager:
    """Клас керуючого Beauty Clinic з інкапсуляцією"""

    def __init__(self):
        self.__clients: List[Client] = []  # private атрибут з typing
        self.__appointments: List[Appointment] = []  # private атрибут з typing
        self.__next_client_id: int = 1  # private для генерації ID
        self.__next_appointment_id: int = 1  # private для генерації ID
    
    @property
    def clients_count(self) -> int:
        """Геттер для кількості клієнтів"""
        return len(self.__clients)
    
    @property
    def appointments_count(self) -> int:
        """Геттер для кількості записів"""
        return len(self.__appointments)
    
    @log_action
    def add_client(self) -> None:
        """Додати клієнта з обробкою виключень"""
        try:
            name = input("Client name: ").strip()
            if name == "":
                raise ValueError("Name cannot be empty")

            # Перевірка на дублікати
            for client in self.__clients:  # валідація
                if client.name == name:
                    raise ValueError("Client already exists")

            # Валідація телефону
            phone = input("Phone (format: +380-XX-XXX-XX-XX): ").strip()
            if not re.fullmatch(r"\+\d{3}-\d{2}-\d{3}-\d{2}-\d{2}", phone):
                raise ValueError("Invalid phone format. Use +380-XX-XXX-XX-XX")

            # Валідація email
            email = input("Email: ").strip()
            if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email):
                raise ValueError("Invalid email format")

            # Заборона доменів .ru, .su, .рф
            banned_domains = [".ru", ".su", ".рф"]
            email_lower = email.lower()
            for domain in banned_domains:
                if email_lower.endswith(domain):
                    raise ValueError(f"The use of email with the {domain} domain is prohibited")

            client = Client(self.__next_client_id, name, phone, email)
            self.__clients.append(client)
            self.__next_client_id += 1
            print(f"Client '{name}' added with ID: {client.id}")
        
        except ValueError as e:
            print(f"Помилка: {e}")
        except Exception as e:
            print(f"Непередбачена помилка: {e}")
    
    @log_action
    def create_appointment(self) -> None:
        """Створити запис з обробкою виключень"""
        try:
            if len(self.__clients) == 0:
                raise ValueError("No clients yet. Add a client first.")
            
            print("Clients:", [client.name for client in self.__clients])
            client_name = input("Client name: ").strip()

            # Знайти клієнта за іменем
            client = None
            for c in self.__clients:
                if c.name == client_name:
                    client = c
                    break

            if client is None:
                raise ValueError("Client not found")

            procedure = input("Procedure (e.g. Facial Cleaning): ").strip()
            master = input("Master (e.g. Anna): ").strip()
            date = input("Date (YYYY-MM-DD): ").strip()

            try:
                total_price = float(input("Total price (UAH): ").strip())
            except ValueError:
                raise ValueError("Invalid price format")

            appointment = Appointment(
                self.__next_appointment_id,
                client_name, procedure, master, "Scheduled", date, total_price
            )
            self.__appointments.append(appointment)
            self.__next_appointment_id += 1
            print(f"Appointment created with ID: {appointment.id}!")
        
        except ValueError as e:
            print(f"Помилка: {e}")
        except Exception as e:
            print(f"Непередбачена помилка: {e}")
    
    @log_action
    def show_appointments(self) -> None:
        """Показати записи"""
        if len(self.__appointments) == 0:
            print("No appointments yet")
            return

        print("\n--- Appointments ---")
        for i, appointment in enumerate(self.__appointments):
            print(f"{i + 1}. ID: {appointment.id} | {appointment}")
    
    @log_action
    def delete_appointment(self) -> None:
        """Видалити запис з обробкою виключень"""
        try:
            if len(self.__appointments) == 0:
                raise ValueError("Nothing to delete")

            self.show_appointments()
            raw = input("Enter appointment number to delete: ")
            if not raw.isdigit():
                raise ValueError("Please enter a number")

            index = int(raw) - 1
            if index < 0 or index >= len(self.__appointments):
                raise ValueError("Appointment not found")
            
            removed = self.__appointments.pop(index)
            print(f"Deleted: ID {removed.id} | {removed.client} — {removed.procedure}")
        
        except ValueError as e:
            print(f"Помилка: {e}")
        except Exception as e:
            print(f"Непередбачена помилка: {e}")
    
    @log_action
    def search_appointments(self) -> None:
        """Пошук записів"""
        if len(self.__appointments) == 0:
            print("No appointments yet")
            return

        client = input("Enter client name to search: ").strip()
        found = False

        for i, appointment in enumerate(self.__appointments):
            if appointment.client == client:
                print(f"{i + 1}. ID: {appointment.id} | {appointment}")
                found = True

        if not found:
            print(f"No appointments found for client '{client}'")
    
    @log_action
    def change_status(self) -> None:
        """Зміна статусу з обробкою виключень"""
        try:
            if len(self.__appointments) == 0:
                raise ValueError("No appointments yet")

            self.show_appointments()
            raw = input("Enter appointment number to change status: ")
            if not raw.isdigit():
                raise ValueError("Please enter a number")

            index = int(raw) - 1
            if index < 0 or index >= len(self.__appointments):
                raise ValueError("Appointment not found")

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
                self.__appointments[index].status = status_map[status_choice]
                print(f"Status changed to {status_map[status_choice]}")
            else:
                raise ValueError("Invalid choice")
        
        except ValueError as e:
            print(f"Помилка: {e}")
        except Exception as e:
            print(f"Непередбачена помилка: {e}")
    
    @log_action
    def export_to_csv(self) -> None:
        """Експорт в CSV з обробкою виключень"""
        try:
            if len(self.__appointments) == 0:
                raise ValueError("No appointments to export")

            with open("appointments.csv", "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["ID", "Client", "Procedure", "Master",
                                "Status", "Date", "Price"])
                for appointment in self.__appointments:
                    writer.writerow([
                        appointment.id,
                        appointment.client,
                        appointment.procedure,
                        appointment.master,
                        appointment.status,
                        appointment.date,
                        appointment.total_price
                    ])
            print("Exported to appointments.csv")
        
        except ValueError as e:
            print(f"Помилка: {e}")
        except Exception as e:
            print(f"Непередбачена помилка: {e}")
    
    @log_action
    def save_data(self) -> None:
        """Збереження даних в JSON з обробкою виключень"""
        try:
            # Використовуємо to_dict() метод для конвертації
            clients_data = [client.to_dict() for client in self.__clients]
            appointments_data = [appointment.to_dict() for appointment in self.__appointments]

            with open("clients.json", "w") as file:
                json.dump(clients_data, file, indent=2)
            with open("appointments.json", "w") as file:
                json.dump(appointments_data, file, indent=2)
            
            print("Data saved to JSON files")
        
        except Exception as e:
            print(f"Помилка при збереженні: {e}")
    
    @log_action
    def load_data(self) -> None:
        """Завантаження даних з JSON з обробкою виключень"""
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
                
                # Оновлюємо next_client_id
                if self.__clients:
                    self.__next_client_id = max(client.id for client in self.__clients) + 1
        except FileNotFoundError:
            self.__clients = []
            self.__next_client_id = 1
        except Exception as e:
            print(f"Помилка при завантаженні клієнтів: {e}")
            self.__clients = []
            self.__next_client_id = 1

        try:
            with open("appointments.json", "r") as file:
                appointments_data = json.load(file)
                self.__appointments = []
                for appointment_data in appointments_data:
                    appointment = Appointment(
                        appointment_data.get("id", 0),
                        appointment_data.get("client", ""),
                        appointment_data.get("procedure", ""),
                        appointment_data.get("master", ""),
                        appointment_data.get("status", "Scheduled"),
                        appointment_data.get("date", "2026-08-21"),
                        appointment_data.get("total_price", 0)
                    )
                    self.__appointments.append(appointment)
                
                # Оновлюємо next_appointment_id
                if self.__appointments:
                    self.__next_appointment_id = max(appointment.id for appointment in self.__appointments) + 1
        except FileNotFoundError:
            self.__appointments = []
            self.__next_appointment_id = 1
        except Exception as e:
            print(f"Помилка при завантаженні записів: {e}")
            self.__appointments = []
            self.__next_appointment_id = 1


def main():
    """Головна функція програми"""
    try:
        manager = ServiceManager()
        manager.load_data()  # завантаження даних при старті

        while True:
            print("\n1. Add client")
            print("2. Create appointment")
            print("3. Show appointments")
            print("4. Delete appointment")
            print("5. Search appointments")
            print("6. Change status")
            print("7. Export to CSV")  # експорт в CSV
            print("8. Exit")
            print(f"--- Appointments: {manager.appointments_count} ---")  # лічильник записів
            print(f"--- Clients: {manager.clients_count} ---")  # лічильник клієнтів

            choice = input("Choose: ")

            if choice == "1":
                manager.add_client()
            elif choice == "2":
                manager.create_appointment()
            elif choice == "3":
                manager.show_appointments()
            elif choice == "4":
                manager.delete_appointment()
            elif choice == "5":
                manager.search_appointments()
            elif choice == "6":
                manager.change_status()
            elif choice == "7":
                manager.export_to_csv()  # експорт в CSV
            elif choice == "8":
                manager.save_data()  # збереження при виході
                print("Goodbye!")
                break
            else:
                print("Unknown option, try again")
    
    except Exception as e:
        print(f"Критична помилка: {e}")


if __name__ == "__main__":
    main()
