import unittest
from CalculateDays.dayCalculator import get_days

class TestGetDays(unittest.TestCase):
    def test_get_days(self):
        days1, fees1 = get_days('2024-01-02','2023-06-02')
        self.assertEqual(days1, 214)
        self.assertEqual(fees1, 1070)
        days2, fees2 = get_days('2025-12-22','2010-01-31')
        self.assertEqual(days2, 5804)
        self.assertEqual(fees2, 29020)
        days3, fees3 = get_days('2023-12-31','2023-12-31')
        self.assertEqual(days3, 0)
        self.assertEqual(fees3, 0)
        days4, fees4 = get_days('2023-12-31','2024-01-01')
        self.assertEqual(days4, -1)
        self.assertEqual(fees4, -5)

unittest.main()