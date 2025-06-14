import os
from openpyxl import Workbook
from datetime import datetime

EXPORT_DIR = "exported_xlsx"
os.makedirs(EXPORT_DIR, exist_ok=True)

def export_to_xlsx(data_dict, filename="export.xlsx"):
    """
    Bir nechta jadvalni alohida sheetlarga eksport qiladi.

    Args:
        data_dict (dict): {sheet_nomi: [dict1, dict2, ...]}
        filename (str): Yaratiladigan .xlsx fayl nomi
    """
    from export.to_csv import log_export  # reuse logging

    filepath = os.path.join(EXPORT_DIR, filename)
    wb = Workbook()
    wb.remove(wb.active)  # Default sheetni olib tashlaymiz

    try:
        for sheet_name, data_list in data_dict.items():
            ws = wb.create_sheet(title=sheet_name)
            if not data_list:
                continue
            headers = list(data_list[0].keys())
            ws.append(headers)

            for row in data_list:
                ws.append([row.get(col, "") for col in headers])

        wb.save(filepath)
        print(f"\n Exported to XLSX: {filepath}")
        log_export(filename, "xlsx", sum(len(v) for v in data_dict.values()))

    except Exception as e:
        print(f"\n XLSX eksportda xatolik: {e}")
