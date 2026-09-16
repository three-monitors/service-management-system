import json
import os
from database import init_db, get_connection
from models_db import add_client, add_service, create_order, update_order_status
from storage import load_clients, load_orders, load_services

def get_next_client_id():
    """Отримує наступний ID для клієнтів"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) as max_id FROM clients")
    result = cursor.fetchone()
    conn.close()
    return (result['max_id'] or 0) + 1

def get_next_service_id():
    """Отримує наступний ID для послуг"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) as max_id FROM services")
    result = cursor.fetchone()
    conn.close()
    return (result['max_id'] or 0) + 1

def get_next_order_id():
    """Отримує наступний ID для замовлень"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(id) as max_id FROM orders")
    result = cursor.fetchone()
    conn.close()
    return (result['max_id'] or 0) + 1

def migrate_json_to_db():
    """Міграція даних з JSON файлів в базу даних"""
    print("=== Міграція даних з JSON в базу даних ===")
    
    # Ініціалізуємо базу даних
    init_db()
    
    # Отримуємо поточні максимальні ID
    next_client_id = get_next_client_id()
    next_service_id = get_next_service_id()
    next_order_id = get_next_order_id()
    
    print(f"Наступний ID для клієнтів: {next_client_id}")
    print(f"Наступний ID для послуг: {next_service_id}")
    print(f"Наступний ID для замовлень: {next_order_id}")
    
    # Визначаємо шлях до файлів
    current_dir = os.path.dirname(os.path.abspath(__file__))
    clients_file = os.path.join(current_dir, "clients.json")
    orders_file = os.path.join(current_dir, "orders.json")
    services_file = os.path.join(current_dir, "services.json")
    
    # Завантажуємо дані з JSON
    try:
        clients = load_clients(clients_file)
        orders = load_orders(orders_file)
        services = load_services(services_file)
    except Exception as e:
        print(f"Помилка при завантаженні JSON: {e}")
        clients = []
        orders = []
        services = []
    
    print(f"Знайдено клієнтів в JSON: {len(clients)}")
    print(f"Знайдено замовлень в JSON: {len(orders)}")
    print(f"Знайдено послуг в JSON: {len(services)}")
    
    # Міграція клієнтів з новими ID
    client_id_map = {}  # JSON ID -> DB ID
    current_client_id = next_client_id
    for client in clients:
        # Вставляємо з конкретним ID замість AUTOINCREMENT
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO clients (id, name, phone, email) VALUES (?, ?, ?, ?)",
            (current_client_id, client.name, client.phone, client.email)
        )
        conn.commit()
        conn.close()
        
        client_id_map[client.id] = current_client_id
        print(f"Клієнт {client.name} доданий (ID: {current_client_id})")
        current_client_id += 1
    
    # Міграція послуг з новими ID
    service_id_map = {}  # JSON ID -> DB ID
    current_service_id = next_service_id
    for service in services:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO services (id, name, price, duration) VALUES (?, ?, ?, ?)",
            (current_service_id, service.name, service.price, service.duration)
        )
        conn.commit()
        conn.close()
        
        service_id_map[service.id] = current_service_id
        print(f"Послуга {service.name} додана (ID: {current_service_id})")
        current_service_id += 1
    
    # Міграція замовлень з новими ID
    current_order_id = next_order_id
    for order in orders:
        # Знаходимо відповідні ID в базі даних
        if order.client in client_id_map and order.procedure in service_id_map:
            client_db_id = client_id_map[order.client]
            service_db_id = service_id_map[order.procedure]
            
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO orders (id, client_id, service_id, status, total_price) 
                   VALUES (?, ?, ?, ?, ?)""",
                (current_order_id, client_db_id, service_db_id, order.status, order.total_price)
            )
            conn.commit()
            conn.close()
            
            print(f"Замовлення {order.client} - {order.procedure} додане (ID: {current_order_id})")
            current_order_id += 1
        else:
            print(f"Пропущено замовлення: клієнт або послуга не знайдені")
    
    print("=== Міграція завершена ===")

if __name__ == "__main__":
    migrate_json_to_db()
