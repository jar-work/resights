import unittest
from graph import get_share_values

class TestGetShareValues(unittest.TestCase):
    def test_get_share_values(self):
        self.assertEqual(get_share_values('100%'), [100])
        self.assertEqual(get_share_values('50%'), [50])
        self.assertEqual(get_share_values('33%'), [33])
        self.assertEqual(get_share_values('<5%'), [0, 2.5, 5])
