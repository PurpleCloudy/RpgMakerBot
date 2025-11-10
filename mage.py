"""
Модуль класса Маг для RPG-игры.

Содержит реализацию класса Mage, наследуемого от базового класса Character,
с уникальными характеристиками и способностью 'Огненный шар'.
"""

from character import Character
from typing import Dict, Any, Optional
import random


class Mage(Character):
    """
    Класс, представляющий персонажа класса Маг.

    Наследуется от базового класса Character и определяет начальные
    характеристики и уникальные способности мага.
    """

    def __init__(self, name: str = "Mage") -> None:
        """
        Инициализирует экземпляр класса Mage.

        Устанавливает начальные характеристики и доступные способности.

        Args:
            name (str): Имя персонажа. По умолчанию 'Mage'.
        """
        super().__init__(name, lvl=1)
        self.characteristics.update({
            'max_health': 10,
            'health': 10,
            'power': 90,
            'exp': 0,
            'lvl': 1,
            'crit_chance': 20,
            'def_chance': 20,
            'coefficent': 0.1,
            'cool_down': 3,
            'initiative': False,
        })

        self.abilities = {
            'Огненный шар': self.fireball,
        }

    def fireball(self, switcher: bool) -> Optional[bool]:
        """
        Переключает активность способности 'Огненный шар'.

        При активации может нанести критический урон (увеличивает силу в 3 раза),
        при деактивации возвращает силу к исходному значению.

        Args:
            switcher (bool): Если True, активирует способность, иначе деактивирует.

        Returns:
            Optional[bool]: True при критическом уроне, False при обычном,
                           None при ошибке или деактивации.
        """
        try:
            if switcher:
                if random.randint(1, 100) <= self.characteristics['crit_chance'] * 2:
                    self.characteristics['power'] *= 3
                    return True
                else:
                    return False
            else:
                self.characteristics['power'] //= 3
                return None
        except Exception as e:
            print(f"Ошибка при использовании способности 'Огненный шар': {e}")
            return None

    def __del__(self) -> str:
        """
        Возвращает строку при удалении экземпляра класса.

        Returns:
            str: Сообщение о завершении жизненного пути персонажа.
        """
        return 'Твой жизненный путь завершен'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Mage':
        """
        Создает экземпляр класса Mage из словаря данных.

        Args:
            data (Dict[str, Any]): Словарь с данными персонажа.

        Returns:
            Mage: Экземпляр класса Mage.
        """
        instance = cls.__new__(cls)
        instance.name = data.get('name', 'Mage')
        instance.characteristics = data.get('characteristics', {})
        instance.abilities = {
            'Огненный шар': instance.fireball
        }
        return instance
