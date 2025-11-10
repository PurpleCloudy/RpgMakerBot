"""
Модуль класса Шаман для RPG-игры.

Содержит реализацию класса Shaman, наследуемого от базового класса Character,
с уникальными характеристиками и способностью 'Щит природы'.
"""

from character import Character
from typing import Dict, Any


class Shaman(Character):
    """
    Класс, представляющий персонажа класса Шаман.

    Наследуется от базового класса Character и определяет начальные
    характеристики и уникальные способности шамана.
    """

    def __init__(self, name: str = "Shaman") -> None:
        """
        Инициализирует экземпляр класса Shaman.

        Устанавливает начальные характеристики и доступные способности.

        Args:
            name (str): Имя персонажа. По умолчанию 'Shaman'.
        """
        super().__init__(name, lvl=1)
        self.characteristics.update({
            'max_health': 90,
            'health': 90,
            'power': 10,
            'exp': 0,
            'lvl': 1,
            'crit_chance': 5,
            'def_chance': 40,
            'coefficent': 0.1,
            'cool_down': 3,
            'initiative': False,
        })

        self.abilities = {
            'Щит природы': self.flora_shield,
        }

    def flora_shield(self, switcher: bool) -> None:
        """
        Переключает активность способности 'Щит природы'.

        При активации увеличивает шанс уклонения на 30, при деактивации - уменьшает.

        Args:
            switcher (bool): Если True, активирует способность, иначе деактивирует.
        """
        try:
            if switcher:
                self.characteristics['def_chance'] += 30
            else:
                self.characteristics['def_chance'] -= 30
        except Exception as e:
            print(f"Ошибка при использовании способности 'Щит природы': {e}")

    def __del__(self) -> str:
        """
        Возвращает строку при удалении экземпляра класса.

        Returns:
            str: Сообщение о завершении жизненного пути персонажа.
        """
        return 'Твой жизненный путь завершен'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Shaman':
        """
        Создает экземпляр класса Shaman из словаря данных.

        Args:
            data (Dict[str, Any]): Словарь с данными персонажа.

        Returns:
            Shaman: Экземпляр класса Shaman.
        """
        instance = cls.__new__(cls)
        instance.name = data.get('name', 'Shaman')
        instance.characteristics = data.get('characteristics', {})
        instance.abilities = {
            'Щит природы': instance.flora_shield
        }
        return instance
