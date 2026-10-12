import psycopg
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


def execute_sql_file(filename):
    dsn = os.getenv("DATABASE_URL")
    script_dir = Path(__file__).parent
    file_path = script_dir / filename

    with open(file_path, 'r', encoding='utf-8') as f:
        sql = f.read()

    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            conn.commit()
    print(f"Виконано: {filename}")


if __name__ == "__main__":
    # Порядок виконання
    execute_sql_file("project_dml.sql")
    execute_sql_file("project_search.sql")
    execute_sql_file("project_update_delete.sql")
    execute_sql_file("project_indexes.sql")
    print("Всі завдання проєкту виконано!")
