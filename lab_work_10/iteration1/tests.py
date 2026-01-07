import unittest
import math
from iteration1 import integrate

# Юнит-тесты
class TestIntegrate(unittest.TestCase):
    def test_sin_integral(self):
        """Проверка интеграла sin(x) от 0 до π (должно быть 2)"""
        result = integrate(math.sin, 0, math.pi, n_iter=10000)
        self.assertAlmostEqual(result, 2.0, places=2)
    
    def test_polynomial(self):
        """Проверка интеграла x² от 0 до 1 (должно быть 1/3)"""
        result = integrate(lambda x: x**2, 0, 1, n_iter=10000)
        self.assertAlmostEqual(result, 1/3, places=3)
    
    def test_iterations_stability(self):
        """Проверка устойчивости к изменению числа итераций"""
        result1 = integrate(math.sin, 0, math.pi, n_iter=1000)
        result2 = integrate(math.sin, 0, math.pi, n_iter=10000)
        self.assertAlmostEqual(result1, result2, places=2)
    
    def test_reverse_bounds(self):
        """Проверка с обратными пределами интегрирования"""
        result = integrate(math.sin, math.pi, 0, n_iter=1000)
        self.assertAlmostEqual(result, -2.0, places=2)
        
        
if __name__ == "__main__":
    unittest.main()