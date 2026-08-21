# Функція: додати клієнта
def add_client(clients):
    name = input("Client name: ").strip()
    if name == "":
        print("Name cannot be empty")
        return
    if name in clients:  # валідація
        print("Client already exists")
        return
    clients.append(name)
    print(f"Client '{name}' added")

# Функція: створити запис
def create_appointment(clients, appointments):
    if len(clients) == 0:
        print("No clients yet. Add a client first.")
        return
    print("Clients:", clients)
    client = input("Client name: ").strip()
    if client not in clients:
        print("Client not found")
        return
    procedure = input("Procedure (e.g. Facial Cleaning): ").strip()
    master = input("Master (e.g. Anna): ").strip()
    appointment = {
        "client": client,
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
        print(f"{i + 1}. {appointments[i]['client']} | {appointments[i]['procedure']} | {appointments[i]['status']}")

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
            print(f"{i + 1}. {appointments[i]['client']} | {appointments[i]['procedure']} | {appointments[i]['master']} | {appointments[i]['status']}")
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

# Точка входу
def main():
    clients = []
    appointments = []
    while True:
        print("\n1. Add client")
        print("2. Create appointment")
        print("3. Show appointments")
        print("4. Delete appointment")
        print("5. Search appointments")
        print("6. Change status")
        print("7. Exit")
        print(f"--- Appointments: {len(appointments)} ---") # лічильник
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
            print("Goodbye!"); break
        else:
            print("Unknown option, try again")

main()
