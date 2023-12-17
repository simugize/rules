import unittest
from yaml_rules import rules

class TestRules(unittest.TestCase):

    def test_my_rule_function(self):
        # Call the function you want to test
        result = rules.my_rule_function()

        # Assert expected results
        self.assertEqual(result, "Expected Result")

if __name__ == '__main__':
    unittest.main()