from character import Character


class Hunter(Character):
    def __init__(self) -> None:
        super().__init__(lvl=1)
        self.characteristics = {
            'max_health': 50,
            'health': 50,
            'power': 50,
            'exp': 0,
            'lvl': 1,
            'crit_chance': 10,
            'def_chance': 50,
            'coefficent': 0.1,
            'cool down': 3,
            'initiative': False,
        }

        self.abilities = {
            'Увертливость': self.dash,
        }

    def dash(self, switcher:bool) -> None:
        if switcher:
            self.characteristics['def_chance'] += 20
        else:
            self.characteristics['def_chance'] -= 20
            
    def __del__(self) -> str:
        return 'Твой жизненный путь завершен'
