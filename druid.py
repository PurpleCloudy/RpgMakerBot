"""
Модуль класса Друид для RPG-игры.

Содержит реализацию класса Druid, наследуемого от базового класса Character,
с уникальными характеристиками и способностью 'Вызов духов'.
"""

from character import Character
from typing import Dict, Any


class Druid(Character):
    """
    Класс, представляющий персонажа класса Друид.

    Наследуется от базового класса Character и определяет начальные
    характеристики и уникальные способности друида.
    """

    def __init__(self, name: str = "Druid") -> None:
        """
        Инициализирует экземпляр класса Druid.

        Устанавливает начальные характеристики и доступные способности.

        Args:
            name (str): Имя персонажа. По умолчанию 'Druid'.
        """
        super().__init__(name, lvl=2)
        self.characteristics.update({
            'max_health': 70,
            'health': 70,
            'power': 30,
            'exp': 0,
            'lvl': 1,
            'crit_chance': 7,
            'def_chance': 30,
            'coefficent': 0.1,
            'cool_down': 3,
            'initiative': False,
        })

        self.abilities = {
            'Вызов духов': self.spirit_calling,
        }

    def spirit_calling(self, switcher: bool) -> None:
        """
        Переключает активность способности 'Вызов духов'.

        При активации увеличивает силу на 20, при деактивации - уменьшает.

        Args:
            switcher (bool): Если True, активирует способность, иначе деактивирует.
        """
        try:
            if switcher:
                self.characteristics['power'] += 20
            else:
                self.characteristics['power'] -= 20
        except Exception as e:
            print(f"Ошибка при использовании способности 'Вызов духов': {e}")

    def __del__(self) -> str:
        """
        Возвращает строку при удалении экземпляра класса.

        Returns:
            str: Сообщение о завершении жизненного пути персонажа.
        """
        return 'Твой жизненный путь завершен'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Druid':
        """
        Создает экземпляр класса Druid из словаря данных.

        Args:
            data (Dict[str, Any]): Словарь с данными персонажа.

        Returns:
            Druid: Экземпляр класса Druid.
        """
        instance = cls.__new__(cls)
        instance.name = data.get('name', 'Druid')
        instance.characteristics = data.get('characteristics', {})
        instance.abilities = {
            'Вызов духов': instance.spirit_calling
        }
        return instance
