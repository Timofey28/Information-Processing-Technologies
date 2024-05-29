import os
from dotenv import load_dotenv

# DOTENV_PATH = os.path.join('..', '.env')
DOTENV_PATH = 'C:\\_Python\\MAI\\6 - Технологии обработки информации\\PZ_4\\.env'


def get_data(key: str) -> str:
    """
    Функция для получения данных из .env файла
    """
    if os.path.exists(DOTENV_PATH):
        load_dotenv(DOTENV_PATH)
        return os.getenv(key)
    else:
        raise FileNotFoundError("Файл .env не найден")