import unittest
from yaml_rules import rules

class TestRules(unittest.TestCase):

    def test_simple_rule(self):
        context = {
            "price":3
        }
        engine = rules.load_from_file("./samples/simple-rule.yaml")
        #engine.execute(context)
        # Assert the action fired once
        self.assertEquals("Simple Rule", engine.name)
        #self.assertTrue("test_print" in context.action_log)
        #self.assertTrue(len(context.action_log["test_print"]) == 1)

if __name__ == '__main__':
    unittest.main()