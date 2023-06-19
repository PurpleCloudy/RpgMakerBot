from character import Character

class Shaman(Character):
    def __init__(self):
        self.characteristics = {
            'max_health':50,
            'health':50,
            'power':50,
            'exp':0,
            'lvl':1,
            'crit_chance':5,
            'def_chance':15,
            'coefficent':0.1,
        }