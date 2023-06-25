from telebot import TeleBot, types
from random import randint
from shaman import Shaman
from mage import Mage
from druid import Druid
from hunter import Hunter

API_TOKEN = '6143855147:AAGhemlrTGrnoqBq_o24oWeBFcjzTxoMU_o'

bot = TeleBot(API_TOKEN)

CHARACTERS = {
    'Шаман':Shaman,
    'Друид':Druid, 
    'Охотник':Hunter, 
    'Маг':Mage,
    }

def first_init_markup():
    init_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_shaman = types.KeyboardButton('Шаман')
    button_hunter = types.KeyboardButton('Охотник')
    button_druid = types.KeyboardButton('Друид')
    button_mage = types.KeyboardButton('Маг')
    init_markup.add(button_shaman, button_druid, button_hunter, button_mage)

def init_village_markup(prof):
    village_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    lvlup_button = types.KeyboardButton('Повысить уровень')
    battle_button = types.KeyboardButton('Отправиться на охоту за монстрами')
    village_markup.add(lvlup_button, battle_button)
    return village_markup



if __name__ == '__main__':

    @bot.message_handler(commands=['start'])
    def start(message:types.Message):

        bot.reply_to(message, '''
            Добро пожаловать в наш мир путник.
            Здесь тебя ждут приключения, опасности и огромная сила.
            Удачи!
        ''')
    first_init_markup()


    @bot.message_handler(content_types=['text'])
    def choose_class(message:types.Message):
        if message.text in CHARACTERS.values():
            bot.send_photo(chat_id=message.chat.id, caption='Ты выбрал шамана', photo=open())
            character = CHARACTERS[message.text]()
        else:
            bot.send_message(message.chat.id, 'Такого класса не существует')

