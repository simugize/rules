import unittest
from yaml_rules import rules
import logging

class TestRules(unittest.TestCase):

    def test_simple_rule(self):
        context = {
            "price":3
        }
        engine = rules.load_from_file("./samples/simple-rule.yaml")
        engine.execute(context)
        
        # Assert name is set
        self.assertEqual("Simple Rule", engine.name)

        # Assert condition has been set
        self.assertIsNotNone(engine.conditions["condition1"])
                
        # Assert result of condition1
        self.assertTrue(context["condition_log"]["condition1"])

        # Assert action is called 
        self.assertTrue("action1" in context["action_log"])

if __name__ == '__main__':
    unittest.main()