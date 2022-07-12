import tkinter as tk
from tkinter import ttk


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


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
        if value.startswith(leader) and is_float(value[len(leader):]):
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


class UnitFormulaFrame(ttk.Frame):
    """Ttk Frame with a predefined set of widgets

        See class definition for a layout of the widgets
    +-----------------------------+
    |           +----------------+|
    |Unit Price |                ||
    |           +----------------+|
    |           +----------------+|
    |Formula    |                ||
    |           +----------------+|
    |           +----------------+|
    |Basis Value|                ||
    |           +----------------+|
    +-----------------------------+
    """

    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.master = master

        self.unit_price_var = None
        self.calculated_basis_var = None
        self.formula_var = None
        self.unit_price_label = None
        self.formula_label = None
        self.calculated_basis_label = None
        self.unit_price_entry = None
        self.formula_entry = None
        self.calculated_basis_entry = None

        self.nvcmd = None
        self.fvcmd = None
        self.ivcmd = None

        self.create_vars()
        self.create_validation_functions()
        self.create_widgets()
        self.place_widgets()

    def create_vars(self):
        self.formula_var = tk.StringVar()
        self.calculated_basis_var = tk.StringVar()
        self.unit_price_var = tk.StringVar()

    def create_validation_functions(self):
        # validation functions
        self.nvcmd = (self.master.register(is_float), '%P')
        self.fvcmd = (self.master.register(validate_formula), '%P')
        self.ivcmd = (self.master.register(self.on_invalid), '%W')

    def create_widgets(self):
        # create the widgets
        self.unit_price_label = ttk.Label(self, text='Unit Price', font=('TkDefaultFont', 18))
        self.formula_label = ttk.Label(self, text='Formula', font=('TkDefaultFont', 18))
        self.calculated_basis_label = ttk.Label(self, text='Basis Value', font=('TkDefaultFont', 18))

        self.unit_price_entry = ttk.Entry(
            self, font=('TkDefaultFont', 18),
            textvariable=self.unit_price_var,
            validate='key',
            validatecommand=self.nvcmd,
            invalidcommand=self.ivcmd,
        )
        self.unit_price_entry.bind('<KeyRelease>', self.update_display)
        self.formula_entry = ttk.Entry(
            self, font=('TkDefaultFont', 18),
            textvariable=self.formula_var,
            validate='key',
            validatecommand=self.fvcmd,
            invalidcommand=self.ivcmd,
        )
        self.formula_entry.bind('<KeyRelease>', self.update_display)
        self.calculated_basis_entry = ttk.Entry(
            self, font=('TkDefaultFont', 18),
            textvariable=self.calculated_basis_var,
            state='readonly',
        )

    def place_widgets(self):

        self.unit_price_label.grid(row=0, column=0, sticky='w', pady=10, padx=10)
        self.unit_price_entry.grid(row=0, column=1, sticky='we', pady=10, padx=10)

        self.formula_label.grid(row=1, column=0, sticky='w', pady=10, padx=10)
        self.formula_entry.grid(row=1, column=1, sticky='we', pady=10, padx=10)

        self.calculated_basis_label.grid(row=2, column=0, sticky='w', pady=10, padx=10)
        self.calculated_basis_entry.grid(row=2, column=1, sticky='we', pady=10, padx=10)

    def update_display(self, _):
        unit_price = self.unit_price_var.get()
        formula = self.formula_var.get()
        if valid_formula(formula):
            multiplier = find_multiplier(formula)
            if multiplier != 0:
                if is_float(unit_price):
                    self.calculated_basis_var.set(round(float(self.unit_price_var.get()) / multiplier, 3))
                else:
                    self.calculated_basis_var.set('')
            else:
                pass
        else:
            self.calculated_basis_var.set('')

    def on_invalid(self, _):
        self.bell()
