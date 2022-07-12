import tkinter as tk
from view import View


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def valid_formula(formula: str) -> bool:
    # if formula is falsey
    formula = formula.upper()
    if not formula:
        return False
    leaders = ['*', 'X', 'D', '-', '+', 'GP']
    for leader in leaders:
        if len(formula) <= len(leader):
            return False
    if not contains_digit(formula):
        return False
    return True


def validate_formula(value: str) -> bool:
    """Returns a boolean indicating if value is in one of the forms case insensitive

        [G]

        [''|None]

        [*||X||D|-|+]{0..9}[.]{0..9}

        GP[-|+]{0..9}[.]{0..9}

        """
    leaders = ['*', 'X', '-', '+', 'G', 'GP']
    if value == '':
        return True
    if value in leaders:
        return True
    for leader in leaders[:len(leaders)-1]:  # don't look at the GP on the end
        value = value.replace(leader, '', 1)  # remove the leaders from value
    if value.startswith('G'):
        value = value[1:]
    if value.upper().startswith('GP') and is_float(value=value[2:]):
        return True
    if is_float(value):
        return True
    return False


def contains_digit(value: str) -> bool:
    return any(x in '0123456789' for x in value)


def find_multiplier(formula: str) -> float:
    """Converts a string formula to a float multiplier

        A return value of -1 indicates error
    """
    try:
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


if __name__ == "__main__":
    app = tk.Tk()
    app.title('Special Calculator')
    app.resizable(False, False)
    view = View(master=app)

    app.mainloop()
