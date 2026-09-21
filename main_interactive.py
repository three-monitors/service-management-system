from managers.service_manager import ServiceManager
from exceptions import InvalidMenuChoiceError
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)


def main():
    """Головна функція програми"""
    try:
        manager = ServiceManager()
        manager.load_data()

        while True:
            print("\n1. Add client")
            print("2. List clients")
            print("3. Delete client")
            print("4. Create order")
            print("5. List orders")
            print("6. Update status")
            print("7. Delete order")
            print("8. Exit")
            print(f"--- Orders: {manager.orders_count} ---")
            print(f"--- Clients: {manager.clients_count} ---")

            choice = input("Choose: ")

            if choice == "1":
                manager.add_client()
                manager.save_data()  # автоматичне збереження
            elif choice == "2":
                manager.list_clients()
            elif choice == "3":
                manager.delete_client()
                manager.save_data()  # автоматичне збереження
            elif choice == "4":
                manager.create_order()
                manager.save_data()  # автоматичне збереження
            elif choice == "5":
                manager.list_orders()
            elif choice == "6":
                manager.update_status()
                manager.save_data()  # автоматичне збереження
            elif choice == "7":
                manager.delete_order()
                manager.save_data()  # автоматичне збереження
            elif choice == "8":
                manager.save_data()
                print("Goodbye!")
                break
            else:
                raise InvalidMenuChoiceError(f"Invalid menu choice: {choice}")

    except InvalidMenuChoiceError as e:
        print(f"Помилка меню: {e}")
    except Exception as e:
        print(f"Критична помилка: {e}")


if __name__ == "__main__":
    main()
