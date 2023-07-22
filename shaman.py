from character import Character


class Shaman(Character):
    def __init__(self) -> None:
        super().__init__(lvl=1)
        self.characteristics = {
            'max_health': 90,
            'health': 90,
            'power': 10,
            'exp': 0,
            'lvl': 1,
            'crit_chance': 5,
            'def_chance': 40,
            'coefficent': 0.1,
            'cool down': 3,
            'initiative': False,
        }
    
        self.abilities = {
            'Щит природы': self.flora_shield,
        }

    def flora_shield(self, switcher) -> None:
        if switcher:
            self.characteristics['def_chance'] += 30
        else:
            self.characteristics['def_chance'] -= 30
    
    def __del__(self) -> str:
        return 'Твой жизненный путь завершен'
