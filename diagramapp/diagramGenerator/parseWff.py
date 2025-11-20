from typing import Tuple
from dag import DiagramNode, DiagramDag, VariableNode
from nodeType import NodeType

INF_BINDING_STRENGTH = 100

binding_strength = {
    NodeType.AND : 0,
    NodeType.OR : 0,
    NodeType.NOT : 1
}

string_to_nodeType = {
    "and" : NodeType.AND,
    "or" : NodeType.OR,
    "not" : NodeType.NOT
}

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

def get_prefix_node(wff) -> tuple[NodeType | None, int]:
    for node_string in string_to_nodeType.keys():
        if wff[0:len(node_string)] == node_string:
            return string_to_nodeType[node_string], len(node_string)
    return None, -1

def split_at_lowest_binding_node(wff: str) -> Tuple[str, NodeType, str]:
    bracket_depth = 0
    n = len(wff)

    lb_idx = -1
    lb_len = -1
    lb_node_type = None
    lowest_binding_strength = INF_BINDING_STRENGTH

    i = 0
    while i < n:
        char = wff[i]
        if char == '(':
            bracket_depth += 1
        elif char == ')':
            bracket_depth -= 1
        elif bracket_depth == 0:
            # Not in brackets
            nodeType, node_string_len = get_prefix_node(wff[i:])

            if nodeType is not None:
                # Save as lowest binding strength
                if lowest_binding_strength > binding_strength[nodeType]:
                    lowest_binding_strength = binding_strength[nodeType]
                    # set the index it was found at, the number of characters it took up and the type of node
                    lb_idx = i
                    lb_len = node_string_len
                    lb_node_type = nodeType
                i += node_string_len

        i += 1

    if bracket_depth != 0:
        raise Exception("Incorrect Brackets")
    if lb_node_type is None:
        raise Exception("")
    
    left_formula = wff[0:lb_idx]
    right_formula = wff[lb_idx + lb_len:]

    return left_formula, lb_node_type, right_formula


def parse_wff(wff, dag: DiagramDag, parent_node):
    wff = strip_outer_brackets(wff)

    if len(wff) <= 1:
        # Only a single variable left
        dag.insert_node(VariableNode(wff), parent_node)
        return dag

    left_formula, node_type, right_formula = split_at_lowest_binding_node(wff)
    new_node = DiagramNode(node_type)
    dag.insert_node(new_node, parent_node)

    if left_formula:
        parse_wff(left_formula, dag, new_node)
    if right_formula:
        parse_wff(right_formula, dag, new_node)

    return dag