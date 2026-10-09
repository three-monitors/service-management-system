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
            cur.execute(sql)
            conn.commit()
    print(f"Виконано: {filename}")


if __name__ == "__main__":
    execute_sql_file("schema.sql")
    print("Таблиці створено успішно!")
