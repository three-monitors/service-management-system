import json
import csv
import re


class Client:
    """Клас клієнта Beauty Clinic"""

    def __init__(self, name, phone, email):
        self.name = name
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"Client: {self.name} | Phone: {self.phone} | Email: {self.email}"


class Appointment:
    """Клас запису на процедуру"""

    def __init__(self, client, procedure, master, status, date, total_price):
        self.client = client
        self.procedure = procedure
        self.master = master
        self.status = status
        self.date = date
        self.total_price = total_price

    def __str__(self):
        return f"{self.client} | {self.procedure} | {self.master} | {self.status} | {self.date} | {self.total_price} грн."


class ServiceManager:
    """Клас керуючого Beauty Clinic"""

    def __init__(self):
        self.clients = []
        self.appointments = []

    def add_client(self):
        """Додати клієнта"""
        name = input("Client name: ").strip()
        if name == "":
            print("Name cannot be empty")
            return

        # Перевірка на дублікати
        for client in self.clients:  # валідація
            if client.name == name:
                print("Client already exists")
                return

        # Валідація телефону
        phone = input("Phone (format: +380-XX-XXX-XX-XX): ").strip()
        if not re.fullmatch(r"\+\d{3}-\d{2}-\d{3}-\d{2}-\d{2}", phone):
            print("Invalid phone format. Use +380-XX-XXX-XX-XX")
            return

        # Валідація email
        email = input("Email: ").strip()
        if not re.fullmatch(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", email):
            print("Invalid email format")
            return

        # Заборона доменів .ru, .su, .рф
        banned_domains = [".ru", ".su", ".рф"]
        email_lower = email.lower()

        for domain in banned_domains:
            if email_lower.endswith(domain):
                print(
                    f"The use of email with the {domain} domain is prohibited")
                return

        client = Client(name, phone, email)
        self.clients.append(client)
        print(f"Client '{name}' added")

    def create_appointment(self):
        """Створити запис"""
        if len(self.clients) == 0:
            print("No clients yet. Add a client first.")
            return
        print("Clients:", [client.name for client in self.clients])
        client_name = input("Client name: ").strip()

        # Знайти клієнта за іменем
        client = None
        for c in self.clients:
            if c.name == client_name:
                client = c
                break

        if client is None:
            print("Client not found")
            return

        procedure = input("Procedure (e.g. Facial Cleaning): ").strip()
        master = input("Master (e.g. Anna): ").strip()
        date = input("Date (YYYY-MM-DD): ").strip()

        try:
            total_price = float(input("Total price (UAH): ").strip())
        except ValueError:
            print("Invalid price format")
            return

        appointment = Appointment(
            client_name, procedure, master, "Scheduled", date, total_price)
        self.appointments.append(appointment)
        print("Appointment created!")

    def show_appointments(self):
        """Показати записи"""
        if len(self.appointments) == 0:
            print("No appointments yet")
            return

        print("\n--- Appointments ---")
        for i, appointment in enumerate(self.appointments):
            print(f"{i + 1}. {appointment.client} | {appointment.procedure} | {appointment.master} | {appointment.status} | {appointment.date} | {appointment.total_price} грн.")

    def delete_appointment(self):
        """Видалити запис"""
        if len(self.appointments) == 0:
            print("Nothing to delete")
            return

        self.show_appointments()
        raw = input("Enter appointment number to delete: ")
        if not raw.isdigit():
            print("Please enter a number")
            return

        index = int(raw) - 1
        if index < 0 or index >= len(self.appointments):
            print("Appointment not found")
            return
        removed = self.appointments.pop(index)
        print(f"Deleted: {removed.client} — {removed.procedure}")

    def search_appointments(self):
        """Пошук записів"""
        if len(self.appointments) == 0:
            print("No appointments yet")
            return

        client = input("Enter client name to search: ").strip()
        found = False

        for i, appointment in enumerate(self.appointments):
            if appointment.client == client:
                print(f"{i + 1}. {appointment.client} | {appointment.procedure} | {appointment.master} | {appointment.status} | {appointment.date} | {appointment.total_price} грн.")
                found = True

        if not found:
            print(f"No appointments found for client '{client}'")

    def change_status(self):
        """Зміна статусу"""
        if len(self.appointments) == 0:
            print("No appointments yet")
            return

        self.show_appointments()
        raw = input("Enter appointment number to change status: ")
        if not raw.isdigit():
            print("Please enter a number")
            return

        index = int(raw) - 1
        if index < 0 or index >= len(self.appointments):
            print("Appointment not found")
            return

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
            self.appointments[index].status = status_map[status_choice]
            print(f"Status changed to {status_map[status_choice]}")
        else:
            print("Invalid choice")

    def export_to_csv(self):
        """Експорт в CSV"""
        if len(self.appointments) == 0:
            print("No appointments to export")
            return

        with open("appointments.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Client", "Procedure", "Master",
                            "Status", "Date", "Price"])
            for appointment in self.appointments:
                writer.writerow([
                    appointment.client,
                    appointment.procedure,
                    appointment.master,
                    appointment.status,
                    appointment.date,
                    appointment.total_price
                ])
        print("Exported to appointments.csv")

    def save_data(self):
        """Збереження даних в JSON"""
        # конвертація об'єктів в словники для JSON
        clients_data = []
        for client in self.clients:
            clients_data.append({
                "name": client.name,
                "phone": client.phone,
                "email": client.email
            })

        appointments_data = []
        for appointment in self.appointments:
            appointments_data.append({
                "client": appointment.client,
                "procedure": appointment.procedure,
                "master": appointment.master,
                "status": appointment.status,
                "date": appointment.date,
                "total_price": appointment.total_price
            })

        with open("clients.json", "w") as file:
            json.dump(clients_data, file)
        with open("appointments.json", "w") as file:
            json.dump(appointments_data, file)
        print("Data saved to JSON files")

    def load_data(self):
        """Завантаження даних з JSON"""
        try:
            with open("clients.json", "r") as file:
                clients_data = json.load(file)
                self.clients = []
                for client_data in clients_data:
                    client = Client(client_data["name"], client_data["phone"], client_data["email"])
                    self.clients.append(client)
        except FileNotFoundError:
            self.clients = []

        try:
            with open("appointments.json", "r") as file:
                appointments_data = json.load(file)
                self.appointments = []
                for appointment_data in appointments_data:
                    client = appointment_data.get("client", "")
                    procedure = appointment_data.get("procedure", "")
                    master = appointment_data.get("master", "")
                    status = appointment_data.get("status", "Scheduled")
                    date = appointment_data.get("date", "2026-08-21")
                    total_price = appointment_data.get("total_price", 0)

                    appointment = Appointment(client, procedure, master, status, date, total_price)
                    self.appointments.append(appointment)
        except FileNotFoundError:
            self.appointments = []


def main():
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
        print(f"--- Appointments: {len(manager.appointments)} ---")  # лічильник записів
        print(f"--- Clients: {len(manager.clients)} ---")  # лічильник клієнтів

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


if __name__ == "__main__":
    main()
