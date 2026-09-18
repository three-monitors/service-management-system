from functools import reduce
from datetime import datetime, timedelta
from models_dataclass import Client, Service, Order, OrderStatus


def main():
    """Демонстрація функціональної обробки замовлень"""

    # Створюємо тестові дані
    client1 = Client("Іваненко Олег", "+380501234567", "ivanenko@example.com")
    client2 = Client("Петренко Марія", "+380509876543", "petrenko@example.com")
    client3 = Client("Коваль Андрій", "+380504567890", "koval@example.com")

    service1 = Service("Очищення обличчя", 850, 30)
    service2 = Service("Пілінг", 400, 20)
    service3 = Service("Масаж", 600, 45)
    service4 = Service("Консультація", 1200, 60)

    orders = [
        Order(client1, service1, OrderStatus.CREATED,
              datetime.now() - timedelta(days=3)),
        Order(client2, service2, OrderStatus.IN_PROGRESS,
              datetime.now() - timedelta(days=2)),
        Order(client3, service3, OrderStatus.COMPLETED,
              datetime.now() - timedelta(days=1)),
        Order(client1, service4, OrderStatus.COMPLETED,
              datetime.now() - timedelta(hours=12)),
        Order(client2, service1, OrderStatus.CREATED,
              datetime.now() - timedelta(hours=6)),
        Order(client3, service2, OrderStatus.CANCELLED,
              datetime.now() - timedelta(hours=3)),
    ]

    # 1. filter: лише активні замовлення
    active = list(filter(lambda o: o.is_active(), orders))
    print(f"Активних замовлень: {len(active)}")

    # 2. filter: лише завершені
    completed = list(filter(lambda o: o.status ==
                     OrderStatus.COMPLETED, orders))
    print(f"Завершених замовлень: {len(completed)}")

    # 3. map + reduce: загальна виручка по завершених
    total_revenue = reduce(lambda acc, o: acc +
                           o.total_price(), completed, 0.0)
    print(f"Загальна виручка: {total_revenue:.2f} грн.")

    # 4. map: список summary() для всіх активних
    active_summaries = list(map(lambda o: o.summary(), active))
    print("\nАктивні замовлення:")
    for summary in active_summaries:
        print(f"  {summary}")

    # 5. sorted: завершені за датою (найновіші першими)
    sorted_completed = sorted(
        completed, key=lambda o: o.created_at, reverse=True)
    print("\nЗавершені замовлення (від нових до старих):")
    for order in sorted_completed:
        print(f"  {order.summary()}")

    # 6. filter: замовлення конкретного клієнта
    client_name = "Іваненко Олег"
    client_orders = list(
        filter(lambda o: o.client.name == client_name, orders))
    print(f"\nЗамовлення клієнта {client_name}: {len(client_orders)}")
    for order in client_orders:
        print(f"  {order.summary()}")


if __name__ == "__main__":
    main()
