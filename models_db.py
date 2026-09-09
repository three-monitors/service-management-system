import sqlite3
from database import get_connection
from typing import List, Dict, Optional


def add_client(name: str, phone: str, email: str) -> int:
    """Додає клієнта, повертає його ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO clients (name, phone, email) VALUES (?, ?, ?)",
        (name, phone, email)
    )
    conn.commit()
    client_id = cursor.lastrowid
    conn.close()
    return client_id


def add_service(name: str, price: float, duration: int) -> int:
    """Додає послугу, повертає її ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO services (name, price, duration) VALUES (?, ?, ?)",
        (name, price, duration)
    )
    conn.commit()
    service_id = cursor.lastrowid
    conn.close()
    return service_id


def create_order(client_id: int, service_id: int) -> int:
    """Створює замовлення, повертає його ID"""
    conn = get_connection()
    cursor = conn.cursor()

    # Отримуємо ціну послуги
    cursor.execute("SELECT price FROM services WHERE id = ?", (service_id,))
    service = cursor.fetchone()
    if not service:
        conn.close()
        raise ValueError("Послуга не знайдена")

    total_price = service["price"]

    cursor.execute(
        """INSERT INTO orders (client_id, service_id, status, total_price) 
           VALUES (?, ?, 'Created', ?)""",
        (client_id, service_id, total_price)
    )
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    return order_id


def get_all_orders() -> List[Dict]:
    """Отримує всі замовлення"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM orders")
    orders = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return orders


def get_orders_with_details() -> List[Dict]:
    """Отримує замовлення з іменами клієнтів та назвами послуг (JOIN)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, c.name as client_name, s.name as service_name, 
               o.total_price, o.status, o.created_at
        FROM orders o
        JOIN clients c ON o.client_id = c.id
        JOIN services s ON o.service_id = s.id
        ORDER BY o.id
    """)
    orders = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return orders


def update_order_status(order_id: int, new_status: str) -> bool:
    """Оновлює статус замовлення"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE orders SET status = ? WHERE id = ?",
        (new_status, order_id)
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    return affected > 0


def add_inventory_item(name: str, quantity: int, price: float) -> int:
    """Додає товар на склад, повертає його ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)",
        (name, quantity, price)
    )
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return item_id


def get_low_stock_items(threshold: int) -> List[Dict]:
    """Отримує товари з кількістю менше за threshold"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM inventory WHERE quantity < ?",
        (threshold,)
    )
    items = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return items


# Бонусна функція
def get_client_history(client_id: int) -> List[Dict]:
    """Отримує історію замовлень клієнта з назвами послуг"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, s.name as service_name, o.total_price, 
               o.status, o.created_at
        FROM orders o
        JOIN services s ON o.service_id = s.id
        WHERE o.client_id = ?
        ORDER BY o.created_at DESC
    """, (client_id,))
    history = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return history
