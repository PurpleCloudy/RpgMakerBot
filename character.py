from random import randint

class Character():
    def __init__(self):
        self.characteristics = {
            'max_health':0,
            'health':0,
            'power':0,
            'exp':0,
            'lvl':1,
            'crit_chance':5,
            'def_chance':15,
            'coefficent':0.1,
        }

    def attack(self, mob_hp):
        if randint(1, 100) <= self.characteristics['crit_chance']:
            return mob_hp - self.power*2
        else:
            return mob_hp - self.power
    
    def defence(self, mob_power):
        if randint(1, 100) <= self.characteristics['def_chance']:
            return self.characteristics['health']
        else:
            return self.characteristics['health'] - mob_power
        
    def level_up(self):
        if self.characteristics['lvl'] < 25:
            self.characteristics['lvl'] += 1
            self.characteristics['max_health'] *= 1.1
            self.characteristics['power'] *= 1.1
            self.characteristics['crit_chance'] += 1
            self.characteristics['def_chance'] += 2
            self.characteristics['exp'] = 0
            self.characteristics['health'] = self.characteristics['max_health']
            return 'Поздравляю, герой, ты стал еще сильнее!'
        else:
            return 'Герой, ты уже слишком силен'
        
    def __del__(self):
        print()

            
