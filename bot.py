
import telebot
from telebot import types
from config import TOKEN
from logic import CLASSES, SUBJECTS, get_base_info

bot = telebot.TeleBot(TOKEN)
user_choices = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    buttons = [types.KeyboardButton(f"{c} класс") for c in CLASSES]
    markup.add(*buttons)
    
    bot.send_message(
        message.chat.id, 
        "Я бот для подготовки к экзаменам. Выбери свой класс:", 
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: any(f"{c} класс" == message.text for c in CLASSES))
def choose_class(message):
    clean_class = message.text.replace(" класс", "").strip()
    user_choices[message.chat.id] = {"class": clean_class}
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    buttons = [types.KeyboardButton(subj) for subj in SUBJECTS]
    markup.add(*buttons)
    
    bot.send_message(
        message.chat.id, 
        f"Хорошо, {message.text}! Теперь выбери предмет:", 
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text in SUBJECTS)
def choose_subject(message):
    chat_id = message.chat.id
    subject = message.text
    
    if chat_id in user_choices and "class" in user_choices[chat_id]:
        student_class = user_choices[chat_id]["class"]
    else:
        student_class = "9"

    material = get_base_info(student_class, subject)
    
    markup = types.ReplyKeyboardRemove()
    
    response = (
        f"{material}\n\n"
        f"Если хочешь пройтись по новой, пиши /start"
    )
    
    bot.send_message(chat_id, response, parse_mode="Markdown", reply_markup=markup)

if __name__ == '__main__':
    print("Бот запущен, всё ок!")
    bot.infinity_polling()
