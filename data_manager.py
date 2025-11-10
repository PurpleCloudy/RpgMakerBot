"""
Модуль для сериализации и управления данными персонажей в форматах JSON и XML.

Содержит абстрактные классы и конкретные реализации для сериализации
персонажей в различные форматы и управления файлами данных.
"""

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
    """
    Абстрактный класс для сериализации и десериализации персонажа.
    """

    @abstractmethod
    def serialize(self, character: Character) -> str:
        """
        Сериализует объект персонажа в строку.

        Args:
            character (Character): Объект персонажа для сериализации.

        Returns:
            str: Сериализованные данные персонажа.
        """
        pass

    @abstractmethod
    def deserialize(self, data: str) -> Character:
        """
        Десериализует строку в объект персонажа.

        Args:
            data (str): Сериализованные данные персонажа.

        Returns:
            Character: Объект персонажа.
        """
        pass


class JSONSerializer(DataSerializer):
    """
    Класс для сериализации и десериализации персонажа в формат JSON.
    """

    def serialize(self, character: Character) -> str:
        """
        Сериализует объект персонажа в JSON-строку.

        Args:
            character (Character): Объект персонажа для сериализации.

        Returns:
            str: JSON-строка с данными персонажа.

        Raises:
            SerializationError: При ошибке сериализации.
        """
        try:
            return json.dumps(character.to_dict(), ensure_ascii=False, indent=4)
        except Exception as e:
            raise SerializationError(f"Ошибка сериализации в JSON: {e}")

    def deserialize(self, data: str) -> Character:
        """
        Десериализует JSON-строку в объект персонажа.

        Args:
            data (str): JSON-строка с данными персонажа.

        Returns:
            Character: Объект персонажа.

        Raises:
            SerializationError: При ошибке десериализации.
        """
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
    """
    Класс для сериализации и десериализации персонажа в формат XML.
    """

    def serialize(self, character: Character) -> str:
        """
        Сериализует объект персонажа в XML-строку.

        Args:
            character (Character): Объект персонажа для сериализации.

        Returns:
            str: XML-строка с данными персонажа.

        Raises:
            SerializationError: При ошибке сериализации.
        """
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
        """
        Десериализует XML-строку в объект персонажа.

        Args:
            data (str): XML-строка с данными персонажа.

        Returns:
            Character: Объект персонажа.

        Raises:
            SerializationError: При ошибке десериализации.
        """
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
    """
    Абстрактный класс для управления файлами данных персонажей.
    """

    def __init__(self, serializer: DataSerializer) -> None:
        """
        Инициализирует менеджер данных с указанным сериализатором.

        Args:
            serializer (DataSerializer): Объект сериализатора.
        """
        self.serializer = serializer

    @abstractmethod
    def create(self, character: Character, filename: str) -> bool:
        """
        Создает файл с данными персонажа.

        Args:
            character (Character): Объект персонажа для сохранения.
            filename (str): Имя файла для сохранения.

        Returns:
            bool: True при успешном создании, иначе False.
        """
        pass

    @abstractmethod
    def read(self, filename: str) -> Character:
        """
        Читает персонажа из файла.

        Args:
            filename (str): Имя файла для чтения.

        Returns:
            Character: Объект персонажа.
        """
        pass

    @abstractmethod
    def update(self, character: Character, filename: str) -> bool:
        """
        Обновляет данные персонажа в файле.

        Args:
            character (Character): Объект персонажа для обновления.
            filename (str): Имя файла для обновления.

        Returns:
            bool: True при успешном обновлении, иначе False.
        """
        pass

    @abstractmethod
    def delete(self, filename: str) -> bool:
        """
        Удаляет файл с данными персонажа.

        Args:
            filename (str): Имя файла для удаления.

        Returns:
            bool: True при успешном удалении, иначе False.
        """
        pass


class JSONDataManager(DataManager):
    """
    Класс для управления файлами данных персонажей в формате JSON.
    """

    def __init__(self) -> None:
        """
        Инициализирует менеджер данных с JSON-сериализатором.
        """
        super().__init__(JSONSerializer())

    def create(self, character: Character, filename: str) -> bool:
        """
        Создает JSON-файл с данными персонажа.

        Args:
            character (Character): Объект персонажа для сохранения.
            filename (str): Имя файла для сохранения.

        Returns:
            bool: True при успешном создании, иначе False.

        Raises:
            DataStorageError: При ошибке создания файла.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.serializer.serialize(character))
            return True
        except Exception as e:
            raise DataStorageError(f"Ошибка при создании файла JSON: {e}")

    def read(self, filename: str) -> Character:
        """
        Читает персонажа из JSON-файла.

        Args:
            filename (str): Имя файла для чтения.

        Returns:
            Character: Объект персонажа.

        Raises:
            DataStorageError: При ошибке чтения файла.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = f.read()
            return self.serializer.deserialize(data)
        except FileNotFoundError:
            raise DataStorageError(f"Файл {filename} не найден.")
        except Exception as e:
            raise DataStorageError(f"Ошибка при чтении файла JSON: {e}")

    def update(self, character: Character, filename: str) -> bool:
        """
        Обновляет данные персонажа в JSON-файле.

        Args:
            character (Character): Объект персонажа для обновления.
            filename (str): Имя файла для обновления.

        Returns:
            bool: True при успешном обновлении, иначе False.

        Raises:
            DataStorageError: При ошибке обновления файла.
        """
        return self.create(character, filename)

    def delete(self, filename: str) -> bool:
        """
        Удаляет JSON-файл с данными персонажа.

        Args:
            filename (str): Имя файла для удаления.

        Returns:
            bool: True при успешном удалении, иначе False.

        Raises:
            DataStorageError: При ошибке удаления файла.
        """
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
    """
    Класс для управления файлами данных персонажей в формате XML.
    """

    def __init__(self) -> None:
        """
        Инициализирует менеджер данных с XML-сериализатором.
        """
        super().__init__(XMLSerializer())

    def create(self, character: Character, filename: str) -> bool:
        """
        Создает XML-файл с данными персонажа.

        Args:
            character (Character): Объект персонажа для сохранения.
            filename (str): Имя файла для сохранения.

        Returns:
            bool: True при успешном создании, иначе False.

        Raises:
            DataStorageError: При ошибке создания файла.
        """
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(self.serializer.serialize(character))
            return True
        except Exception as e:
            raise DataStorageError(f"Ошибка при создании файла XML: {e}")

    def read(self, filename: str) -> Character:
        """
        Читает персонажа из XML-файла.

        Args:
            filename (str): Имя файла для чтения.

        Returns:
            Character: Объект персонажа.

        Raises:
            DataStorageError: При ошибке чтения файла.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = f.read()
            return self.serializer.deserialize(data)
        except FileNotFoundError:
            raise DataStorageError(f"Файл {filename} не найден.")
        except Exception as e:
            raise DataStorageError(f"Ошибка при чтении файла XML: {e}")

    def update(self, character: Character, filename: str) -> bool:
        """
        Обновляет данные персонажа в XML-файле.

        Args:
            character (Character): Объект персонажа для обновления.
            filename (str): Имя файла для обновления.

        Returns:
            bool: True при успешном обновлении, иначе False.

        Raises:
            DataStorageError: При ошибке обновления файла.
        """
        return self.create(character, filename)

    def delete(self, filename: str) -> bool:
        """
        Удаляет XML-файл с данными персонажа.

        Args:
            filename (str): Имя файла для удаления.

        Returns:
            bool: True при успешном удалении, иначе False.

        Raises:
            DataStorageError: При ошибке удаления файла.
        """
        try:
            import os
            os.remove(filename)
            return True
        except FileNotFoundError:
            print(f"Файл {filename} не найден для удаления.")
            return False
        except Exception as e:
            raise DataStorageError(f"Ошибка при удалении файла XML: {e}")