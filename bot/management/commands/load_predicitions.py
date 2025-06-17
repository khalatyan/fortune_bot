import os
import json
from django.core.files import File
from django.core.management.base import BaseCommand

from bot.models import Prediction


class Command(BaseCommand):
    help = 'Импортирует предсказания из JSON-файла с привязкой к изображениям'

    def handle(self, *args, **kwargs):
        json_path = os.path.join('predictions.json')
        media_path = "images"
        Prediction.objects.all().delete()

        if not os.path.exists(json_path):
            self.stderr.write(self.style.ERROR('Файл predictions.json не найден.'))
            return

        with open(json_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        for item in data:
            text = item['text']
            image_filename = item.get('image')

            if Prediction.objects.filter(text=text).exists():
                self.stdout.write(self.style.WARNING(f'⏩ Уже существует: {text[:40]}...'))
                continue

            prediction = Prediction(text=text)

            if image_filename:
                image_path = os.path.join(media_path, image_filename)
                if os.path.isfile(image_path):
                    with open(image_path, 'rb') as img_file:
                        prediction.image.save(image_filename, File(img_file), save=False)

            prediction.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Добавлено: {text[:40]}'))
