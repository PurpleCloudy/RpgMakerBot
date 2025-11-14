"""
Telegram бот для RPG-игры с элементами боя и развития персонажа.

Модуль предоставляет возможность игрокам выбирать классы (Шаман, Друид, Охотник, Маг),
уровень персонажа, сражаться с монстрами, использовать способности, а также
сохранять и загружать прогресс в форматах JSON и XML.

Добавлена механика временных событий - особое подземелье, доступное раз в 4 часа реального времени.

Атрибуты:
    API_TOKEN (str): Токен для доступа к Telegram Bot API (в реальном проекте
                     должен быть вынесен в переменные окружения).
    CHARACTERS (dict): Словарь соответствия названий классов и их классов.
    is_battle_mode (bool): Флаг, указывающий, находится ли пользователь в бою.
    cooldown (dict): Словарь для отслеживания кулдаунов действий пользователей.
    character (Character): Экземпляр класса персонажа текущего пользователя.
    monster (Character): Экземпляр класса монстра в текущем бою.
    current_user_id (int): ID текущего пользователя.
    json_manager (JSONDataManager): Менеджер для работы с JSON-файлами.
    xml_manager (XMLDataManager): Менеджер для работы с XML-файлами.
    dungeon_cooldowns (dict): Словарь для хранения времени последнего посещения подземелья по user_id.
    TIME_PATTERN (str): Регулярное выражение для валидации времени в формате ЧЧ:ММ:СС.
    NAME_PATTERN (str): Регулярное выражение для валидации имени персонажа (только русские буквы).
"""

from telebot import TeleBot, types
from shaman import Shaman
from mage import Mage
from druid import Druid
from hunter import Hunter
from character import Character
from data_manager import JSONDataManager, XMLDataManager
from exceptions import CharacterError, DataStorageError
from dotenv import load_dotenv
import os
import re
from datetime import datetime, timedelta

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
CHARACTERS = {
    'Шаман': Shaman,
    'Друид': Druid,
    'Охотник': Hunter,
    'Маг': Mage,
}

is_battle_mode: bool = False
cooldown = {}
character: Character = None
monster: Character = None
current_user_id = None
dungeon_cooldowns = {}

TIME_PATTERN = r"^([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]$"
NAME_PATTERN = r'^[А-Яа-яЁё]+$'

json_manager = JSONDataManager()
xml_manager = XMLDataManager()


def is_valid_time_format(time_str: str) -> bool:
    """
    Проверяет, соответствует ли строка формату времени ЧЧ:ММ:СС с помощью регулярного выражения.

    Args:
        time_str (str): Строка с временем для проверки.

    Returns:
        bool: True, если строка соответствует формату времени, иначе False.
    """
    return bool(re.fullmatch(TIME_PATTERN, time_str))


def is_valid_name(name_str: str) -> bool:
    """
    Проверяет, соответствует ли строка формату имени персонажа (только русские буквы).

    Args:
        name_str (str): Строка с именем для проверки.

    Returns:
        bool: True, если строка соответствует формату имени, иначе False.
    """
    return bool(re.fullmatch(NAME_PATTERN, name_str))


def can_enter_special_dungeon(user_id: int) -> tuple[bool, str]:
    """
    Проверяет, может ли пользователь войти в особое подземелье.

    Пользователь может входить в подземелье раз в 4 часа реального времени.

    Args:
        user_id (int): ID пользователя.

    Returns:
        tuple[bool, str]: Кортеж из флага доступа (True/False) и сообщения для пользователя.
    """
    current_time = datetime.now()

    if user_id not in dungeon_cooldowns:
        dungeon_cooldowns[user_id] = current_time
        next_available = current_time + timedelta(hours=4)
        return True, f"Ты вошел в особое подземелье! Следующий вход будет доступен после {next_available.strftime('%H:%M:%S')}."

    last_entry = dungeon_cooldowns[user_id]
    time_diff = current_time - last_entry

    if time_diff >= timedelta(hours=4):
        dungeon_cooldowns[user_id] = current_time
        next_available = current_time + timedelta(hours=4)
        return True, f"Ты вошел в особое подземелье! Следующий вход будет доступен после {next_available.strftime('%H:%M:%S')}."
    else:
        remaining_time = timedelta(hours=4) - time_diff
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return False, f"Подземелье недоступно. Следующий вход возможен через {hours:02d}:{minutes:02d}:{seconds:02d}."


def handler_filter(message: types.Message) -> bool:
    """
    Фильтр для проверки, является ли текст сообщения выбором класса.

    Args:
        message (types.Message): Объект сообщения от пользователя.

    Returns:
        bool: True, если текст сообщения совпадает с одним из названий классов, иначе False.
    """
    for name in CHARACTERS.keys():
        if name == message.text:
            return True
    return False


def init_village_markup():
    """
    Создает клавиатуру главного меню (деревни).

    Returns:
        types.ReplyKeyboardMarkup: Объект клавиатуры с кнопками действий.
    """
    village_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    lvlup_button = types.KeyboardButton('Повысить уровень')
    battle_button = types.KeyboardButton('Отправиться на охоту за монстрами')
    special_dungeon_button = types.KeyboardButton('Особое подземелье')
    change_class_button = types.KeyboardButton('Смена класса')
    save_json_button = types.KeyboardButton('Сохранить в JSON')
    save_xml_button = types.KeyboardButton('Сохранить в XML')
    load_json_button = types.KeyboardButton('Загрузить из JSON')
    load_xml_button = types.KeyboardButton('Загрузить из XML')
    village_markup.add(lvlup_button, battle_button, special_dungeon_button)
    village_markup.add(change_class_button)
    village_markup.add(save_json_button, save_xml_button)
    village_markup.add(load_json_button, load_xml_button)
    return village_markup


def change_class_markup():
    """
    Создает клавиатуру для выбора класса персонажа.

    Returns:
        types.ReplyKeyboardMarkup: Объект клавиатуры с кнопками классов.
    """
    change_class_reply_keyboard_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_shaman = types.KeyboardButton('Шаман')
    button_hunter = types.KeyboardButton('Охотник')
    button_druid = types.KeyboardButton('Друид')
    button_mage = types.KeyboardButton('Маг')
    change_class_reply_keyboard_markup.add(button_shaman, button_druid, button_hunter, button_mage)
    return change_class_reply_keyboard_markup


def battle_markup(character: Character):
    """
    Создает клавиатуру боевого меню с атакой, защитой и способностями.

    Args:
        character (Character): Объект персонажа, чьи способности будут отображены.

    Returns:
        types.ReplyKeyboardMarkup: Объект клавиатуры с боевыми действиями.
    """
    battle_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    abilities = [types.KeyboardButton(ability) for ability in character.abilities.keys()]
    attack_button = types.KeyboardButton('Атаковать')
    defend = types.KeyboardButton('Защищаться')
    battle_reply_markup.add(attack_button, defend)
    for ability in abilities:
        battle_reply_markup.add(ability)
    return battle_reply_markup


def main():
    """
    Основная функция инициализации и запуска Telegram бота.

    Настраивает обработчики команд и сообщений, запускает polling бота.
    """
    bot = TeleBot(API_TOKEN)

    @bot.message_handler(commands=['start'])
    def start(message: types.Message):
        """
        Обработчик команды /start.

        Приветствует пользователя и предлагает выбрать класс персонажа.
        Устанавливает ID текущего пользователя.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global current_user_id
        current_user_id = message.from_user.id
        try:
            bot.reply_to(
                message=message,
                text='Добро пожаловать в наш мир путник. Здесь тебя ждут приключения, опасности и огромная сила. Удачи!',
                reply_markup=change_class_markup()
            )
        except Exception as e:
            print(f"Ошибка при отправке сообщения: {e}")

    @bot.message_handler(func=lambda menu: True if menu.text == 'Смена класса' else False)
    def transfer_to_choosing(message: types.Message):
        """
        Обработчик сообщения 'Смена класса'.

        Позволяет пользователю вернуться к выбору класса, если он не в бою.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global character
        try:
            if not is_battle_mode:
                start(message)
            else:
                bot.send_message(message.chat.id, 'Извини, класс сменить нельзя, пока ты в бою')
        except Exception as e:
            print(f"Ошибка при смене класса: {e}")

    @bot.message_handler(func=handler_filter)
    def choose_class(message: types.Message):
        """
        Обработчик выбора класса персонажа.

        Создает экземпляр выбранного класса и запрашивает имя персонажа.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global character
        try:
            character = CHARACTERS[message.text](name=f"Temp_{message.from_user.id}")
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Ты выбрал класс {message.text}. Введите имя вашего персонажа (только русские буквы):',
            )
        except Exception as e:
            print(f"Ошибка при выборе класса: {e}")

    @bot.message_handler(func=lambda message: message.text and not handler_filter(message) and
                                              message.text not in ['Повысить уровень',
                                                                   'Отправиться на охоту за монстрами',
                                                                   'Особое подземелье',
                                                                   'Смена класса', 'Сохранить в JSON',
                                                                   'Сохранить в XML',
                                                                   'Загрузить из JSON', 'Загрузить из XML', 'Атаковать',
                                                                   'Защищаться'])
    def set_character_name(message: types.Message):
        """
        Обработчик ввода имени персонажа.

        Проверяет имя на корректность и устанавливает его персонажу.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global character
        try:
            if character and character.name.startswith("Temp_"):
                if is_valid_name(message.text):
                    character.name = message.text
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=f'Отлично! Твое имя: {character.name}. Ты можешь отправиться в деревню.',
                        reply_markup=init_village_markup()
                    )
                else:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text='Имя должно содержать только русские буквы (заглавные или строчные). Пожалуйста, введите имя заново:'
                    )
            else:
                pass
        except Exception as e:
            print(f"Ошибка при установке имени: {e}")

    @bot.message_handler(func=lambda menu: True if menu.text == 'Повысить уровень' else False)
    def level_up(message: types.Message):
        """
        Обработчик сообщения 'Повысить уровень'.

        Повышает уровень персонажа, если у него достаточно опыта.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global character
        try:
            if character:
                if character.characteristics['exp'] >= 100:
                    response = character.level_up()
                    bot.send_message(chat_id=message.chat.id, text=response)
                else:
                    bot.send_message(chat_id=message.chat.id, text='У тебя пока недостаточно опыта')
            else:
                bot.send_message(chat_id=message.chat.id, text='Сначала выбери класс.')
        except Exception as e:
            print(f"Ошибка при повышении уровня: {e}")

    @bot.message_handler(func=lambda menu: True if menu.text == 'Отправиться на охоту за монстрами' else False)
    def battle(message: types.Message):
        """
        Обработчик начала боя.

        Создает монстра соответствующего уровня и переводит игрока в боевой режим.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global is_battle_mode, monster, character
        try:
            if not character:
                bot.send_message(chat_id=message.chat.id, text='Сначала выбери класс.')
                return

            is_battle_mode = True
            character.reset()
            monster = Character(name="Monster", lvl=character.characteristics['lvl'] + 2)
            bot.send_message(
                chat_id=message.chat.id,
                text=f"Из-за угла выскакивает готовое к бою чудовище, судя по его виду ты можешь определить, что его: "
                     f"сила ~ {monster.characteristics['power']}, а живучесть ~ {monster.characteristics['max_health']} "
                     f"Приготовься к бою!",
                reply_markup=battle_markup(character)
            )
        except Exception as e:
            print(f"Ошибка при начале боя: {e}")

    @bot.message_handler(func=lambda menu: True if menu.text == 'Особое подземелье' else False)
    def special_dungeon(message: types.Message):
        """
        Обработчик входа в особое подземелье.

        Проверяет, прошло ли 4 часа с последнего посещения, и предоставляет доступ
        к особому контенту с уникальными монстрами и наградами.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global character, is_battle_mode, monster
        try:
            if not character:
                bot.send_message(chat_id=message.chat.id, text='Сначала выбери класс.')
                return

            can_enter, response_message = can_enter_special_dungeon(message.from_user.id)
            bot.send_message(chat_id=message.chat.id, text=response_message)

            if can_enter:
                is_battle_mode = True
                character.reset()
                monster = Character(name="Ancient Guardian",
                                    lvl=character.characteristics['lvl'] + 5)

                monster.characteristics['exp_reward'] = monster.characteristics['lvl'] * 30

                bot.send_message(
                    chat_id=message.chat.id,
                    text=f"Ты входишь в таинственное подземелье, охраняемое древним стражем. "
                         f"Его сила ~ {monster.characteristics['power']}, "
                         f"а живучесть ~ {monster.characteristics['max_health']}. "
                         f"Приготовься к тяжелому бою!",
                    reply_markup=battle_markup(character)
                )
            else:
                bot.send_message(chat_id=message.chat.id, text='Ты возвращаешься в деревню.',
                                 reply_markup=init_village_markup())
        except Exception as e:
            print(f"Ошибка при входе в особое подземелье: {e}")

    @bot.message_handler(func=lambda menu: True if menu.text == 'Атаковать' else False)
    def attack(message: types.Message):
        """
        Обработчик атаки персонажа.

        Выполняет атаку по монстру, обновляет здоровье монстра и проверяет его смерть.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global is_battle_mode, monster, character
        try:
            if not character or not monster:
                bot.send_message(chat_id=message.chat.id, text='Что-то пошло не так, начни бой заново.')
                return

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
                cooldown[message.chat.id] = cooldown.get(message.chat.id, 0) + 1
            else:
                if hasattr(monster, 'exp_reward'):
                    exp_gained = monster.exp_reward
                else:
                    exp_gained = monster.characteristics["lvl"] * 15

                character.gain_exp(exp_gained)
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'Размашистый удар раскалывает череп чудовища. '
                         f'{monster.__del__()}',
                    reply_markup=init_village_markup()
                )
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'Ты получил {exp_gained} опыта'
                )
                is_battle_mode = False
                monster = None
        except Exception as e:
            print(f"Ошибка при атаке: {e}")

    @bot.message_handler(func=lambda menu: True if menu.text == 'Защищаться' else False)
    def defence(message: types.Message):
        """
        Обработчик защиты персонажа.

        Выполняет защиту от атаки монстра, обновляет здоровье персонажа и проверяет его смерть.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global character, is_battle_mode
        try:
            if not character or not monster:
                bot.send_message(chat_id=message.chat.id, text='Что-то пошло не так, начни бой заново.')
                return

            results = character.defence(monster.characteristics['power'])
            character.characteristics['health'] = results['hp']
            if character.characteristics['health'] >= 0:
                if results['is_crit']:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=f'Уворот оказывается успешным и благодаря выигранному времени ты заходишь за спину '
                             f'противника!'
                             f'У тебя остается {character.characteristics["health"]} жизней и инициатива на твоей '
                             f'стороне,'
                             f'пока монстр пытается вытащить оружие!'
                    )
                else:
                    bot.send_message(
                        chat_id=message.chat.id,
                        text=f'Уворот оказывается неудачным! У тебя остается {character.characteristics["health"]} жизней!'
                    )
                cooldown[message.chat.id] = cooldown.get(message.chat.id, 0) + 1
            else:
                bot.send_message(chat_id=message.chat.id, text=character.__del__())
                is_battle_mode = False
        except Exception as e:
            print(f"Ошибка при защите: {e}")

    @bot.message_handler(
        func=lambda ability: True if character and ability.text in character.abilities.keys() else False)
    def abilities_list(message: types.Message):
        """
        Обработчик использования способности персонажа.

        Активирует выбранную способность персонажа.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global character
        try:
            if not character:
                return
            result = character.abilities[message.text](switcher=True)
            if result is None or result is True:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'Ты успешно использовал способность {message.text}, твоё тело наливается силой'
                )
                cooldown[message.chat.id] = 0
                cooldown['ability'] = f'{message.text}'
            else:
                bot.send_message(
                    chat_id=message.chat.id,
                    text=f'Тебе не удается использовать скрытую внутри тебя силу.'
                )
        except Exception as e:
            print(f"Ошибка при использовании способности: {e}")

    @bot.message_handler(func=lambda message: True if cooldown.get(message.chat.id) == 2 else False)
    def off_ability(message: types.Message):
        """
        Обработчик деактивации способности по истечении кулдауна.

        Деактивирует использованную способность персонажа.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global character
        try:
            if not character or 'ability' not in cooldown:
                return
            bot.send_message(
                chat_id=message.chat.id,
                text=f'Время действия способности {cooldown["ability"]} прошло'
            )
            character.abilities[cooldown["ability"]](switcher=False)
        except Exception as e:
            print(f"Ошибка при деактивации способности: {e}")

    @bot.message_handler(func=lambda m: m.text == 'Сохранить в JSON')
    def save_json(message: types.Message):
        """
        Обработчик сохранения персонажа в JSON-файл.

        Сохраняет текущего персонажа в файл с именем, основанным на ID пользователя.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global character
        try:
            if not character:
                bot.send_message(chat_id=message.chat.id, text='Нет персонажа для сохранения.')
                return
            filename = f"character_{message.from_user.id}.json"
            success = json_manager.create(character, filename)
            if success:
                bot.send_message(chat_id=message.chat.id, text=f'Персонаж сохранен в {filename}')
            else:
                bot.send_message(chat_id=message.chat.id, text='Ошибка при сохранении.')
        except DataStorageError as e:
            bot.send_message(chat_id=message.chat.id, text=f'Ошибка хранения данных: {e}')
        except Exception as e:
            print(f"Ошибка при сохранении в JSON: {e}")
            bot.send_message(chat_id=message.chat.id, text='Произошла ошибка при сохранении.')

    @bot.message_handler(func=lambda m: m.text == 'Сохранить в XML')
    def save_xml(message: types.Message):
        """
        Обработчик сохранения персонажа в XML-файл.

        Сохраняет текущего персонажа в файл с именем, основанным на ID пользователя.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global character
        try:
            if not character:
                bot.send_message(chat_id=message.chat.id, text='Нет персонажа для сохранения.')
                return
            filename = f"character_{message.from_user.id}.xml"
            success = xml_manager.create(character, filename)
            if success:
                bot.send_message(chat_id=message.chat.id, text=f'Персонаж сохранен в {filename}')
            else:
                bot.send_message(chat_id=message.chat.id, text='Ошибка при сохранении.')
        except DataStorageError as e:
            bot.send_message(chat_id=message.chat.id, text=f'Ошибка хранения данных: {e}')
        except Exception as e:
            print(f"Ошибка при сохранении в XML: {e}")
            bot.send_message(chat_id=message.chat.id, text='Произошла ошибка при сохранении.')

    @bot.message_handler(func=lambda m: m.text == 'Загрузить из JSON')
    def load_json(message: types.Message):
        """
        Обработчик загрузки персонажа из JSON-файла.

        Загружает персонажа из файла с именем, основанным на ID пользователя.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global character
        try:
            filename = f"character_{message.from_user.id}.json"
            if not os.path.exists(filename):
                bot.send_message(chat_id=message.chat.id, text=f'Файл {filename} не найден.')
                return
            character = json_manager.read(filename)
            bot.send_message(chat_id=message.chat.id,
                             text=f'Персонаж загружен из {filename}. Текущий уровень: {character.characteristics["lvl"]}')
        except DataStorageError as e:
            bot.send_message(chat_id=message.chat.id, text=f'Ошибка хранения данных: {e}')
        except Exception as e:
            print(f"Ошибка при загрузке из JSON: {e}")
            bot.send_message(chat_id=message.chat.id, text='Произошла ошибка при загрузке.')

    @bot.message_handler(func=lambda m: m.text == 'Загрузить из XML')
    def load_xml(message: types.Message):
        """
        Обработчик загрузки персонажа из XML-файла.

        Загружает персонажа из файла с именем, основанным на ID пользователя.

        Args:
            message (types.Message): Объект сообщения от пользователя.
        """
        global character
        try:
            filename = f"character_{message.from_user.id}.xml"
            if not os.path.exists(filename):
                bot.send_message(chat_id=message.chat.id, text=f'Файл {filename} не найден.')
                return
            character = xml_manager.read(filename)
            bot.send_message(chat_id=message.chat.id,
                             text=f'Персонаж загружен из {filename}. Текущий уровень: {character.characteristics["lvl"]}')
        except DataStorageError as e:
            bot.send_message(chat_id=message.chat.id, text=f'Ошибка хранения данных: {e}')
        except Exception as e:
            print(f"Ошибка при загрузке из XML: {e}")
            bot.send_message(chat_id=message.chat.id, text='Произошла ошибка при загрузке.')

    print("Bot is running...")
    bot.infinity_polling()


if __name__ == '__main__':
    def save_dungeon_times_to_file():
        """Сохраняет время последнего посещения подземелья в файл."""
        try:
            with open('dungeon_times.txt', 'w', encoding='utf-8') as f:
                for user_id, time_obj in dungeon_cooldowns.items():
                    f.write(f"{user_id}:{time_obj.strftime('%Y-%m-%d %H:%M:%S')}\n")
        except Exception as e:
            print(f"Ошибка при сохранении времени посещений: {e}")


    def load_dungeon_times_from_file():
        """Загружает время последнего посещения подземелья из файла."""
        try:
            if os.path.exists('dungeon_times.txt'):
                with open('dungeon_times.txt', 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            parts = line.split(':')
                            if len(parts) == 2:
                                user_id = int(parts[0])
                                time_str = parts[1]
                                try:
                                    time_obj = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
                                    dungeon_cooldowns[user_id] = time_obj
                                except ValueError:
                                    print(f"Некорректный формат времени в файле для user_id {user_id}: {time_str}")
                                    dungeon_cooldowns[user_id] = datetime.now()
            else:
                with open('dungeon_times.txt', 'w', encoding='utf-8') as f:
                    pass
        except Exception as e:
            print(f"Ошибка при загрузке времени посещений: {e}")
            dungeon_cooldowns.clear()


    load_dungeon_times_from_file()

    import atexit

    atexit.register(save_dungeon_times_to_file)

    main()
