class CharacterError(Exception):
    pass


class SerializationError(Exception):
    pass


class DataStorageError(Exception):
    pass


class InvalidCharacterClassError(CharacterError):
    pass


class BattleError(Exception):
    pass
