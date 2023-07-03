from telebot import TeleBot, types
from random import randint
from shaman import Shaman
from mage import Mage
from druid import Druid
from hunter import Hunter

API_TOKEN = '6143855147:AAGhemlrTGrnoqBq_o24oWeBFcjzTxoMU_o'

bot = TeleBot(API_TOKEN)

is_battle = False

CHARACTERS = {
    'Шаман':Shaman,
    'Друид':Druid, 
    'Охотник':Hunter, 
    'Маг':Mage,
    }

def handler_filter(message:types.Message, filter_obj:dict) -> bool:
    for name in filter_obj.keys():
        if name == message.text:
            return True
    return False
        

        
def init_village_markup(char):
    village_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    lvlup_button = types.KeyboardButton('Повысить уровень')
    battle_button = types.KeyboardButton('Отправиться на охоту за монстрами')
    change_class_button = types.KeyboardButton('Смена класса')
    village_markup.add(lvlup_button, battle_button, change_class_button)
    return village_markup

def change_class_markup():
    change_class_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_shaman = types.KeyboardButton('Шаман')
    button_hunter = types.KeyboardButton('Охотник')
    button_druid = types.KeyboardButton('Друид')
    button_mage = types.KeyboardButton('Маг')
    change_class_markup.add(button_shaman, button_druid, button_hunter, button_mage)
    return change_class_markup
    
def battle_markup():
    battle_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    attack = types.KeyboardButton()
    defend = types.KeyboardButton()
    battle_markup.add(attack, defend)
    return battle_markup


if __name__ == '__main__':

    @bot.message_handler(commands=['start'])
    def start(message:types.Message):

        bot.reply_to(
        message, 
        '''Добро пожаловать в наш мир путник. Здесь тебя ждут приключения, опасности и огромная сила. Удачи!''', 
        reply_markup = change_class_markup()
)


    @bot.message_handler(func=handler_filter(filter_obj=CHARACTERS))
    def choose_class(message:types.Message):
        if not is_battle:
            bot.send_message(chat_id=message.chat.id, text=f'Твой выбор: {message.text}', reply_markup=init_village_markup())
            character = CHARACTERS[message.text]()
        else:
            bot.send_message(message.chat.id, 'Извини, класc сменить нельзя, пока ты в бою')
            
    @bot.message_handler(commands=['Повышение уровня'])
    def level_up(char):
        char.level_up()
        
    @bot.message_handler(commands=['Защищать деревню!'])
    def battle(char):
        pass
        
bot.infinity_polling()
    
            
    
    
            
    

