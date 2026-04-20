from datetime import datetime
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
    btn3 = types.KeyboardButton('✏️ Записаться')
    markup.add(btn1, btn2, btn3)
    return markup

# --- ОБРАБОТЧИК КОМАНДЫ /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        f"Здравствуйте, {message.from_user.first_name}!\n"
        "Добро пожаловать в наш бот-создания программ\n"
        "Выберите действие в меню ниже:",
        reply_markup=get_main_keyboard()
    )

# --- ОБРАБОТЧИК ТЕКСТОВЫХ СООБЩЕНИЙ ---
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text
    
    if text == '📋 Услуги':
        services_text = (
            "💰 *Прайс-лист:*\n\n"
            "💻 Создание программ (html, js, css) - 1500 ₽\n"
            "🤖 Создание телеграм бота - 1500 ₽\n"
            "🎯 Другое\n\n"
            "Для записи нажмите кнопку '✏️ Записаться'."
        )
        bot.send_message(chat_id, services_text, parse_mode='Markdown', reply_markup=get_main_keyboard())
    
    elif text == '📞 Контакты':
        contacts_text = (
            "📍 *Наши контакты:*\n\n"
            "📞 Телефон: +7 (960) 512-00-71\n"
            "🕐 Часы работы: Пн-Вс 10:00 - 21:00"
        )
        bot.send_message(chat_id, contacts_text, parse_mode='Markdown', reply_markup=get_main_keyboard())
    
    elif text == '✏️ Записаться':
        msg = bot.send_message(
            chat_id,
            "Давайте запишем вас на услугу.\nПожалуйста, введите ваше *Имя*:",
            parse_mode='Markdown',
            reply_markup=types.ForceReply(selective=False)
        )
        bot.register_next_step_handler(msg, process_name_step)
    
    elif chat_id in user_
        pass
    
    else:
        bot.send_message(chat_id, "Пожалуйста, воспользуйтесь кнопками меню.", reply_markup=get_main_keyboard())

# --- ШАГ 1: ОБРАБОТКА ИМЕНИ ---
def process_name_step(message):
    chat_id = message.chat.id
    name = message.text.strip()
    user_data[chat_id] = {'name': name}
    msg = bot.send_message(chat_id, f"{name}, укажите ваш *номер телефона*:", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_phone_step)

# --- ШАГ 2: ОБРАБОТКА ТЕЛЕФОНА ---
def process_phone_step(message):
    chat_id = message.chat.id
    phone = message.text.strip()
    if chat_id not in user_
        bot.send_message(chat_id, "Что-то пошло не так. Начните заново.", reply_markup=get_main_keyboard())
        return
    user_data[chat_id]['phone'] = phone
    msg = bot.send_message(chat_id, "На какое *время и дату* вас записать?\n(Например: завтра в 15:00)", parse_mode='Markdown')
    bot.register_next_step_handler(msg, process_time_step)

# --- ШАГ 3: ОБРАБОТКА ВРЕМЕНИ И ФИНАЛ ---
def process_time_step(message):
    chat_id = message.chat.id
    time = message.text.strip()
    
    if chat_id not in user_data:
        bot.send_message(chat_id, "Сессия устарела. Начните заново.", reply_markup=get_main_keyboard())
        return
    
    user_data[chat_id]['time'] = time
    name = user_data[chat_id]['name']
    phone = user_data[chat_id]['phone']
    
    print("=" * 30)
    print("📋 НОВАЯ ЗАЯВКА:")
    print(f"Имя: {name}")
    print(f"Телефон: {phone}")
    print(f"Время: {time}")
    print(f"User ID: {chat_id}")
    print("=" * 30)
    
    del user_data[chat_id]
    
    # Сообщение клиенту
    bot.send_message(
        chat_id,
        f"✅ *Спасибо, {name}!*\n\n"
        "Ваша заявка принята.\n"
        "Администратор свяжется с вами в ближайшее время.\n\n"
        "Хорошего дня! 🌺",
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )
    
    # Уведомление АДМИНУ (вам)
    admin_chat_id = 8010944762
    
    bot.send_message(
        admin_chat_id,
        f"🔔 <b>НОВАЯ ЗАЯВКА!</b>\n\n"
        f"👤 Имя: {name}\n"
        f"📞 Телефон: {phone}\n"
        f"⏰ Время: {time}\n"
        f"🆔 ID: {chat_id}",
        parse_mode='HTML'
    )

# --- ЗАПУСК БОТА ---
if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()

