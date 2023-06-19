from character import Character

class Druid(Character):
    def __init__(self):
        self.characteristics = {
            'max_health':70,
            'health':70,
            'power':30,
            'exp':0,
            'lvl':1,
            'crit_chance':5,
            'def_chance':15,
            'coefficent':0.1,
        }