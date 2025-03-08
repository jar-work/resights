import sys
import unittest
from graph import get_share_values, get_ownership_description

class TestGetShareValues(unittest.TestCase):
    def test_get_share_values(self):
        self.assertEqual(get_share_values('100%'), [1, 1, 1])
        self.assertEqual(get_share_values('50%'), [0.5, 0.5, 0.5])
        self.assertEqual(get_share_values('33%'), [0.33, 0.33, 0.33])
        self.assertEqual(get_share_values('<5%'), [0, 0.025, 0.05])

    def test_print_ownership(self):
        self.assertEqual(get_ownership_description('Alice', 0.2, 0.4, 0.6, 'Bob'), 'Alice owns 20.00-60.00% of Bob')
        self.assertEqual(get_ownership_description('Alice', 0.2, 0.2, 0.2, 'Bob'), 'Alice owns 20.00% of Bob')
        self.assertEqual(get_ownership_description('Alice', 0, 0.025, 0.05, 'Bob'), 'Alice owns <5.00% of Bob')


