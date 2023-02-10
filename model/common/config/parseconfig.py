"""
Parses the config.yaml file and checks for consistency with the default config template.
"""

import os
import yaml

if __name__ == "__main__":
    import sys

    sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
    from utils import GeneralParser, PARSER_FACTORY, set_nested, get_nested, flatten
else:
    from .utils import GeneralParser, PARSER_FACTORY, set_nested, get_nested, flatten

from model.common.units import Quantity


def load_yaml(filename):
    full_filename = os.path.join(
        os.path.dirname(__file__), "../../../inputdata/config/", filename
    )
    with open(full_filename, "r", encoding="utf8") as configfile:
        output = yaml.safe_load(configfile)
    return output


def parse_params(default_yaml, user_yaml, quant=None, return_parser_tree=False):

    parsed_dict = {}
    parser_tree = {}

    def _recursive_traverse(curr_keys, subset):
        for key, node in subset.items():
            keys = list(curr_keys) + [key]
            if isinstance(node, dict) and "type" not in node:
                _recursive_traverse(keys, node)
            else:
                parser = PARSER_FACTORY.create_parser(node, quant)

                # Save the parser instance for possible later use
                set_nested(parser_tree, keys, parser)

                # Save the parsed value
                set_nested(parsed_dict, keys, parser.get(user_yaml, keys))

    _recursive_traverse([], default_yaml)

    if return_parser_tree:
        return parsed_dict, parser_tree

    return parsed_dict


def check_obsolete_params(user_yaml, parsed_params, parser_tree):
    def leaf_criterium(keys, node):
        try:
            parser_type = get_nested(parser_tree, keys).type
        except (AttributeError, KeyError):
            parser_type = None
        if isinstance(node, dict) and parser_type != "dict":
            return False
        return True

    keys_user = set(flatten(user_yaml, leaf_criterium=leaf_criterium))
    keys_parsed = set(flatten(parsed_params, leaf_criterium=leaf_criterium))

    # Check keys which are in user config, but not in parsed file
    # These are obsolete/unused/misspelled parameters
    num_obsolete = 0
    for key in set(keys_user) - set(keys_parsed):
        num_obsolete += 1
        print(f"Obsolete key: {key}")
    if num_obsolete > 0:
        raise RuntimeWarning("Some config parameters are obsolete.")


def load_params(user_yaml_filename="config.yaml"):

    default_units = load_yaml("default_units.yaml")
    default_yaml = load_yaml("config_default.yaml")
    user_yaml = load_yaml(user_yaml_filename) # config yaml params loader

    units = parse_params(default_units, user_yaml)
    quant = Quantity(units)

    params, params_parser_tree = parse_params(
        default_yaml, user_yaml, quant, return_parser_tree=True
    )

    params["default units"] = units["default units"]
    check_obsolete_params(user_yaml, params, params_parser_tree)

    return params


params = load_params()

