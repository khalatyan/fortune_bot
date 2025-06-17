import os
import random
from django.core.management.base import BaseCommand
from django.core.files import File

from bot.models import Prediction


class Command(BaseCommand):
    help = 'Связывает рандомные картинки из папки с предсказаниями'

    def add_arguments(self, parser):
        parser.add_argument('images_dir', type=str, help='Путь к папке с картинками')

    def handle(self, *args, **kwargs):
        images_dir = kwargs['images_dir']

        if not os.path.isdir(images_dir):
            self.stderr.write(f'Папка не найдена: {images_dir}')
            return

        # Список всех файлов в папке (фильтруем по расширениям картинок)
        valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
        image_files = [f for f in os.listdir(images_dir) if f.lower().endswith(valid_extensions)]

        if not image_files:
            self.stderr.write('В папке нет подходящих изображений.')
            return

        predictions = Prediction.objects.all()
        total = predictions.count()
        self.stdout.write(f'Найдено {total} предсказаний и {len(image_files)} картинок.')

        for prediction in predictions:
            image_name = random.choice(image_files)
            image_path = os.path.join(images_dir, image_name)

            with open(image_path, 'rb') as img_file:
                django_file = File(img_file)
                # Генерируем уникальное имя файла для сохранения
                filename = f'pred_{prediction.id}_{image_name}'

                # Сохраняем картинку в поле image, перезаписывая старую, если есть
                prediction.image.save(filename, django_file, save=True)

            self.stdout.write(f'К предсказанию {prediction.id} добавлена картинка {image_name}')

        self.stdout.write(self.style.SUCCESS('Все картинки успешно связаны с предсказаниями.'))