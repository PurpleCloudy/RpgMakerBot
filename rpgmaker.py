from telebot import TeleBot, types
from random import randint

API_TOKEN = '6143855147:AAGhemlrTGrnoqBq_o24oWeBFcjzTxoMU_o'

bot = TeleBot(API_TOKEN)

CHARECTERS = ['shaman', 'druid', 'hunter', 'mage']

@bot.message_handler(commands=['start'])
def start(message:types.Message):

    bot.reply_to(message, '''
        Добро пожаловать в наш мир путник.
        Здесь тебя ждут приключения, опасности и огромная сила.
        Удачи!
    ''')
