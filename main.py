import time
import json
from PIL import Image, ImageDraw, ImageFont
from telegram import Update, Bot, InputFile
import random
from io import BytesIO
from telegram.ext import (
    Updater,
    MessageHandler,
    CallbackContext,
    Filters  # Note: use Filters instead of filters
)


#Содержит токен бота для подключения
bot = Bot(token="7875443059:AAH1o7EJPDOypj3yIalCBcpOjfizx30NIRU")


def reply_to_text(update: Update, context: CallbackContext):
    user_message = update.message.text.lower()


    # базовая помощь с описанием работы всех функций + про Коордика
    if user_message == "!помощь":
        update.message.reply_text("Привет, организатор!\n\nЯ способный парень, но иногда "
                                  "могу косячить. Если возникают проблемы, то тыкайте Юру\n\nВот, что я умею:\n\n"
                                  "!дуэль - Выбирай жертву и вызови её на дуэль\n"
                                  "!рулетка - Выход гордого волка-одиночки, который хочет испытать своё везение\n"
                                  "!мысль - Прочитать великие изречения коллег\n"
                                  "!цитата - Создать собственное великое изречение\n"
                                  "!вероятность, что - Сам Господь Бог вычислит, с какой вероятностью произойдёт это событие\n"
                                  "!когда - Разложу карты таро и скажу, когда произойдёт то или иное событие\n"
                                  "!подскажи - Отвечу будет или не будет\n\n"
                                  "Также, у меня есть друг - Коордик. Внутри него есть искусственный интеллект. "
                                  "Для работы с ним нужно написать обычный промпт и добавить его имя. "
                                  "Он умеет генерировать тексты, изображения и может рассказать гороскоп на сегодня\n"
                                  "P.S. Но про меня тоже не забывайте( Я правда хороший...",
                                  reply_to_message_id=None,)

    # проверяем постоянно, если вдруг человек из списка мертвых уже пережил своё время восстановления
    try:
        with open('deadmen.json', 'r', encoding="utf-8") as read_file:
            mute = json.load(read_file)
        read_file.close()
    except FileNotFoundError:
        mute = {}
    keys_to_unmute = []
    for key, unmute_date in mute.items():
        if unmute_date < time.time():
            keys_to_unmute.append(key)
    for key in keys_to_unmute:   #нужно доработать цикл, так как не возвращает полноценно. Тут он убирает из списка мертвых
        mute.pop(key)
        update.message.reply_text(f"И всё-таки, {update.effective_user.full_name} воскрес!"
                                  f"\nБудь аккуратнее в следующий раз 🥺",
                                  reply_to_message_id=None,)
        with open('deadmen.json', 'w') as write_file:
            json.dump(mute, write_file)
        write_file.close()
    if str(update.effective_user.id) in mute.keys(): #работает сам почему-то. Удаляет сообщения мертвяков
        try:
            update.message.delete(update.effective_user.id)
            return "ok"
        except:
            pass

    # базовый чек на айди чата
    elif user_message == "!айди":
        chat_id = update.effective_chat.id
        update.message.reply_text(f"Айди этого чата => {chat_id}",
                                        reply_to_message_id=None,)

    #получаем айди нападающего и жертвы + получаем дату анмута будущего мертвеца. Также, рандомно выбираем цифру
    elif user_message == "!дуэль":
        iniz = update.effective_user.id
        shertv = update.message.reply_to_message.from_user.id
        dez = random.randint(1, 2)
        unmute_date = time.time() + 3600
        # проверяем, чтобы не было дуэли на самого себя
        if shertv == update.effective_user.id:
            update.message.reply_text("Ты чё удумал? Для самоубийств используй !рулетка", reply_to_message_id=None,)

        # проверяем, чтобы не было дуэли на бота
        elif shertv == context.bot.id:
            update.message.reply_text("Ты на кого полез, ёпт. Беги в страхе, пока я не передумал")

        # в остальных случаях, если рандомно выпадает цифра 2, то бот "убивает" нападающего + закидывает
        # нападающего в список мёртвых

        else:
            if dez == 2:
                update.message.reply_text(f"К сожалению, {update.effective_user.full_name} умер(((\n"
                                          f"Вините {update.message.reply_to_message.from_user.full_name} во всём!",
                                      reply_to_message_id=None,)
                mute[str(iniz)] = unmute_date
                with open('deadmen.json', 'w') as write_file:
                    json.dump(mute, write_file)
                write_file.close()

            # в остальных случаях, если рандомно выпадает цифра 1, то бот "убивает" жертву + закидывает
            # жертву в список мёртвых
            else:
                update.message.reply_text(f"К сожалению, {update.message.reply_to_message.from_user.full_name} умер(((\n"
                                          f"Вините {update.effective_user.full_name} во всём!",
                                      reply_to_message_id=None,)
                mute[str(shertv)] = unmute_date
                with open('deadmen.json', 'w') as write_file:
                    json.dump(mute, write_file)
                write_file.close()


    # выбираем рандомно цифру от 1 до 3 и если выпадает 2, то самоубийца умирает и бот закидывает его в список мёртвых
    elif user_message == "!рулетка":
        des = random.randint(1, 3)
        if des == 2:
            update.message.reply_text(f"{update.effective_user.full_name}, брат, тебе не повезло(((\n"
                                      f"Будь аккуратнее в следующий раз!",
                                      reply_to_message_id=None, )
            unmute_date = time.time() + 3600
            mute[str(update.effective_user.id)] = unmute_date
            with open('deadmen.json', 'w') as write_file:
                json.dump(mute, write_file)
            write_file.close()

        else:
            update.message.reply_text(f"{update.effective_user.full_name}, брат, а ты везунчик!\n"
                                      f"Но лучше так не делай в следующий раз...",
                                      reply_to_message_id=None, )

    # бот подготавливает фон для мысли
    elif user_message == "!мысль":
        def publish_image(text: str, filename: str = "thought.png"):
            background = Image.open("font.png")
            img = background.resize((1000, 1000))
            draw = ImageDraw.Draw(img)

            # бот вытаскивает рандомную цитату из json'а с мыслями

            try:
                with open('thoughts.json', 'r') as f:
                    saved_messages = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                saved_messages = []

            if not saved_messages:
                update.message.reply_text( f"Нет сохраненных цитат", reply_to_message_id=None,)

            message_data = random.choice(saved_messages)

            text = message_data.get('thought', '')
            name = message_data.get('name', '')

            # бот подставляет данные из json'а в картинку

            title_font = ImageFont.truetype("VelaSans-ExtraBold.ttf", size=60)  # geniral font.ttf
            text_font_1 = ImageFont.truetype("VelaSans-ExtraBold.ttf", size=40)  # vela sans.ttf
            text_font_2 = ImageFont.truetype("VelaSans-Bold.ttf", size=24)  # vela sans.ttf

            # рисуем текст (цвет, позиция, шрифт)
            draw.text((180, 30), "Цитаты великих Тапков", fill=(31, 31, 31), font=title_font)
            draw.text((370, 450), f" «{text}»", fill=(31, 31, 31),
                      font=text_font_1)
            draw.text((600, 620), f"© {name}", fill=(31, 31, 31),
                      font=text_font_2)

            # сохраняем изображение
            img.save(filename)
            return filename

        # бот закидывает готовую мысль в чат

        image_path = publish_image("")
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=update.effective_chat.id, photo=InputFile(photo))

    elif user_message == "!цитата":
        def generate_image(text: str, filename: str = "thought.png"):
            # Создаём изображение (размер, цвет фона)
            background = Image.open("font.png")
            img = background.resize((1000, 1000))
            draw = ImageDraw.Draw(img)
            photos = context.bot.get_user_profile_photos(update.message.reply_to_message.from_user.id, limit=1)

            # бот сохраняет мысль в словарь и делает копию для транспортировки в json

            th_data = {
                "thought": update.message.reply_to_message.text,
                "name": update.message.reply_to_message.from_user.full_name,
                "from_id": update.message.reply_to_message.from_user.id
            }
            thought = th_data.copy()

            # бот транспортирует мысль в json

            try:
                with open('thoughts.json', 'r') as t:
                    messages = json.load(t)
                    if not isinstance(messages, list):
                        messages = []
            except (FileNotFoundError, json.JSONDecodeError):
                messages = []

            messages.append(thought)

            # сохраняем обновленный список в файл
            with open('thoughts.json', 'w') as t:
                json.dump(messages, t)

            photo = photos.photos[0][-1]
            file = context.bot.get_file(photo.file_id)

                # Скачиваем и конвертируем в изображение
            img_bytes = BytesIO()
            file.download(out=img_bytes)
            image = Image.open(img_bytes)

            title_font = ImageFont.truetype("VelaSans-ExtraBold.ttf", size=60) #geniral font.ttf
            text_font_1 = ImageFont.truetype("VelaSans-ExtraBold.ttf", size=40) #vela sans.ttf
            text_font_2 = ImageFont.truetype("VelaSans-Bold.ttf", size=24) #vela sans.ttf

            # Рисуем текст (цвет, позиция, шрифт)
            draw.text((180, 30), "Цитаты великих Тапков", fill=(31, 31, 31), font=title_font)
            draw.text((370, 450), f" «{update.message.reply_to_message.text}»", fill=(31, 31, 31),
                      font=text_font_1)
            draw.text((600, 620), f"© {update.message.reply_to_message.from_user.full_name}", fill=(31, 31, 31),
                      font=text_font_2)
            result = Image.new('RGB', (image.width + 20, image.height + 20))
            result.paste(image, (600,620))

            # Сохраняем изображение
            img.save(filename)
            return filename

        image_path = generate_image("")
        with open(image_path, 'rb') as photo:
            bot.send_photo(chat_id=update.effective_chat.id, photo=InputFile(photo))


    #elif user_message == "!орг дня":
    #    update.message.reply_text("Нормально, у меня же нет чувств!")

    #elif "!инфа" in user_message:
    #    update.message.reply_text("Нормально, у меня же нет чувств!")


    #elif "!кто" in user_message:
     #   update.message.reply_text("Нормально, у меня же нет чувств!")


    elif user_message[:17] == "!вероятность, что":
        update.message.reply_text(user_message[18:] + " с вероятностью " + str(random.randint(0, 100)) + "%",
                                      reply_to_message_id=None,)


    elif user_message[:6] == "!когда":
        ch = random.choice([f"сегодня {random.choice(['днём', 'вечером', 'ночью'])}",
                                                      f"завтра {random.choice(['утром', 'днём', 'вечером', 'ночью'])}",
                                                      f"{random.randint(1,29)} "
                                                      f"{random.choice(['января', 'февраля', 'марта', 'апреля', 'мая', 
                                                                        'июня','июля', 'августа', 'сентября', 'октября', 
                                                                        'ноября', 'декабря'])}"
                                                      f" {random.randint(2025,2055)} года"])
        update.message.reply_text("Я вижу... вижу, что " + user_message[7:] + " " + ch,
                                      reply_to_message_id=None,)


    elif user_message[:9] == "!подскажи":
        update.message.reply_text(random.choice(['Естественно!', 'Нет, конечно', 'Вообще без понятия(']),
                                      reply_to_message_id=None,)




def main():
    updater = Updater("7875443059:AAH1o7EJPDOypj3yIalCBcpOjfizx30NIRU")
    dp = updater.dispatcher  # Получаем Dispatcher из Updater
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_to_text))  # Fixed `Filters`

    updater.start_polling()
    updater.idle()  # Блокирующий вызов для поддержания работы бота

if __name__ == '__main__':
    main()