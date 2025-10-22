from character import Character
from typing import Dict, Any, Optional
import random


class Mage(Character):
    def __init__(self, name: str = "Mage") -> None:
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
        return 'Твой жизненный путь завершен'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Mage':
        instance = cls.__new__(cls)
        instance.name = data.get('name', 'Mage')
        instance.characteristics = data.get('characteristics', {})
        instance.abilities = {
            'Огненный шар': instance.fireball
        }
        return instance
