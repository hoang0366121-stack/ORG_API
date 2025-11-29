import json
import os

def save_to_file(filename, data):
    """Lưu dữ liệu ra file JSON trong thư mục gốc dự án"""
    path = os.path.join(os.getcwd(), filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"✅ Dữ liệu đã được lưu vào: {path}")
