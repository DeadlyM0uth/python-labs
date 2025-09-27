import unittest

# Функция, которую будем тестировать
def add(a, b):
    return a + b

class TestMath(unittest.TestCase):
    # Сложение двух положительных чисел
    def test_add_positive(self):
        self.assertEqual(add(2, 3), 5)

    # Сложение двух отрицательных чисел
    def test_add_negative(self):
        self.assertEqual(add(-1, -3), -4)

    # Сложение с нулем
    def test_add_zero(self):
        self.assertEqual(add(0, 5), 5)

    # Сложение двух нулей
    def test_add_two_zeros(self):
        self.assertEqual(add(0, 0), 0)

    # Сложение положительного и отрицательного числа
    def test_add_positive_negative(self):
        self.assertEqual(add(7, -2), 5)

    # Сложение с большим числом
    def test_add_large_numbers(self):
        self.assertEqual(add(10**10, 10**10), 2 * 10**10)

    # Сложение чисел с плавающей точкой
    def test_add_floats(self):
        self.assertAlmostEqual(add(2.5, 3.1), 5.6, places=6)

    # Смешанное сложение int и float
    def test_add_int_and_float(self):
        self.assertEqual(add(2, 3.5), 5.5)

    # Сложение строк
    def test_add_strings(self):
        self.assertEqual(add("Hello, ", "World"), "Hello, World")

    # Ошибка при сложении несовместимых типов
    def test_add_invalid_types(self):
        with self.assertRaises(TypeError):
            add(5, [1, 2, 3])

if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)
