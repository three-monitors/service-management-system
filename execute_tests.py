import psycopg
import os
from dotenv import load_dotenv

load_dotenv()
DSN = os.getenv("DATABASE_URL")


def execute_sql_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        sql = f.read()

    with psycopg.connect(DSN) as conn:
        with conn.cursor() as cur:
            statements = sql.split(';')
            for stmt in statements:
                stmt = stmt.strip()
                if stmt:
                    try:
                        cur.execute(stmt)
                        conn.commit()
                        print(f"✅ Успішно: {stmt[:50]}...")
                    except psycopg.Error as e:
                        conn.rollback()
                        print(f"❌ Помилка (очікується): {e}")


if __name__ == "__main__":
    execute_sql_file("test_constraints.sql")
    print("Тестування обмежень завершено!")
