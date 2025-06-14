import csv
import os
from datetime import datetime

# Export qilinadigan fayllar joylashadigan papka
EXPORT_DIR = "exported_csv"
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_to_csv(data_list, filename, fieldnames):
    """
    Ma'lumotlar ro‘yxatini .csv faylga yozadi.

    Args:
        data_list (list of dict): Eksport qilinadigan dictionary obyektlar ro‘yxati
        filename (str): Yaratiladigan CSV fayl nomi (masalan: 'users.csv')
        fieldnames (list of str): CSV fayl sarlavhalari (dict kalitlari bilan bir xil bo‘lishi kerak)
    """
    filepath = os.path.join(EXPORT_DIR, filename)

    try:
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in data_list:
                writer.writerow(item)

        print(f"[📁] Exported to CSV: {filepath}")
        log_export(filename, "csv", len(data_list))

    except Exception as e:
        print(f"[❌] CSV eksportda xatolik: {e}")

def log_export(filename, format, count):
    """
    Har bir eksport amaliyotini log faylga yozadi.

    Args:
        filename (str): Yaratilgan fayl nomi
        format (str): Format nomi (masalan: 'csv', 'xlsx', ...)
        count (int): Eksport qilingan yozuvlar soni
    """
    with open("export_log.txt", mode='a', encoding='utf-8') as log_file:
        log_file.write(
            f"{datetime.now().isoformat()} | Exported {count} records to {filename} ({format})\n"
        )
