from django.core.management.base import BaseCommand
import re

from bot.models import Prediction


class Command(BaseCommand):
    help = 'Загружает предсказания из файла в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('filepath', type=str, help='Путь к текстовому файлу с предсказаниями')

    def handle(self, *args, **kwargs):
        filepath = kwargs['filepath']

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                lines = file.readlines()

            count = 0
            for line in lines:
                line = line.strip()
                if not line:
                    continue  # пропускаем пустые строки

                # удаляем номер в начале строки (например, "1. ", "29. ", "30. ")
                cleaned = re.sub(r'^\d+\.\s*', '', line)

                if cleaned:
                    # сохраняем в БД, избегая дубликатов
                    _, created = Prediction.objects.get_or_create(text=cleaned)
                    if created:
                        count += 1

            self.stdout.write(self.style.SUCCESS(f'Успешно добавлено {count} предсказаний.'))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f'Файл не найден: {filepath}'))
