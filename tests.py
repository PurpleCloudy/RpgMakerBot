import unittest
import re
from datetime import datetime, timedelta
from rpgmaker import is_valid_time_format, can_enter_special_dungeon, TIME_PATTERN


class TestDungeonTimeValidation(unittest.TestCase):
    """
    Класс для тестирования валидации времени и логики доступа к подземелью.
    """

    def setUp(self):
        """
        Метод, вызываемый перед каждым тестом.
        Инициализирует тестовые данные.
        """
        self.valid_times = ["00:00:00", "12:30:45", "23:59:59", "08:15:30", "00:00:00"]
        self.invalid_times = ["24:00:00", "12:60:00", "12:30:60", "25:30:45", "12:5:30", "8:5:3", "12:30",
                              "abc:def:ghi", ""]

    def tearDown(self):
        """
        Метод, вызываемый после каждого теста.
        Очищает тестовые данные (если нужно).
        """
        pass

    def test_time_pattern_compiles_correctly(self):
        """
        Тест: регулярное выражение компилируется без ошибок.
        """
        try:
            re.compile(TIME_PATTERN)
            self.assertTrue(True)
        except re.error:
            self.fail("TIME_PATTERN is not a valid regex")

    def test_valid_time_formats(self):
        """
        Тест: корректные форматы времени проходят валидацию.
        """
        for time_str in self.valid_times:
            with self.subTest(time_str=time_str):
                self.assertTrue(is_valid_time_format(time_str), f"Время {time_str} должно быть корректным")

    def test_invalid_time_formats(self):
        """
        Тест: некорректные форматы времени не проходят валидацию.
        """
        for time_str in self.invalid_times:
            with self.subTest(time_str=time_str):
                self.assertFalse(is_valid_time_format(time_str), f"Время {time_str} не должно быть корректным")

    def test_time_format_edge_cases(self):
        """
        Тест: граничные случаи формата времени.
        """
        self.assertTrue(is_valid_time_format("00:00:00"))
        self.assertTrue(is_valid_time_format("23:59:59"))
        self.assertFalse(is_valid_time_format("24:00:00"))
        self.assertFalse(is_valid_time_format("12:60:00"))
        self.assertFalse(is_valid_time_format("12:30:60"))

    def test_can_enter_dungeon_first_time(self):
        """
        Тест: первый вход в подземелье разрешен.
        """
        user_id = 12345
        import rpgmaker
        rpgmaker.dungeon_cooldowns.clear()

        can_enter, message = can_enter_special_dungeon(user_id)
        self.assertTrue(can_enter)
        self.assertIn("Ты вошел в особое подземелье!", message)

    def test_can_enter_dungeon_after_4_hours(self):
        """
        Тест: повторный вход разрешен, если прошло 4+ часа.
        """
        user_id = 12346
        import rpgmaker
        rpgmaker.dungeon_cooldowns.clear()

        rpgmaker.dungeon_cooldowns[user_id] = datetime.now() - timedelta(hours=5)

        can_enter, message = can_enter_special_dungeon(user_id)
        self.assertTrue(can_enter)
        self.assertIn("Ты вошел в особое подземелье!", message)

    def test_cannot_enter_dungeon_before_4_hours(self):
        """
        Тест: вход запрещен, если прошло менее 4 часов.
        """
        user_id = 12347
        import rpgmaker
        rpgmaker.dungeon_cooldowns.clear()

        rpgmaker.dungeon_cooldowns[user_id] = datetime.now() - timedelta(hours=2)

        can_enter, message = can_enter_special_dungeon(user_id)
        self.assertFalse(can_enter)
        self.assertIn("Подземелье недоступно", message)
        self.assertIn("через", message)

    def test_time_validation_with_regex_directly(self):
        """
        Тест: прямая проверка регулярного выражения на валидных и невалидных строках.
        """
        for time_str in self.valid_times:
            with self.subTest(time_str=time_str):
                match = re.fullmatch(TIME_PATTERN, time_str)
                self.assertIsNotNone(match, f"Регулярное выражение не совпадает с {time_str}")

        for time_str in self.invalid_times:
            with self.subTest(time_str=time_str):
                match = re.fullmatch(TIME_PATTERN, time_str)
                self.assertIsNone(match, f"Регулярное выражение неожиданно совпадает с {time_str}")


if __name__ == '__rpgmaker__':
    unittest.rpgmaker()
