from database import get_connection


def reset_sequence():
    conn = get_connection()
    cursor = conn.cursor()

    # Отримуємо максимальний існуючий ID
    cursor.execute("SELECT MAX(id) as max_id FROM clients")
    result = cursor.fetchone()
    max_id = result['max_id'] if result['max_id'] else 0

    print(f"Максимальний існуючий ID: {max_id}")

    # Видаляємо запис з sqlite_sequence
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='clients'")

    # Якщо є клієнти, встановлюємо правильне значення
    if max_id > 0:
        cursor.execute(
            "INSERT INTO sqlite_sequence (name, seq) VALUES ('clients', ?)", (max_id,))
        print(f"sqlite_sequence встановлено на: {max_id}")
    else:
        print("sqlite_sequence видалено (немає клієнтів)")

    conn.commit()
    conn.close()
    print("AUTOINCREMENT скинуто")


if __name__ == "__main__":
    reset_sequence()
