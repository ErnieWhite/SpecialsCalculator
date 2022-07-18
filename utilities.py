def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def is_float_or_empty(value):
    return is_float(value) or value == ''


def find_multiplier(formula: str) -> float:
    """Converts a string formula to a float multiplier

        A return value of -1 indicates error
    """
    try:
        print(formula)
        if formula[0] in '+-':
            return 1 + float(formula) / 100
        if formula[0].upper() == 'D':
            return 1 / float(formula[1:])
        if formula.upper().startswith('GP'):
            return 1 / (1 - float(formula[2:]) / 100)
        if formula[0].upper() in '*X':
            return float(formula[1:])
    except ZeroDivisionError:
        return -1


def validate_formula(value: str) -> bool:
    """Returns a boolean indicating if value is in one of the forms case insensitive

        [G]

        [''|None]

        [*||X||D|-|+]{0..9}[.]{0..9}

        GP[-|+]{0..9}[.]{0..9}

        """
    leaders = ['*', 'X', '-', '+', 'D', 'G', 'GP']
    value = value.upper()
    if value in leaders:
        return True
    leaders.remove('G')
    for leader in leaders:
        if value.startswith(leader) and (is_float(value[len(leader):]) or value[len(leader):] == '.'):
            return True
    if value == '':
        return True
    return False


def valid_formula(value: str) -> bool:
    """Returns a boolean indicating if value is in one of the forms case insensitive

        [G]

        [''|None]

        [*||X||D|-|+]{0..9}[.]{0..9}

        GP[-|+]{0..9}[.]{0..9}

        """
    leaders = ['*', 'X', '-', '+', 'D', 'GP']
    value = value.upper()
    for leader in leaders:
        if value.startswith(leader) and is_float(value[len(leader):]):
            return True
    return False
