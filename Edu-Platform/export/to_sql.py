import os
from datetime import datetime

EXPORT_DIR = "exported_sql"
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_to_sql(data_dict, filename="export.sql"):
    """
    JSONga o'xshash dict orqali SQL so'rovlar generatori.

    Args:
        data_dict (dict): {"table_name": [dict1, dict2, ...]}
        filename (str): Saqlanadigan .sql fayl nomi
    """
    from export.to_csv import log_export  # reuse logging

    filepath = os.path.join(EXPORT_DIR, filename)

    try:
        with open(filepath, mode="w", encoding="utf-8") as file:
            for table_name, records in data_dict.items():
                if not records:
                    continue

                # CREATE TABLE IF NOT EXISTS
                columns = records[0].keys()
                create_stmt = f"CREATE TABLE IF NOT EXISTS {table_name} (\n"
                for col in columns:
                    col_type = "VARCHAR(255)"
                    if col.lower() in ["id", "student_id", "teacher_id", "recipient_id"]:
                        col_type = "INT"
                    create_stmt += f"  {col} {col_type},\n"
                create_stmt = create_stmt.rstrip(",\n") + "\n);\n\n"
                file.write(create_stmt)

                # INSERT INTO
                for record in records:
                    keys = ', '.join(record.keys())
                    values = ', '.join(format_sql_value(v) for v in record.values())
                    insert_stmt = f"INSERT INTO {table_name} ({keys}) VALUES ({values});\n"
                    file.write(insert_stmt)
                file.write("\n")

        print(f"\nExported to SQL: {filepath}")
        log_export(filename, "sql", sum(len(v) for v in data_dict.values()))

    except Exception as e:
        print(f"\nSQL eksportda xatolik: {e}")


def format_sql_value(value):
    """SQL uchun qiymatni to'g'ri formatlash."""
    if isinstance(value, (int, float)):
        return str(value)
    if value is None:
        return "NULL"
    escaped = str(value).replace("'", "''")  # SQL uchun ' belgini escape qilish
    return f"'{escaped}'"


