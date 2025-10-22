from character import Character
from typing import Dict, Any


class Hunter(Character):
    def __init__(self, name: str = "Hunter") -> None:
        super().__init__(name, lvl=1)
        self.characteristics.update({
            'max_health': 50,
            'health': 50,
            'power': 50,
            'exp': 0,
            'lvl': 1,
            'crit_chance': 10,
            'def_chance': 50,
            'coefficent': 0.1,
            'cool_down': 3,
            'initiative': False,
        })

        self.abilities = {
            'Увертливость': self.dash,
        }

    def dash(self, switcher: bool) -> None:
        try:
            if switcher:
                self.characteristics['def_chance'] += 20
            else:
                self.characteristics['def_chance'] -= 20
        except Exception as e:
            print(f"Ошибка при использовании способности 'Увертливость': {e}")

    def __del__(self) -> str:
        return 'Твой жизненный путь завершен'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Hunter':
        instance = cls.__new__(cls)
        instance.name = data.get('name', 'Hunter')
        instance.characteristics = data.get('characteristics', {})
        instance.abilities = {
            'Увертливость': instance.dash
        }
        return instance
