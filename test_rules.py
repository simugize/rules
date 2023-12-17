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

    def test_simple_rule_no_action(self):
        context = {
            "price":1 # Too low to trigger action
        }
        engine = rules.load_from_file("./samples/simple-rule.yaml")
        engine.execute(context)
        
        # Assert name is set
        self.assertEqual("Simple Rule", engine.name)

        # Assert condition has been set
        self.assertIsNotNone(engine.conditions["condition1"])
                
        # Assert result of condition1
        self.assertFalse(context["condition_log"]["condition1"])

        # Assert no action was called 
        self.assertFalse("action1" in context["action_log"])        

    def test_simple_rule_with_between(self):
        context = {
            "price":9
        }
        engine = rules.load_from_file("./samples/simple-rule2.yaml")
        engine.execute(context)
        
        # Assert name is set
        self.assertEqual("Simple Rule2", engine.name)

        # Assert condition has been set
        self.assertIsNotNone(engine.conditions["condition1"])
                
        # Assert result of condition1
        self.assertTrue(context["condition_log"]["condition1"])

        # Assert action is called 
        self.assertTrue("action1" in context["action_log"])

    def test_simple_rule_with_reference_value(self):
        context = {
            "high_price":100,
            "low_price":100
        }
        engine = rules.load_from_file("./samples/simple-rule3.yaml")
        engine.execute(context)
        
        # Assert name is set
        self.assertEqual("Simple Rule3", engine.name)

        # Assert condition has been set
        self.assertIsNotNone(engine.conditions["condition1"])
                
        # Assert result of condition1
        self.assertTrue(context["condition_log"]["condition1"])

        # Assert action is called 
        self.assertTrue("action1" in context["action_log"])        

if __name__ == '__main__':
    unittest.main()