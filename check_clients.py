from database import get_connection


def check_clients():
    conn = get_connection()
    cursor = conn.cursor()

    # Перевіряємо фактичну кількість клієнтів
    cursor.execute("SELECT COUNT(*) as count FROM clients")
    count = cursor.fetchone()['count']
    print(f"Фактична кількість клієнтів: {count}")

    # Перевіряємо клієнтів
    cursor.execute("SELECT * FROM clients")
    clients = cursor.fetchall()
    print("\nСписок клієнтів:")
    for client in clients:
        print(f"ID: {client['id']}, Name: {client['name']}")

    # Перевіряємо sqlite_sequence
    cursor.execute("SELECT * FROM sqlite_sequence WHERE name='clients'")
    seq = cursor.fetchone()
    if seq:
        print(f"\nsqlite_sequence для clients: {seq['seq']}")
    else:
        print("\nsqlite_sequence для clients не знайдено")

    conn.close()


if __name__ == "__main__":
    check_clients()
