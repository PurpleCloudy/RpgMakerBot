from character import Character
from typing import Dict, Any


class Druid(Character):
    def __init__(self, name: str = "Druid") -> None:
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
        try:
            if switcher:
                self.characteristics['power'] += 20
            else:
                self.characteristics['power'] -= 20
        except Exception as e:
            print(f"Ошибка при использовании способности 'Вызов духов': {e}")

    def __del__(self) -> str:
        return 'Твой жизненный путь завершен'

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Druid':
        instance = cls.__new__(cls)
        instance.name = data.get('name', 'Druid')
        instance.characteristics = data.get('characteristics', {})
        instance.abilities = {
            'Вызов духов': instance.spirit_calling
        }
        return instance
