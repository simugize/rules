import unittest
from yaml_rules import rules
import logging

class TestWatchlist(unittest.TestCase):

    action_fired = False

    def toggle_status(self, context):
        self.action_fired = True

    def test_simple_rule(self):
        context = {
            "price":2,
            "recentPositiveNews": True,
            "outstandingShares": 10000000,
            "dailyVolume": 100,
            "30DayAverageVolume": 10
        }
        engine = rules.load_from_file("./samples/watchlist-rule.yaml")
        engine.add_action_handler(lambda c2: self.toggle_status(context))
        engine.execute(context)
        
        self.assertTrue(self.action_fired, "Watchlist rule was not executed.")

if __name__ == '__main__':
    unittest.main()