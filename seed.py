from database import init_db
from models_db import (
    add_client, add_service, create_order,
    get_orders_with_details, update_order_status,
    add_inventory_item, get_low_stock_items, get_client_history
)


def main():
    """Заповнює базу даних тестовими даними"""
    print("=== Ініціалізація бази даних ===")
    init_db()

    print("\n=== Додавання клієнтів ===")
    client1_id = add_client(
        "Іваненко Олег", "+380-50-123-45-67", "ivanenko@example.com")
    client2_id = add_client(
        "Петренко Марія", "+380-50-987-65-43", "petrenko@example.com")
    client3_id = add_client(
        "Коваль Андрій", "+380-50-456-78-90", "koval@example.com")
    print(f"Клієнти додані: {client1_id}, {client2_id}, {client3_id}")

    print("\n=== Додавання послуг ===")
    service1_id = add_service("Очищення обличчя", 850.00, 30)  # Oil Change
    service2_id = add_service("Пілінг", 400.00, 20)  # Tire Rotation
    service3_id = add_service("Масаж", 600.00, 45)  # Brake Check
    service4_id = add_service("Консультація", 1200.00, 60)
    print(
        f"Послуги додані: {service1_id}, {service2_id}, {service3_id}, {service4_id}")

    print("\n=== Створення замовлень ===")
    order1_id = create_order(client1_id, service1_id)
    order2_id = create_order(client2_id, service2_id)
    order3_id = create_order(client3_id, service3_id)
    order4_id = create_order(client1_id, service4_id)
    order5_id = create_order(client2_id, service1_id)
    print(
        f"Замовлення створені: {order1_id}, {order2_id}, {order3_id}, {order4_id}, {order5_id}")

    print("\n=== Оновлення статусів ===")
    update_order_status(order1_id, "Done")
    update_order_status(order2_id, "In Progress")
    update_order_status(order3_id, "Created")
    update_order_status(order4_id, "Scheduled")
    update_order_status(order5_id, "In Progress")
    print("Статуси оновлені")

    print("\n=== Додавання товарів на склад ===")
    item1_id = add_inventory_item(
        "Крем для обличчя", 2, 450.00)  # Моторна олива 5W-30
    item2_id = add_inventory_item(
        "Олія для масажу", 1, 800.00)  # Гальмівні колодки
    item3_id = add_inventory_item("Маска для обличчя", 10, 150.00)
    item4_id = add_inventory_item("Міцелярна вода", 5, 200.00)
    print(f"Товари додані: {item1_id}, {item2_id}, {item3_id}, {item4_id}")

    print("\n=== Замовлення ===")
    orders = get_orders_with_details()
    for order in orders:
        print(f"[{order['id']}] {order['client_name']:20} | {order['service_name']:20} | {order['total_price']:8.2f} | {order['status']}")

    print("\n=== Мало на складі (< 3 шт.) ===")
    low_stock = get_low_stock_items(3)
    for item in low_stock:
        print(f"{item['name']:20} : {item['quantity']} шт.")

    print("\n=== Бонус: Історія клієнта Іваненко Олег ===")
    history = get_client_history(client1_id)
    for record in history:
        print(f"[{record['id']}] {record['service_name']:20} | {record['total_price']:8.2f} | {record['status']} | {record['created_at']}")


if __name__ == "__main__":
    main()
