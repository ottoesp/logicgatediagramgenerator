from django.http import JsonResponse
MAX_LEN_INPUT = 100

class ValidationResponse:
    def __init__(self, valid: bool, reasons: list[str]) -> None:
        self.valid: bool = valid
        self.reasons: list[str] = reasons

def is_valid_input(sentence: str, max_width: str) -> ValidationResponse:
    valid = True
    reasons: list[str] = []

    if len(sentence) > MAX_LEN_INPUT:
        valid = False
        reasons.append(f'Input size exceeds {MAX_LEN_INPUT}')
    elif len(sentence) == 0:
        valid = False
        reasons.append(f'Input is empty')
    try:
        w = int(max_width)
        if w < 0:
            valid = False
            reasons.append('Max width is negative')
    except:
        valid = False
        reasons.append('Max width is not integer')

    return ValidationResponse(valid, reasons)