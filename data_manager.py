import json
import xml.etree.ElementTree as ET
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
from exceptions import SerializationError, DataStorageError
from character import Character
from shaman import Shaman
from mage import Mage
from druid import Druid
from hunter import Hunter


CHARACTER_TYPES = {
    'Shaman': Shaman,
    'Mage': Mage,
    'Druid': Druid,
    'Hunter': Hunter
}


class DataSerializer(ABC):
    @abstractmethod
    def serialize(self, character: Character) -> str:
        pass

    @abstractmethod
    def deserialize(self, data: str) -> Character:
        pass


class JSONSerializer(DataSerializer):
    def serialize(self, character: Character) -> str:
        try:
            return json.dumps(character.to_dict(), ensure_ascii=False, indent=4)
        except Exception as e:
            raise SerializationError(f"Ошибка сериализации в JSON: {e}")

    def deserialize(self, data: str) -> Character:
        try:
            char_dict = json.loads(data)
            char_type = char_dict.get('type')
            if char_type not in CHARACTER_TYPES:
                raise SerializationError(f"Неизвестный тип персонажа: {char_type}")
            return CHARACTER_TYPES[char_type].from_dict(char_dict)
        except json.JSONDecodeError as e:
            raise SerializationError(f"Ошибка десериализации из JSON: {e}")
        except Exception as e:
            raise SerializationError(f"Ошибка десериализации из JSON: {e}")


class XMLSerializer(DataSerializer):

    def serialize(self, character: Character) -> str:
        try:
            root = ET.Element("Character")
            root.set("type", character.__class__.__name__)
            root.set("name", character.name)

            characteristics_elem = ET.SubElement(root, "Characteristics")
            for key, value in character.characteristics.items():
                attr_elem = ET.SubElement(characteristics_elem, "Attribute")
                attr_elem.set("name", key)
                attr_elem.text = str(value)

            abilities_elem = ET.SubElement(root, "Abilities")
            for ability_name in character.abilities.keys():
                ability_elem = ET.SubElement(abilities_elem, "Ability")
                ability_elem.text = ability_name

            return ET.tostring(root, encoding='unicode')
        except Exception as e:
            raise SerializationError(f"Ошибка сериализации в XML: {e}")

    def deserialize(self, data: str) -> Character:
        try:
            root = ET.fromstring(data)
            char_type = root.get("type")
            name = root.get("name")

            if char_type not in CHARACTER_TYPES:
                raise SerializationError(f"Неизвестный тип персонажа: {char_type}")

            instance = CHARACTER_TYPES[char_type].__new__(CHARACTER_TYPES[char_type])
            instance.name = name

            characteristics_elem = root.find("Characteristics")
            characteristics = {}
            for attr_elem in characteristics_elem.findall("Attribute"):
                key = attr_elem.get("name")
                val_text = attr_elem.text
                try:
                    val = int(val_text)
                except ValueError:
                    try:
                        val = float(val_text)
                    except ValueError:
                        val = val_text
                characteristics[key] = val
            instance.characteristics = characteristics

            abilities_elem = root.find("Abilities")
            abilities = {}
            for ability_elem in abilities_elem.findall("Ability"):
                ability_name = ability_elem.text
                abilities[ability_name] = lambda s: None
            instance.abilities = abilities

            return instance
        except ET.ParseError as e:
            raise SerializationError(f"Ошибка десериализации из XML: {e}")
        except Exception as e:
            raise SerializationError(f"Ошибка десериализации из XML: {e}")


class DataManager(ABC):
    def __init__(self, serializer: DataSerializer) -> None:
        self.serializer = serializer

    @abstractmethod
    def create(self, character: Character, filename: str) -> bool:
        pass

    @abstractmethod
    def read(self, filename: str) -> Character:
        pass

    @abstractmethod
    def update(self, character: Character, filename: str) -> bool:
        pass

    @abstractmethod
    def delete(self, filename: str) -> bool:
        pass


class JSONDataManager(DataManager):
    def __init__(self) -> None:
        super().__init__(JSONSerializer())

    def create(self, character: Character, filename: str) -> bool:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.serializer.serialize(character))
            return True
        except Exception as e:
            raise DataStorageError(f"Ошибка при создании файла JSON: {e}")

    def read(self, filename: str) -> Character:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = f.read()
            return self.serializer.deserialize(data)
        except FileNotFoundError:
            raise DataStorageError(f"Файл {filename} не найден.")
        except Exception as e:
            raise DataStorageError(f"Ошибка при чтении файла JSON: {e}")

    def update(self, character: Character, filename: str) -> bool:
        return self.create(character, filename)

    def delete(self, filename: str) -> bool:
        try:
            import os
            os.remove(filename)
            return True
        except FileNotFoundError:
            print(f"Файл {filename} не найден для удаления.")
            return False
        except Exception as e:
            raise DataStorageError(f"Ошибка при удалении файла JSON: {e}")


class XMLDataManager(DataManager):
    def __init__(self) -> None:
        super().__init__(XMLSerializer())

    def create(self, character: Character, filename: str) -> bool:
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.serializer.serialize(character))
            return True
        except Exception as e:
            raise DataStorageError(f"Ошибка при создании файла XML: {e}")

    def read(self, filename: str) -> Character:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = f.read()
            return self.serializer.deserialize(data)
        except FileNotFoundError:
            raise DataStorageError(f"Файл {filename} не найден.")
        except Exception as e:
            raise DataStorageError(f"Ошибка при чтении файла XML: {e}")

    def update(self, character: Character, filename: str) -> bool:
        return self.create(character, filename)

    def delete(self, filename: str) -> bool:
        try:
            import os
            os.remove(filename)
            return True
        except FileNotFoundError:
            print(f"Файл {filename} не найден для удаления.")
            return False
        except Exception as e:
            raise DataStorageError(f"Ошибка при удалении файла XML: {e}")
