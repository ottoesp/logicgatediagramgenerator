from inputParser.connectives import connectives, Connective
from typing import Tuple
from dag import DiagramNode, DiagramDag, VariableNode
import copy
import re

def strip_outer_brackets(wff):
    wff = wff.strip()
    if len(wff) >= 2 and wff[0] == '(' and wff[-1] == ')':
        bracket_depth = 0
        for i, char in enumerate(wff):
            if char == '(':
                bracket_depth += 1
            elif char == ')':
                bracket_depth -= 1
                if (bracket_depth == 0) and i != len(wff) - 1:
                    # The bracket in the first position is closing before the end
                    return wff
        # Strip brackets and go again in case they are double layered
        return strip_outer_brackets(wff[1:-1])
    # No bracket in first position so leave unchanged
    return wff

def get_prefix_connective(wff) -> Connective:
    for connective in connectives:
        if wff[0:len(connective.name)] == connective.name:
            return copy.deepcopy(connective) # Try remove this
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

    return left_formula, lb_connective.name, right_formula

def is_valid_formula(formula): # Broken
    """Checks if a string is a valid propositional logic formula."""
    # This pattern is simplified and may not catch all logic rules (e.g., precedence)
    # but works for the structure requested.
    pattern = r"^(?:\s*not\s*)?(?:[A-Z]|\((?:\s*not\s*)?[A-Z]\s+(?:and|or)\s+(?:\s*not\s*)?[A-Z]\s*\))(?:\s+(?:and|or)\s+(?:\s*not\s*)?(?:[A-Z]|\((?:\s*not\s*)?[A-Z]\s+(?:and|or)\s+(?:\s*not\s*)?[A-Z]\s*\)))*$"
    return re.fullmatch(pattern, formula) is not None

def parse_wff(wff, dag: DiagramDag, parent_node):
    wff = strip_outer_brackets(wff)
    # if not is_valid_formula(wff):
    #     raise Exception(f'{wff} is not a wff')

    if len(wff) <= 1:
        # Only a single variable left
        dag.insert_node(VariableNode(wff), parent_node)
        return dag

    left_formula, root_log_el, right_formula = split_at_connective(wff)
    new_node = DiagramNode(root_log_el)
    dag.insert_node(new_node, parent_node)

    if left_formula:
        parse_wff(left_formula, dag, new_node)
    if right_formula:
        parse_wff(right_formula, dag, new_node)

    return dag