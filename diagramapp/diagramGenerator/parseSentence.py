from __future__ import annotations
from .nodeType import STRING_REPRESENTATION, TYPE_FROM_STRING_REPRESENTATION, NodeType, BINDING_STRENGTH, DOUBLE_INPUT_GATES, SINGLE_INPUT_GATES
from .nodeType import NodeType

GATE_STRINGS = STRING_REPRESENTATION.values()


class ParsingError(ValueError):
    pass

def tokenise_sentence(sentence: str) -> list[str]:
    tokens: list[str] = []
    i = 0
    
    while i < len(sentence):
        char = sentence[i]

        # Skip whitespace
        if char.isspace():
            i += 1
        
        elif char in '()':
            tokens.append(char)
            i += 1

        elif char.isalpha():            
            # Find the end of the current word
            word_end = i
            while word_end < len(sentence) and sentence[word_end].isalpha():
                word_end += 1

            word = sentence[i:word_end]
            i = word_end

            # Length one words are variables
            if len(word) == 1:
                tokens.append(word)

            elif word in GATE_STRINGS:
                tokens.append(word)
            
            else:
                raise ParsingError(f'Invalid token {word}')
        
        else:
            raise ParsingError(f'Invalid token {char}')

    return tokens

ParseTree = tuple[NodeType, "ParseTree", "ParseTree"] | tuple[NodeType, "ParseTree"] | tuple[NodeType, str]

def parse_tokens(tokens: list[str]) -> ParseTree:
    bracket_depth = 0
    first_opening_bracket = None
    matching_closing_bracket = None
    
    lowest_binding_token: tuple[NodeType, int] | None = None

    # Do a pass through each token and save the lowest binding
    for i, token in enumerate(tokens):
        if token == '(':
            bracket_depth += 1
            # Record position of first opening bracket
            if first_opening_bracket is None:
                first_opening_bracket = i
        elif token == ')':
            bracket_depth -= 1
            
            if matching_closing_bracket is None and bracket_depth == 0:
                matching_closing_bracket = i
        elif bracket_depth == 0:
            if len(token) == 1:
                token_type = NodeType.VARIABLE
            else:
                token_type = TYPE_FROM_STRING_REPRESENTATION[token]

            if lowest_binding_token is None or BINDING_STRENGTH[lowest_binding_token[0]] > BINDING_STRENGTH[token_type]:
                lowest_binding_token = (token_type, i)
                
    if bracket_depth != 0:
        raise ParsingError("Parenthesises are not closed")
    
    # If no token was found to be the lowest then check parenthesis
    if lowest_binding_token is None:
        if (matching_closing_bracket is None) or (first_opening_bracket is None) or (first_opening_bracket + 1 == matching_closing_bracket):
            raise ParsingError("Parenthesises are empty")
        
        if first_opening_bracket != 0 or matching_closing_bracket != len(tokens) - 1:
            raise ParsingError("Terms grouped by parenthesises are not joined by operator")

        # Strip brackets and do another pass
        return parse_tokens(tokens[first_opening_bracket + 1:matching_closing_bracket])
    
    elif lowest_binding_token[0] in DOUBLE_INPUT_GATES:
        # Check that there are tokens to the left and right
        if lowest_binding_token[1] == 0 or lowest_binding_token[1] == len(tokens) - 1:
            raise ParsingError(f"Invalid {STRING_REPRESENTATION[lowest_binding_token[0]]} gate")
        
        left = parse_tokens(tokens[:lowest_binding_token[1]])
        right = parse_tokens(tokens[lowest_binding_token[1] + 1:])

        return (lowest_binding_token[0], left, right)
    
    elif lowest_binding_token[0] in SINGLE_INPUT_GATES:
        # Must be leftmost token to be valid, and must have tokens after it
        if lowest_binding_token[1] != 0 or lowest_binding_token[1] == len(tokens) - 1:
            raise ParsingError(f'Invalid {STRING_REPRESENTATION[lowest_binding_token[0]]} gate')
        
        right = parse_tokens(tokens[lowest_binding_token[1] + 1:])
        return (lowest_binding_token[0], right)
    
    elif lowest_binding_token[0] == NodeType.VARIABLE:
        if len(tokens) > 1:
            raise ParsingError(f'Variables not joined by gate')
        return (lowest_binding_token[0], tokens[lowest_binding_token[1]])
    else:
        raise ParsingError(f'Bad Parsing')
    
def parse_sentence(sentence: str) -> ParseTree:
    tokens = tokenise_sentence(sentence)
    return parse_tokens(tokens)