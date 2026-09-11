import re
from typing import Any, Callable

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def compose_validators(*funcs: Callable[[Any], bool]) -> Callable[[Any], bool]:
    return lambda x: all(f(x) for f in funcs)

def range_validator(min_val: int, max_val: int) -> Callable[[int], bool]:
    return lambda x: min_val <= x <= max_val

def type_validator(expected_type: type) -> Callable[[Any], bool]:
    return lambda x: isinstance(x, expected_type)

def sanitize_string(input_str: str) -> str:
    return ''.join(char for char in input_str if char.isalnum() or char.isspace()).strip()

def chain_validation(value: Any, validators: list[Callable[[Any], bool]]) -> bool:
    for validator in validators:
        if not validator(value):
            return False
    return True

if __name__ == '__main__':
    age_check = compose_validators(type_validator(int), range_validator(18, 99))
    print(f'Validation success: {age_check(25)}')