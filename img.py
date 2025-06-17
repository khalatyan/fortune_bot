import os
from pathlib import Path

# Укажи путь к папке
folder_path = Path("./images")  # Например: Path("/home/user/images")

# Получаем список всех файлов (исключая папки)
files = [f.name for f in folder_path.iterdir() if f.is_file()]

# Выводим названия
for file_name in files:
    print(file_name)
