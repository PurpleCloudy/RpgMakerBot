from telebot import TeleBot, types
from shaman import Shaman
from mage import Mage
from druid import Druid
from hunter import Hunter
from character import Character


API_TOKEN = '6143855147:AAGhemlrTGrnoqBq_o24oWeBFcjzTxoMU_o'
CHARACTERS = {
    'Шаман': Shaman,
    'Друид': Druid,
    'Охотник': Hunter,
    'Маг': Mage,
}

is_battle_mode: bool = False
cooldown = {}


def handler_filter(message: types.Message) -> bool:
    for name in CHARACTERS.keys():
        if name == message.text:
            return True
    return False

        
def init_village_markup():
    village_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    lvlup_button = types.KeyboardButton('Повысить уровень')
    battle_button = types.KeyboardButton('Отправиться на охоту за монстрами')
    change_class_button = types.KeyboardButton('Смена класса')
    village_markup.add(lvlup_button, battle_button, change_class_button)
    return village_markup


def change_class_markup():
    change_class_reply_keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_shaman = types.KeyboardButton('Шаман')
    button_hunter = types.KeyboardButton('Охотник')
    button_druid = types.KeyboardButton('Друид')
    button_mage = types.KeyboardButton('Маг')
    change_class_reply_keyboard_markup.add(button_shaman, button_druid, button_hunter, button_mage)
    return change_class_reply_keyboard_markup


def battle_markup(character: Druid|Shaman|Mage|Hunter):
    battle_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    abilities = [types.KeyboardButton(ability) for ability in character.abilities.keys()]
    attack_button = types.KeyboardButton('Атаковать')
    defend = types.KeyboardButton('Защищаться')
    battle_reply_markup.add(attack_button, defend)
    for ability in abilities:
        battle_reply_markup.add(ability)
    return battle_reply_markup


def main():
    bot = TeleBot(API_TOKEN)

    @bot.message_handler(commands=['start'])
    def start(message: types.Message):

        bot.reply_to(
            message=message,
            text='Добро пожаловать в наш мир путник. Здесь тебя ждут приключения, опасности и огромная сила. Удачи!',
            reply_markup=change_class_markup()
        )

    @bot.message_handler(func=lambda menu: True if menu.text == 'Смена класса' else False)
    def transfer_to_choosing(message: types.Message):
        if not is_battle_mode:
            start(message)
        else:
            bot.send_message(message.chat.id, 'Извини, класc сменить нельзя, пока ты в бою')

    @bot.message_handler(func=handler_filter)
    def choose_class(message: types.Message):
        global character
            
        bot.send_message(
            chat_id=message.chat.id,
            text=f'Твой выбор: {message.text}',
            reply_markup=init_village_markup()
        )
        character = CHARACTERS[message.text]()

    @bot.message_handler(func=lambda menu: True if menu.text == 'Повысить уровень' else False)
    def level_up(message=types.Message):
        if character:
            if character.characteristics['exp'] >= 100:
                bot.send_message(chat_id=message.chat.id, text=character.level_up())
            else:
                bot.send_message(chat_id=message.chat.id, text='У тебя пока недостаточно опыта')

    @bot.message_handler(func=lambda menu: True if menu.text == 'Отправиться на охоту за монстрами' else False)
    def battle(message: types.Message):
        global is_battle_mode
        global monster
        
        is_battle_mode = True
        monster = Character(character.characteristics['lvl'] + 2)
        bot.send_message(
            chat_id=message.chat.id,
            text=f"Из-за угла выскакивает готовое к бою чудовище, судя по его виду ты можешь определить, что его: "
                 f"сила ~ {monster.characteristics['power']}, а живучесть ~ {monster.characteristics['max_health']} "
                 f"Приготовься к бою!",
            reply_markup=battle_markup(character)
        )

    @bot.message_handler(func=lambda menu: True if menu.text == 'Атаковать' else False)
    def attack(message: types.Message):
        global is_battle_mode
        
        results = character.attack(monster.characteristics['health'])
        monster.characteristics['health'] = results['hp']
        if monster.characteristics['health'] > 0:
            if results['is_crit']:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'Умелый удар попадает в уязвимое место чудовища! '
                         f'У него остается всего {monster.characteristics["health"]} жизней!'
                )
            else:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'Отличный удар! У чудовища остается всего {monster.characteristics["health"]} жизней!'
                )
            cooldown[message.chat.id] += 1
        else:
            character.characteristics['exp'] += monster.characteristics["lvl"] * 15
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Размашистый удар раскалывает череп чудовища. '
                     f'{monster.__del__()}',
                reply_markup=init_village_markup()
            )
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Ты получил {monster.characteristics["lvl"] * 15} опыта'
            )
            is_battle_mode = False

    @bot.message_handler(func=lambda menu: True if menu.text == 'Защищаться' else False)
    def defence(message: types.Message):
        results = character.defence(monster.characteristics['power'])
        character.characteristics['health'] = results['hp']
        if character.characteristics['health'] >= 0:
            if results['is_crit']:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'Уворот оказывается успешным и благодаря выигранному времени ты заходишь за спину противника! '
                        f'У тебя остается {character.characteristics["health"]} жизней и инициатива на твоей стороне, '
                        f'пока монстр пытается вытащить оружие!'
                )
            else:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'Уворот оказывается неудачным! У тебя остается {character.characteristics["health"]} жизней!'
                )
            cooldown[message.chat.id] += 1
        else:
            bot.send_message(chat_id=message.chat.id, text=character.__del__())
            
    @bot.message_handler(func=lambda ability: True if ability.text in character.abilities.keys() else False)
    def abilities_list(message:types.Message, character: Druid|Shaman|Mage|Hunter):
        if character.abilities[message.text](switcher=True) == None|True:
            bot.send_message(
                        chat_id=message.chat.id,
                        text=f'Ты успешно использовал спосбоность {message.text}, твоё тело наливается силой'
                    )
            cooldown[message.chat.id] = 0
            cooldown['ability'] = f'{message.text}' 
            
        else:
            bot.send_message(
                        chat_id=message.chat.id,
                        text=f'Тебе не удается использовать сокрытую внутри тебя силу.'
                    )
            
    @bot.message_handler(func=lambda message: True if cooldown.get(message.chat.id) == 2 else False)
    def off_ability(message:types.Message, character: Druid|Shaman|Mage|Hunter):
            bot.send_message(
                        chat_id=message.chat.id,
                        text=f'Время действия способности {cooldown["ability"]} прошло'
                    )
            character.abilities[cooldown["ability"]](switcher=False)
            

    print("Bot is running...")
    bot.infinity_polling()


if __name__ == '__main__':
    main()
