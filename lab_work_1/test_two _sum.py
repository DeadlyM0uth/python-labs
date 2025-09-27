import unittest
from two_sum import two_sum


class TestTwoSum(unittest.TestCase):
    def test_example1(self):
        self.assertEqual(two_sum([2,7,11,15], 9), [0,1])

    def test_example2(self):
        self.assertEqual(two_sum([3,2,4], 6), [1,2])

    def test_example3(self):
        self.assertEqual(two_sum([3,3], 6), [0,1])

    
if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)