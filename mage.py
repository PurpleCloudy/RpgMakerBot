from character import Character
from random import randint


class Mage(Character):
    def __init__(self) -> None:
        super().__init__(lvl=1)
        self.characteristics = {
            'max_health': 10,
            'health': 10,
            'power': 90,
            'exp': 0,
            'lvl': 1,
            'crit_chance': 20,
            'def_chance': 20,
            'coefficent': 0.1,
            'cool down': 3,
            'initiative': False,
        }

        self.abilities = {
            'Огненный шар': self.fireball,
        }

    def fireball(self, switcher:bool) -> None|bool:
        if switcher:
            if randint(1, 100) <= self.characteristics['crit_chance']*2:
                self.characteristics['power']*=3
                return True
            else:
                return False
        else:
            self.characteristics['power']//=3
        
    def __del__(self) -> str:
        return 'Твой жизненный путь завершен'
