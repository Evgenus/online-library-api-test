from unittest import TestCase

from .subset import find_subset


class SubSetTestCase(TestCase):
    def test_found_1(self):
        subset = find_subset([1, 2, 3, 4, -11, 5, 6, 7, 8])
        self.assertEqual(subset, (-11, 3, 8))

    def test_found_2(self):
        subset = find_subset([1, 2, 3, 4, -10, -11, -12, -13, -3])
        self.assertEqual(subset, (-3, 1, 2))

    def test_not_found(self):
        subset = find_subset([1, 2, 3, 4, -10, -11, -12, -13, -33])
        self.assertEqual(subset, None)
