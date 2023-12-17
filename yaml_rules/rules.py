import logging 
import yaml

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

def load_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            rules_data = yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Could not parse {file_path}: {e.args[0]}", e)
        raise Exception(f"Could not parse {file_path}: {e.args[0]}")

    engine = Engine(name=None)

    for key in rules_data["rule"]:
        if key == "name":
            engine.name = rules_data["rule"]["name"]
        if key == "conditions":
            if not "and" in rules_data["rule"]["conditions"]:
                continue

            and_condition_list = rules_data["rule"]["conditions"]["and"]
            for cvalue in and_condition_list:
                build_rules(engine, cvalue)

        if key == "actions":
            add_actions_list(engine, rules_data["rule"]["actions"])
    
    return engine          

def add_actions_list(engine, action_list):
    for action in action_list:
        for akey, avalue in action.items():
            engine.actions[akey] = create_action_handler(akey, avalue)

def create_action_handler(akey, action_key):
    return Action(name=akey, action_label=action_key)

def build_rules(engine, conditions_dict):
    for key, condition_dict in conditions_dict.items():
        engine.conditions[key] = create_condition_handler(key, condition_dict)
        break

def create_condition_handler(condition_name, condition_dict):
    return Condition(name=condition_name, key=condition_dict["key"], operator=condition_dict["operator"], value=condition_dict["value"])

class Condition:
    def __init__(self, name=None, key=None, operator=None, value=None):
        self.name = name
        self.key = key
        self.operator = operator
        self.value = value

    def evaluate(self, context):
        result = self.execute_condition(context)
        context["condition_log"][self.name] = result
        return result

    def execute_condition(self, context):
        return True
    
class Action:
    def __init__(self, name=None, action_label=None):
        self.name = name
        self.action_label = action_label

    def execute(self, context):
        logging.info(f"Action executing for {self.action_label}")
        # Log it 
        context["action_log"][self.name] = f"Action executing for {self.name} - {self.action_label}"