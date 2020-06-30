import unittest
import indicator_util


class IndicatorUtilTest(unittest.TestCase):
    sma = [22.2247500, 22.2128300, 22.2326900, 22.2623800, 22.3060600, 22.4232400, 22.6149900, 22.7669200, 22.9069300,
           23.0777300, 23.2117800, 23.3786100, 23.5265700, 23.6537800, 23.7113900, 23.6855700, 23.6129800, 23.5057300,
           23.4322500, 23.2773400, 23.1312100]

    sol = [22.503, 22.601554, 22.718133]

    def test_moving_average(self):
        sma_length = len(self.sma)
        period = 10
        i = 0;
        while i < 3:
            self.assertAlmostEqual(self.sol[i], indicator_util.calculate_simple_moving_average(self.sma[i:period + i]),
                                   places=3)
            i += 1

    def test_moving_average_negative_one(self):
        self.assertEqual(-1, indicator_util.calculate_simple_moving_average(-1))
