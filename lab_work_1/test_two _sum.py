import unittest
from two_sum import two_sum


class TestTwoSum(unittest.TestCase):
    def test_example1(self):
        self.assertEqual(two_sum([2,7,11,15], 9), [0,1])

    def test_example2(self):
        self.assertEqual(two_sum([3,2,4], 6), [1,2])

    def test_example3(self):
        self.assertEqual(two_sum([3,3], 6), [0,1])
    
    def test_no_solution(self):
        self.assertEqual(two_sum([1,2,3], 7), [])
    
    def test_negative_numbers(self):
        self.assertEqual(two_sum([-1,-2,-3,-4,-5], -8), [2,4])
    
    def test_mixed_numbers(self):
        self.assertEqual(two_sum([-3,4,3,90], 0), [0,2])
    
    def test_large_numbers(self):
        self.assertEqual(two_sum([1000000,2000000,3000000], 5000000), [1,2])
    
    def test_duplicate_numbers_different_indices(self):
        self.assertEqual(two_sum([2,5,5,11], 10), [1,2])
    
    def test_single_element(self):
        self.assertEqual(two_sum([5], 10), [])
    
    def test_empty_array(self):
        self.assertEqual(two_sum([], 5), [])


if __name__ == "__main__":
    unittest.main(argv=[''], verbosity=2, exit=False)