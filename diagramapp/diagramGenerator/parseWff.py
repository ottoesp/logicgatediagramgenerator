from connectives import connectives, Connective, Variable
from typing import Tuple
from logicalElementTree import LogElNode
import copy
import re

def strip_outer_brackets(wff):
    wff = wff.strip()
    while wff[0] == '(':
        if wff[len(wff) - 1] == ')':
            wff = wff[1:len(wff) - 1]
        else:
            break
    return wff

def get_prefix_connective(wff) -> Connective:
    for connective in connectives:
        if wff[0:len(connective.name)] == connective.name:
            return copy.deepcopy(connective)
    return Connective()

def split_at_connective(wff: str) -> Tuple[str, Connective, str]:
    bracket_depth = 0
    n = len(wff)

    lb_idx = -1
    lb_connective = Connective()

    i = 0
    while i < n:
        char = wff[i]
        if char == '(':
            bracket_depth += 1
        elif char == ')':
            bracket_depth -= 1
        elif bracket_depth == 0:
            # Not in brackets
            connective = get_prefix_connective(wff[i:])
            if not connective.is_empty():
                # Save as lowest binding strength
                if (lb_connective.is_empty()) or (lb_connective.binding_strength > connective.binding_strength):
                    lb_connective = connective
                    lb_idx = i
                i += len(connective.name)

        i += 1

    if bracket_depth != 0:
        raise Exception("Incorrect Brackets")

    left_formula = wff[0:lb_idx]
    right_formula = wff[lb_idx + len(lb_connective.name):]

    return left_formula, lb_connective, right_formula

def is_valid_formula(formula):
    """Checks if a string is a valid propositional logic formula."""
    # This pattern is simplified and may not catch all logic rules (e.g., precedence)
    # but works for the structure requested.
    pattern = r"^(?:\s*not\s*)?(?:[A-Z]|\((?:\s*not\s*)?[A-Z]\s+(?:and|or)\s+(?:\s*not\s*)?[A-Z]\s*\))(?:\s+(?:and|or)\s+(?:\s*not\s*)?(?:[A-Z]|\((?:\s*not\s*)?[A-Z]\s+(?:and|or)\s+(?:\s*not\s*)?[A-Z]\s*\)))*$"
    return re.fullmatch(pattern, formula) is not None

def parse_wff(wff, tree):
    wff = strip_outer_brackets(wff)
    if not is_valid_formula(wff):
        raise Exception(f'{wff} is not a wff')

    if len(wff) <= 1:
        tree.set_data(Variable(wff))
        return tree

    left_formula, root_log_el, right_formula = split_at_connective(wff)
    tree.set_data(root_log_el)

    if left_formula:
        tree.left = LogElNode()
        parse_wff(left_formula, tree.left)
    if right_formula:
        tree.right = LogElNode()
        parse_wff(right_formula, tree.right)

    return tree