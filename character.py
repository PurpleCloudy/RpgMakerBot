from random import randint


class Character:
    def __init__(self, lvl) -> None:
        self.characteristics = {
            'max_health': lvl * 10,
            'health': lvl * 10,
            'power': lvl * 5,
            'exp': 0,
            'lvl': lvl,
            'crit_chance': lvl * 2,
            'def_chance': lvl * 4,
            'coefficent': 0.1,
            'initiative': False,
        }
        
        self.abilities = dict()

    def attack(self, mob_hp: int) -> dict:
        if (randint(1, 100) <= self.characteristics['crit_chance'] or
           (randint(1, 50) <= self.characteristics['crit_chance'] and self.characteristics['initiative'])):
            self.characteristics['initiative'] = False
            return {'hp': mob_hp - self.characteristics['power'] * 2, 'is_crit': True}
        else:
            return {'hp': mob_hp - self.characteristics['power'], 'is_crit': False}
    
    def defence(self, mob_power: int) -> dict:
        if randint(1, 100) <= self.characteristics['def_chance']:
            self.characteristics['initiative'] = True
            return {'hp': self.characteristics['health'], 'is_crit': True}
        else:
            return {'hp': self.characteristics['health'] - mob_power, 'is_crit': False}
        
    def level_up(self) -> str:
        if self.characteristics['lvl'] < 25:
            self.characteristics['lvl'] += 1
            self.characteristics['max_health'] *= 1.1
            self.characteristics['power'] *= 1.1
            self.characteristics['crit_chance'] += 1
            self.characteristics['def_chance'] += 2
            self.characteristics['exp'] -= 100
            self.characteristics['health'] = self.characteristics['max_health']
            return 'Поздравляю, герой, ты стал еще сильнее!'
        else:
            return 'Герой, ты уже слишком силен'
        
    def __del__(self) -> str:
        return 'Монстр мертв, жители торжествуют!'

            
