import json
import csv
import re

# Функція: додати клієнта
def add_client(clients):
    name = input("Client name: ").strip()
    if name == "":
        print("Name cannot be empty")
        return
    if name in clients:  # валідація
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
            print(f"The use of email with the {domain} domain is prohibited")
            return

    client = {
        "name": name,
        "phone": phone,
        "email": email
    }
    clients.append(client)
    print(f"Client '{name}' added")

# Функція: створити запис
def create_appointment(clients, appointments):
    if len(clients) == 0:
        print("No clients yet. Add a client first.")
        return
    print("Clients:", [client["name"] for client in clients])
    client_name = input("Client name: ").strip()

    # Знайти клієнта за іменем
    client = None
    for c in clients:
        if c["name"] == client_name:
            client = c
            break

    if client is None:
        print("Client not found")
        return
    procedure = input("Procedure (e.g. Facial Cleaning): ").strip()
    master = input("Master (e.g. Anna): ").strip()
    appointment = {
        "client": client_name,
        "procedure": procedure,
        "master": master,
        "status": "Scheduled"
    }
    appointments.append(appointment)
    print("Appointment created!")

# Функція: показати записи
def show_appointments(appointments):
    if len(appointments) == 0:
        print("No appointments yet")
        return
    print("\n--- Appointments ---")
    for i in range(len(appointments)):
        print(
            f"{i + 1}. {appointments[i]['client']} | {appointments[i]['procedure']} | {appointments[i]['master']} | {appointments[i]['status']}")

# Функція: видалити запис
def delete_appointment(appointments):
    if len(appointments) == 0:
        print("Nothing to delete")
        return
    show_appointments(appointments)
    raw = input("Enter appointment number to delete: ")
    if not raw.isdigit():
        print("Please enter a number")
        return
    index = int(raw) - 1
    if index < 0 or index >= len(appointments):
        print("Appointment not found")
        return
    removed = appointments.pop(index)
    print(f"Deleted: {removed['client']} — {removed['procedure']}")

# Функція: пошук
def search_appointments(appointments):
    if len(appointments) == 0:
        print("No appointments yet")
        return
    client = input("Enter client name to search: ").strip()
    found = False
    for i in range(len(appointments)):
        if appointments[i]['client'] == client:
            print(
                f"{i + 1}. {appointments[i]['client']} | {appointments[i]['procedure']} | {appointments[i]['master']} | {appointments[i]['status']}")
            found = True
    if not found:
        print(f"No appointments found for client '{client}'")

# Функція: зміна статусу
def change_status(appointments):
    if len(appointments) == 0:
        print("No appointments yet")
        return
    show_appointments(appointments)
    raw = input("Enter appointment number to change status: ")
    if not raw.isdigit():
        print("Please enter a number")
        return
    index = int(raw) - 1
    if index < 0 or index >= len(appointments):
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
        appointments[index]['status'] = status_map[status_choice]
        print(f"Status changed to {status_map[status_choice]}")
    else:
        print("Invalid choice")

# Функція: збереження даних
def save_data(clients, appointments):
    """Зберігає клієнтів та записи в JSON файли"""
    with open("clients.json", "w") as file:
        json.dump(clients, file)
    with open("appointments.json", "w") as file:
        json.dump(appointments, file)
    print("Data saved to JSON files")

# Функція: завантаження даних
def load_data():
    """Завантажує клієнтів та записи з JSON файлів"""
    try:
        with open("clients.json", "r") as file:
            clients = json.load(file)
    except FileNotFoundError:
        clients = []

    try:
        with open("appointments.json", "r") as file:
            appointments = json.load(file)
    except FileNotFoundError:
        appointments = []

    return clients, appointments

# Функція: експорт в CSV
def export_to_csv(appointments):
    """Експортує записи в CSV файл"""
    with open("appointments.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Client", "Procedure", "Master", "Status"])
        for appointment in appointments:
            writer.writerow([
                appointment["client"],
                appointment["procedure"],
                appointment["master"],
                appointment["status"]
            ])
    print("Exported to appointments.csv")

# Точка входу
def main():
    clients, appointments = load_data()  # завантаження даних при старті

    while True:
        print("\n1. Add client")
        print("2. Create appointment")
        print("3. Show appointments")
        print("4. Delete appointment")
        print("5. Search appointments")
        print("6. Change status")
        print("7. Export to CSV")  # експорт в CSV
        print("8. Exit")
        print(f"--- Appointments: {len(appointments)} ---")  # лічильник записів
        choice = input("Choose: ")
        if choice == "1":
            add_client(clients)
        elif choice == "2":
            create_appointment(clients, appointments)
        elif choice == "3":
            show_appointments(appointments)
        elif choice == "4":
            delete_appointment(appointments)
        elif choice == "5":
            search_appointments(appointments)
        elif choice == "6":
            change_status(appointments)
        elif choice == "7":
            export_to_csv(appointments)  # експорт в CSV
        elif choice == "8":
            save_data(clients, appointments)  # збереження при виході
            print("Goodbye!")
            break
        else:
            print("Unknown option, try again")


main()
