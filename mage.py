from character import Character
from random import randint
class Mage(Character):
    def __init__(self) -> None:
        self.characteristics = {
            'max_health':10,
            'health':10,
            'power':90,
            'exp':0,
            'lvl':1,
            'crit_chance':20,
            'def_chance':20,
            'coefficent':0.1,
        }

    def fireball(self) -> int:
        if randint(1, 100) <= self.characteristics['crit_chance']*2:
            return self.characteristics['power']*3
        
    def __del__(self) -> str:
        return 'Твой жизненный путь завершен'