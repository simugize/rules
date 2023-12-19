import logging
from rules import Engine, build_rules, add_actions_list
import yaml

def load_from_file(file_path):
    try:
        with open(file_path, 'r') as file_contents:
            return load_from_string(file_contents)
    except Exception as e:
        logging.error(f"Could not parse {file_path}: {e.args[0]}", e)
        raise Exception(f"Could not parse {file_path}: {e.args[0]}")


def load_from_string(yaml_string):
    rules_data = yaml.safe_load(yaml_string)

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