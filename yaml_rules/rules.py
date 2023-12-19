import logging 
import yaml
import re
import string
import random

class Engine:
    def __init__(self, name):
        self.name = name
        self.conditions = {}    # Definition
        self.actions = {}       # Action definitions
    
    def execute(self, context):
        context["condition_log"] = {}
        context["action_log"] = {}

        # Run 'and' conditions
        and_result = True
        for condition_name in self.conditions:
            
            # Bail if the result is ever false
            if not and_result: 
                break

            and_result = self.conditions[condition_name].evaluate(context)

        # Don't run anything
        if not and_result:
            return

        # Execute actions if true
        for akey, avalue in self.actions.items():
            avalue.execute(context)

    def add_action_handler(self, action_func):
        action_key = random_string(10)
        self.actions[action_key] = create_action_handler(action_key, action_key, action_func)

# End Engine class

def random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

    
def add_actions_list(engine, action_list):
    for action in action_list:
        for akey, avalue in action.items():
            engine.actions[akey] = create_action_handler(akey, avalue)

def create_action_handler(akey, action_key=None, action_func=None):
    return Action(name=akey, action_label=action_key, action_func=action_func)

def build_rules(engine, conditions_dict):
    for key, condition_dict in conditions_dict.items():
        engine.conditions[key] = create_condition_handler(key, condition_dict)
        break

def create_condition_handler(condition_name, condition_dict):
    operator = "="
    if "operator" in condition_dict:
        operator = condition_dict["operator"]

    value_transform = None
    if "value_transform" in condition_dict:
        value_transform = condition_dict["value_transform"]

    return Condition(name=condition_name, key=condition_dict["key"], operator=operator, value=condition_dict["value"], value_transform=value_transform)

def replace_variable(match, context):
    variable_name = match.group(1)
    return str(context.get(variable_name, match.group(0)))

class Condition:
    def __init__(self, name=None, key=None, operator=None, value=None,value_transform=None):
        self.name = name
        self.key = key
        self.operator = operator
        self.value = value
        self.value_transform = value_transform

    def evaluate(self, context):
        result = self.execute_condition(context)
        context["condition_log"][self.name] = result
        return result

    def execute_condition(self, context):
        key_value = context[self.key]
        target_value = self.value

        # If target is a reference field, grab the value
        if isinstance(target_value, str) and target_value.startswith("$"):
            target_value = context[target_value[1:]]

        # Do I need to transform the value?
        if isinstance(self.value_transform, str):
            pattern = r'\$(\w+)'
            value_transform = re.sub(pattern, lambda match: replace_variable(match, context), self.value_transform)            
            target_value = eval(value_transform)


        if self.operator == "=":
            return key_value == target_value 
    
        if self.operator == "<":
            return key_value < target_value
        
        if self.operator == ">":
            return key_value > target_value   

        if self.operator == ">=":
            return key_value >= target_value   
        
        if self.operator == "<=":
            return key_value <= target_value   

        if self.operator == "between":
            values = target_value.split(",")
            return float(key_value) > float(values[0]) and float(key_value) < float(values[1])   
               

class Action:
    def __init__(self, name=None, action_label=None, action_func=None):
        self.name = name
        self.action_label = action_label
        self.action_func = action_func

    def execute(self, context):
        # If you have a custom handler, execute it
        if self.action_func:
            self.action_func(context)
        else: 
            logging.info(f"Action executing for {self.action_label}")
            # Log it 
            context["action_log"][self.name] = f"Action executing for {self.name} - {self.action_label}"