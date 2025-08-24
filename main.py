import telebot
from config import TG_TOKEN
from ai_helper import ai_classification
import time


bot = telebot.TeleBot(TG_TOKEN)

@bot.message_handler(commands=['start'])
def start_command(message):
    text = (
        f'👋Привет, {message.from_user.username}!/n'
        "🤖Я - бот, который распознает породы собак на фото. Отправь мне фотографию🌇, \n"
        'чтобы узнать, есть ли на ней собака отправь /photo'
    )
    bot.send_message(message.chat.id, text)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # получаем информацию о фотографии
    file_info = bot.get_file(message.photo[-1].file_id)
    file_name = file_info.file_path.split('/')[-1] # 'smt/telegram/smt/smt/smt/duck.jpg'
    file_path = file_info.file_path 

    # сохраняем
    downloaded_file = bot.download_file(file_path)
    with open(file_name, 'wb') as photo:
        photo.write(downloaded_file)

    # Вызываем детектор классификатор
    results = ai_classification(file_name)

    # Подготавливаем вывод и отправляем результат
    if results:
        text = 'Вот, что у меня получилось найти\n\n'
        bot.send_message(message.chat.id, text)
    else:
        text = 'К сожалению, я никого здесь не увидел'
        return bot.send_message(message.chat.id, text)

    for photo_path, result in results.items():
        with open(photo_path, 'rb') as photo:
            image_caption = f'С вероятностью{result[1]}% на фото {result[0].lower()}'
            bot.send_photo(message.chat.id, photo = photo, caption=image_caption)
            time.sleep(1)

    bot.send_message(message.chat.id, 'На этом всё...')

bot.infinity_polling()