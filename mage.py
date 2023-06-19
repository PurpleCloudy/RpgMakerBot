from character import Character

class Shaman(Character):
    def __init__(self):
        self.characteristics = {
            'max_health':10,
            'health':10,
            'power':90,
            'exp':0,
            'lvl':1,
            'crit_chance':5,
            'def_chance':15,
            'coefficent':0.1,
        }