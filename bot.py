import telebot
from telebot import types

# --- НАСТРОЙКИ ---
TOKEN = "8423103342:AAFr5LiWPnh6Z_N7rmdpDTWun3wWPNwNpnM"
bot = telebot.TeleBot(TOKEN)

# Хранилище состояний пользователя (временное, в памяти)
user_data = {}

# --- ГЛАВНОЕ МЕНЮ ---
def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('📋 Услуги')
    btn2 = types.KeyboardButton('📞 Контакты')
    btn3 = types.KeyboardButton('📝 Записаться')
    markup.add(btn1, btn2, btn3)
    return markup

# --- ОБРАБОТЧИК КОМАНДЫ /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {message.from_user.first_name}!\n"
        "Добро пожаловать в наш бот-салон красоты.\n"
        "Выберите действие в меню ниже:",
        reply_markup=get_main_keyboard()
    )

# --- ОБРАБОТЧИК ТЕКСТОВЫХ СООБЩЕНИЙ (МЕНЮ И ВВОД ДАННЫХ) ---
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text

    # 1. Кнопка "Услуги"
    if text == '📋 Услуги':
        services_text = (
            "💅 *Прайс-лист:*\n\n"
            "• Маникюр — 1000 ₽\n"
            "• Стрижка — 1500 ₽\n\n"
            "Для записи нажмите кнопку '📝 Записаться'."
        )
        bot.send_message(chat_id, services_text, parse_mode='Markdown', reply_markup=get_main_keyboard())

    # 2. Кнопка "Контакты"
    elif text == '📞 Контакты':
        contacts_text = (
            "📌 *Наши контакты:*\n\n"
            "📞 Телефон: +7 (960) 512-00-71\n"
            "📍 Адрес: г. Иваново, Ивановская обл.\n"
            "🕒 Часы работы: Пн-Вс 10:00 - 21:00"
        )
        bot.send_message(chat_id, contacts_text, parse_mode='Markdown', reply_markup=get_main_keyboard())

    # 3. Кнопка "Записаться" (Начало процесса)
    elif text == '📝 Записаться':
        msg = bot.send_message(
            chat_id,
            "Давайте запишем вас на процедуру.\nПожалуйста, введите ваше *Имя*:",
            parse_mode='Markdown',
            reply_markup=types.ForceReply(selective=False) # Убираем клавиатуру, показываем поле ввода
        )
        bot.register_next_step_handler(msg, process_name_step)

    # 4. Если бот ожидает данные от пользователя (состояние есть в словаре)
    elif chat_id in user_data:
        # Логика обработки шагов (имя -> телефон -> время) вынесена в отдельные функции ниже
        # Сюда попасть не должно, так как мы используем register_next_step_handler
        pass

    else:
        # Если пользователь прислал что-то непонятное вне сценария
        bot.send_message(chat_id, "Пожалуйста, воспользуйтесь кнопками меню.", reply_markup=get_main_keyboard())

# --- ШАГ 1: ОБРАБОТКА ИМЕНИ ---
def process_name_step(message):
    chat_id = message.chat.id
    name = message.text.strip()
    
    # Сохраняем имя
    user_data[chat_id] = {'name': name}
    
    msg = bot.send_message(chat_id, f"{name}, укажите ваш *номер телефона*:", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_phone_step)

# --- ШАГ 2: ОБРАБОТКА ТЕЛЕФОНА ---
def process_phone_step(message):
    chat_id = message.chat.id
    phone = message.text.strip()
    
    # Проверка, что данные по имени есть (на случай сбоя)
    if chat_id not in user_data:
        bot.send_message(chat_id, "Что-то пошло не так. Начните заново с кнопки '📝 Записаться'.", reply_markup=get_main_keyboard())
        return
        
    user_data[chat_id]['phone'] = phone
    
    msg = bot.send_message(chat_id, "На какое *время и дату* вас записать?\n(Например: завтра в 15:00)", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_time_step)

# --- ШАГ 3: ОБРАБОТКА ВРЕМЕНИ И ФИНАЛ ---
def process_time_step(message):
    chat_id = message.chat.id
    time = message.text.strip()
    
    if chat_id not in user_data:
        bot.send_message(chat_id, "Сессия устарела. Нажмите '📝 Записаться' снова.", reply_markup=get_main_keyboard())
        return

    # Сохраняем время
    user_data[chat_id]['time'] = time
    
    # Извлекаем все данные
    name = user_data[chat_id]['name']
    phone = user_data[chat_id]['phone']
    
    # ----- ВЫВОД ДАННЫХ В КОНСОЛЬ (ЛОГИРОВАНИЕ) -----
    print("=" * 30)
    print("📝 НОВАЯ ЗАЯВКА:")
    print(f"Имя: {name}")
    print(f"Телефон: {phone}")
    print(f"Время: {time}")
    print(f"User ID: {chat_id}")
    print("=" * 30)
    # ------------------------------------------------

    # Удаляем данные из временного хранилища (опционально)
    del user_data[chat_id]
    
    # Финальное сообщение
    bot.send_message(
        chat_id,
        f"✅ *Спасибо, {name}!*\n\n"
        "Ваша заявка принята.\n"
        "Администратор свяжется с вами в ближайшее время для подтверждения записи.\n\n"
        "Хорошего дня! 💐",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard() # Возвращаем главное меню
    )

# --- ЗАПУСК БОТА ---
if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()
