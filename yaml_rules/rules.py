import logging 
import yaml

class Engine:
    def __init__(self, name):
        self.name = name
        self.conditions = {}    # Definition
        self.actions = {}       # Action definitions
    
    def execute(self, context):
        eval_result = False
        # Run the 'AND' rules
        if not "and" in self.conditions:
            logging.info(f"No and conditions in {self.name}") 


def load_from_file(file_path):
    with open(file_path, 'r') as file:
        rules_data = yaml.safe_load(file)
    
    engine = Engine(name=None)

    for key in rules_data['rule']:
        if key == "name":
            engine.name = rules_data['rule']['name']
    
    return engine          
