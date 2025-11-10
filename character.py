"""
Модуль базового класса персонажа для RPG-игры.

Содержит абстрактный класс Character с основной логикой боя,
уровня персонажа и управления характеристиками.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import random


class Character(ABC):
    """
    Абстрактный базовый класс для всех персонажей игры.

    Определяет общие характеристики, методы боя, повышения уровня
    и управления состоянием персонажа.
    """

    def __init__(self, name: str, lvl: int) -> None:
        """
        Инициализирует экземпляр класса Character.

        Args:
            name (str): Имя персонажа.
            lvl (int): Начальный уровень персонажа.
        """
        self.name = name
        self.characteristics: Dict[str, Any] = {
            'max_health': lvl * 10,
            'health': lvl * 10,
            'power': lvl * 5,
            'exp': 0,
            'lvl': lvl,
            'crit_chance': lvl * 2,
            'def_chance': lvl * 4,
            'coefficient': 0.1,
            'initiative': False,
        }
        self.abilities: Dict[str, callable] = {}

    def attack(self, mob_hp: int) -> Dict[str, Any]:
        """
        Выполняет атаку по монстру.

        Рассчитывает урон с учетом шанса критического удара и инициативы.

        Args:
            mob_hp (int): Текущее здоровье монстра.

        Returns:
            Dict[str, Any]: Словарь с новым здоровьем монстра и флагом крита.
        """
        try:
            if (random.randint(1, 100) <= self.characteristics['crit_chance'] or
                    (random.randint(1, 50) <= self.characteristics['crit_chance'] and self.characteristics[
                        'initiative'])):
                self.characteristics['initiative'] = False
                return {'hp': mob_hp - self.characteristics['power'] * 2, 'is_crit': True}
            else:
                return {'hp': mob_hp - self.characteristics['power'], 'is_crit': False}
        except Exception as e:
            print(f"Ошибка при атаке: {e}")
            return {'hp': mob_hp, 'is_crit': False}

    def defence(self, mob_power: int) -> Dict[str, Any]:
        """
        Выполняет защиту от атаки монстра.

        Рассчитывает полученный урон с учетом шанса уклонения.

        Args:
            mob_power (int): Сила атаки монстра.

        Returns:
            Dict[str, Any]: Словарь с новым здоровьем персонажа и флагом уклонения.
        """
        try:
            if random.randint(1, 100) <= self.characteristics['def_chance']:
                self.characteristics['initiative'] = True
                return {'hp': self.characteristics['health'], 'is_crit': True}
            else:
                return {'hp': self.characteristics['health'] - mob_power, 'is_crit': False}
        except Exception as e:
            print(f"Ошибка при защите: {e}")
            return {'hp': self.characteristics['health'], 'is_crit': False}

    def level_up(self) -> str:
        """
        Повышает уровень персонажа и улучшает его характеристики.

        Увеличивает здоровье, силу, шансы крита и уклонения, сбрасывает опыт.

        Returns:
            str: Сообщение о результате повышения уровня.
        """
        try:
            if self.characteristics['lvl'] < 25:
                self.characteristics['lvl'] += 1
                self.characteristics['max_health'] = int(self.characteristics['max_health'] * 1.1)
                self.characteristics['power'] = int(self.characteristics['power'] * 1.1)
                self.characteristics['crit_chance'] += 1
                self.characteristics['def_chance'] += 2
                self.characteristics['exp'] -= 100
                self.characteristics['health'] = self.characteristics['max_health']
                return 'Поздравляю, герой, ты стал еще сильнее!'
            else:
                return 'Герой, ты уже слишком силен'
        except Exception as e:
            print(f"Ошибка при повышении уровня: {e}")
            return 'Произошла ошибка при попытке повысить уровень.'

    def gain_exp(self, exp_amount: int) -> None:
        """
        Добавляет персонажу опыт.

        Args:
            exp_amount (int): Количество опыта для добавления.
        """
        try:
            self.characteristics['exp'] += exp_amount
        except Exception as e:
            print(f"Ошибка при получении опыта: {e}")

    def reset(self) -> None:
        """
        Сбрасывает состояние персонажа к начальному для нового боя.

        Восстанавливает здоровье до максимального и сбрасывает инициативу.
        """
        try:
            self.characteristics['health'] = self.characteristics['max_health']
            self.characteristics['initiative'] = False
        except Exception as e:
            print(f"Ошибка при сбросе состояния: {e}")

    def to_dict(self) -> Dict[str, Any]:
        """
        Преобразует объект персонажа в словарь.

        Returns:
            Dict[str, Any]: Словарь с данными персонажа.
        """
        return {
            'type': self.__class__.__name__,
            'name': self.name,
            'characteristics': self.characteristics.copy(),
            'abilities': list(self.abilities.keys())
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Character':
        """
        Создает экземпляр класса Character из словаря данных.

        Args:
            data (Dict[str, Any]): Словарь с данными персонажа.

        Returns:
            Character: Экземпляр класса Character.
        """
        instance = cls.__new__(cls)
        instance.name = data.get('name', 'Unknown')
        instance.characteristics = data.get('characteristics', {})
        instance.abilities = {name: lambda s: None for name in data.get('abilities', [])}
        return instance

    def __del__(self) -> str:
        """
        Возвращает строку при удалении экземпляра класса.

        Returns:
            str: Сообщение о смерти монстра.
        """
        return 'Монстр мертв, жители торжествуют!'
