import asyncio
import random
from pathlib import Path

from django.core.management.base import BaseCommand
from django.conf import settings

from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from asgiref.sync import sync_to_async
from bot.models import Prediction


@sync_to_async
def get_random_prediction():
    predictions = list(Prediction.objects.all())
    if predictions:
        return random.choice(predictions)
    return None


class Command(BaseCommand):
    help = 'Запуск Telegram-бота предсказаний'

    def handle(self, *args, **options):
        async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
            await update.message.reply_text("Привет! Напиши /predict, чтобы получить предсказание.")

        async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
            chat_id = update.effective_chat.id

            # Путь к локальному mp4 с колесом загрузки
            loading_video_path = Path('loading.mp4')  # Обернули строку в Path

            sent_message = await context.bot.send_video(
                chat_id=chat_id,
                video=loading_video_path.open('rb')  # Теперь можно вызвать open
            )

            # Ждём 30 секунд
            await asyncio.sleep(5)

            # Удаляем видео (сообщение с анимацией загрузки)
            await context.bot.delete_message(chat_id=chat_id, message_id=sent_message.message_id)

            # Получаем предсказание из базы
            prediction = await get_random_prediction()

            if prediction:
                if prediction.image:
                    image_path = Path(settings.MEDIA_ROOT) / prediction.image.name
                    await context.bot.send_photo(
                        chat_id=chat_id,
                        photo=image_path.open('rb'),
                        caption=prediction.text
                    )
                else:
                    await update.message.reply_text(prediction.text)
            else:
                await update.message.reply_text("Предсказаний пока нет.")

            # Путь к локальному mp4 с колесом загрузки
            loading_video_path = Path('mail-download.mp4')  # Обернули строку в Path

            sent_message = await context.bot.send_video(
                chat_id=chat_id,
                video=loading_video_path.open('rb')  # Теперь можно вызвать open
            )

        # Вставь сюда свой токен бота
        bot_token = '7799746443:AAFrPPvydjcJ81B9MsbXWgvgTbP94X6-geQ'

        app = ApplicationBuilder().token(bot_token).build()

        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("predict", predict))

        self.stdout.write(self.style.SUCCESS("Бот запущен..."))
        app.run_polling()
