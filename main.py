# Функція: додати клієнта
def add_client(clients):
    name = input("Client name: ").strip()
    if name == "":
        print("Name cannot be empty")
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
    appointment = {
        "client": client,
        "procedure": procedure,
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

# Точка входу
def main():
    clients = []
    appointments = []
    while True:
        print("\n1. Add client")
        print("2. Create appointment")
        print("3. Show appointments")
        print("4. Delete")
        print("5. Exit")
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
            print("Goodbye!"); break
        else:
            print("Unknown option, try again")

main()