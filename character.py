from random import randint

class Character():
    def __init__(self, lvl) -> None:
        self.characteristics = {
            'max_health':lvl*10,
            'health':lvl*10,
            'power':lvl*5,
            'exp':0,
            'lvl':lvl,
            'crit_chance':lvl*2,
            'def_chance':lvl*4,
            'coefficent':0.1,
            'initiative':False,
        }

    def attack(self, mob_hp:int) -> int:
        if randint(1, 100) <= self.characteristics['crit_chance'] or (randint(1, 50) <= self.characteristics['crit_chance'] and self.characteristics['initiative']):
            self.characteristics['initiative'] = False
            return mob_hp - self.power*2
        else:
            return mob_hp - self.power
    
    def defence(self, mob_power:int) -> int:
        if randint(1, 100) <= self.characteristics['def_chance']:
            self.characteristics['initiative'] = True
            return self.characteristics['health']
        else:
            return self.characteristics['health'] - mob_power
        
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

            
