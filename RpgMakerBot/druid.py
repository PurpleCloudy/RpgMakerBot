from character import Character


class Druid(Character):
    def __init__(self) -> None:
        super().__init__(lvl=2)  # Проверить соответствие архитектуры класса с SOLID
        self.characteristics = {
            'max_health': 70,
            'health': 70,
            'power': 30,
            'exp': 0,
            'lvl': 1,
            'crit_chance': 7,
            'def_chance': 30,
            'coefficent': 0.1,
            'cool down': 3,
        }

        self.abilities = {
            'Вызов духов': self.spirit_calling,
        }

    def spirit_calling(self):
        self.characteristics['power'] += 20
        return self.characteristics['power']
    
    def __del__(self) -> str:
        return 'Твой жизненный путь завершен'