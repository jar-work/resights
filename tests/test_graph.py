import unittest
from graph import EdgeInformation

class TestGetShareValues(unittest.TestCase):
    def test_get_share_values(self):
        edge_information = EdgeInformation('100%')
        self.assertEqual(edge_information.lower_ownership, 1)
        self.assertEqual(edge_information.middle_ownership, 1)
        self.assertEqual(edge_information.upper_ownership, 1)

        edge_information = EdgeInformation('50%')
        self.assertEqual(edge_information.lower_ownership, 0.5)
        self.assertEqual(edge_information.middle_ownership, 0.5)
        self.assertEqual(edge_information.upper_ownership, 0.5)

        edge_information = EdgeInformation('30-40%')
        self.assertEqual(edge_information.lower_ownership, 0.3)
        self.assertEqual(edge_information.middle_ownership, 0.35)
        self.assertEqual(edge_information.upper_ownership, 0.4)

        edge_information = EdgeInformation('<70%')
        self.assertEqual(edge_information.lower_ownership, 0)
        self.assertEqual(edge_information.middle_ownership, 0.35)
        self.assertEqual(edge_information.upper_ownership, 0.7)

    def test_print_ownership(self):
        edge_information = EdgeInformation('20-60%')
        self.assertEqual(edge_information.get_ownership_value(), '20-60%')

        edge_information = EdgeInformation('20%')
        self.assertEqual(edge_information.get_ownership_value(), '20%')

        edge_information = EdgeInformation('<11%')
        self.assertEqual(edge_information.get_ownership_value(), '<11%')

        # less than 10% we show two decimals
        edge_information = EdgeInformation('<10%')
        self.assertEqual(edge_information.get_ownership_value(), '<10.00%')
