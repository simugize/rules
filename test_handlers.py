import unittest
from yaml_rules import rules
import logging

class TestHandlers(unittest.TestCase):

    action_fired = False

    def toggle_status(self, context):
        self.action_fired = True

    def test_simple_rule(self):
        context = {
            "price":2
        }
        engine = rules.load_from_file("./samples/simple-handler.yaml")
        engine.add_action_handler(lambda c2: self.toggle_status(context))
        engine.execute(context)
        
        # Assert name is set
        self.assertEqual("Simple Handler", engine.name)

        # Assert action callback was called
        self.assertTrue(self.action_fired, "Action callback was not called.")


if __name__ == '__main__':
    unittest.main()