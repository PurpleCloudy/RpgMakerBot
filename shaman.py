from character import Character
from typing import Dict, Any


class Shaman(Character):
    def __init__(self, name: str = "Shaman") -> None:
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
        try:
            if switcher:
                self.characteristics['def_chance'] += 30
            else:
                self.characteristics['def_chance'] -= 30
        except Exception as e:
            print(f"Ошибка при использовании способности 'Щит природы': {e}")

    def __del__(self) -> str:
        return 'Твой жизненный путь завершен'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Shaman':
        instance = cls.__new__(cls)
        instance.name = data.get('name', 'Shaman')
        instance.characteristics = data.get('characteristics', {})
        instance.abilities = {
            'Щит природы': instance.flora_shield
        }
        return instance
