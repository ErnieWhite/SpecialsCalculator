import re
import tkinter as tk
from tkinter import ttk


def validate_number(value: str) -> bool:
    """Returns a boolean indicating if value is in the form [-|+]{0..9}[.]{0..9}"""
    if re.fullmatch(r"^[-,+]?\d*\.?\d*$", value) is None:
        return False
    else:
        return True


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


def validate_unsigned_number(value: str) -> bool:
    """Returns a boolean indicating if value is in the form {0..9}[.]{0..9}"""
    if re.fullmatch(r"^\d*\.?\d*$", value) is None:
        return False
    else:
        return True


def validate_formula(value: str) -> bool:
    """Returns a boolean indicating if value is in one of the forms case insensitive

        [G]

        [''|None]

        [*||X||D|-|+]{0..9}[.]{0..9}

        GP[-|+]{0..9}[.]{0..9}

        """
    if not value:
        return True
    if value[0].upper() in "*XD-+" and validate_unsigned_number(value=value[1:]):
        return True
    if value.upper() == 'G':
        return True
    if value.upper().startswith('GP') and validate_number(value=value[2:]):
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


class UnitBasisFrame(ttk.Frame):
    """Ttk Frame with a predefined set of widgets

    See class definition for a layout of the widgets
    """

    def __init__(self, master, **kwargs):
        """Construct a Ttk Frame with parent master and predefined widgets.

        STANDARD OPTIONS
            class, cursor, style, takefocus

        WIDGET-SPECIFIC OPTIONS

            borderwidth, relief, padding, width, height
        """
        """
        +-----------------------------------------------+
        |           +----------------++----------------+|
        |Unit Price |                ||                ||
        |           +----------------++----------------+|
        |           +----------------++----------------+|
        |Basis Value|                ||                ||
        |           +----------------++----------------+|
        |           +----------------++----------------+|
        |Decimals   |Auto           v||                ||
        |           +----------------++----------------+|
        |                             +----------------+|
        |                             |                ||
        |                             +----------------+|
        +-----------------------------------------------+
        """
        super().__init__(master, **kwargs)

        # validation functions
        vcmd = (self.master.register(validate_number), '%P')
        ivcmd = (self.master.register(self.on_invalid), '%W')

        # text variables
        self.unit_price_var = tk.StringVar()
        self.basis_value_var = tk.StringVar()
        self.multiplier_var = tk.StringVar()
        self.discount_var = tk.StringVar()
        self.markup_var = tk.StringVar()
        self.gross_profit_var = tk.StringVar()
        self.decimals_var = tk.StringVar()

        # create the widgets
        self.unit_price_label = ttk.Label(self, text='Unit Price', font=('TkDefaultFont', 18))
        self.basis_value_label = ttk.Label(self, text='Basis Value', font=('TkDefaultFont', 18))
        self.decimals_label = ttk.Label(self, text='Decimals', font=('TkDefaultFont', 18))

        self.unit_price_entry = ttk.Entry(
            self,
            textvariable=self.unit_price_var,
            validate='key',
            font=('TkDefaultFont', 18),
            validatecommand=vcmd,
            invalidcommand=ivcmd,
        )
        self.unit_price_entry.bind('<KeyRelease>', self.update_display)
        self.basis_value_entry = ttk.Entry(
            self,
            font=('TkDefaultFont', 18),
            textvariable=self.basis_value_var,
            validate='key',
            validatecommand=vcmd,
            invalidcommand=ivcmd,
        )
        self.basis_value_entry.bind('<KeyRelease>', self.update_display)
        self.decimals_combo = ttk.Combobox(
            self,
            font=('TkDefaultFont', 18),
            values=('Auto', '0', '1', '2', '3', '4', '5', '6'),
            state='readonly',
            textvariable=self.decimals_var,
        )
        self.decimals_combo.bind('<<ComboboxSelected>>', self.update_display)
        self.decimals_combo.set('Auto')

        self.multiplier_formula_entry = ttk.Entry(
            self,
            font=('TkDefaultFont', 18),
            textvariable=self.multiplier_var,
            state='readonly',
        )
        self.discount_formula_entry = ttk.Entry(
            self,
            font=('TkDefaultFont', 18),
            textvariable=self.discount_var,
            state='readonly',
        )
        self.markup_formula_entry = ttk.Entry(
            self,
            font=('TkDefaultFont', 18),
            textvariable=self.markup_var,
            state='readonly',
        )
        self.gross_profit_formula_entry = ttk.Entry(
            self,
            font=('TkDefaultFont', 18),
            textvariable=self.gross_profit_var,
            state='readonly',
        )

        self.unit_price_label.grid(row=0, column=0, sticky='w', pady=10, padx=10)
        self.unit_price_entry.grid(row=0, column=1, sticky='ew', pady=10, padx=10)
        self.multiplier_formula_entry.grid(row=0, column=2, sticky='ew', pady=10, padx=10)

        self.basis_value_label.grid(row=1, column=0, sticky='w', pady=10, padx=10)
        self.basis_value_entry.grid(row=1, column=1, sticky='ew', pady=10, padx=10)
        self.discount_formula_entry.grid(row=1, column=2, sticky='ew', pady=10, padx=10)

        self.decimals_label.grid(row=2, column=0, sticky='w', pady=10, padx=10)
        self.decimals_combo.grid(row=2, column=1, sticky='ew', pady=10, padx=10)
        self.markup_formula_entry.grid(row=2, column=2, sticky='ew', pady=10, padx=10)

        self.gross_profit_formula_entry.grid(row=3, column=2, sticky='ew', pady=10, padx=10)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=2)

    def on_invalid(self, _):
        self.bell()

    def update_display(self, _):
        if contains_digit(self.unit_price_var.get()) and contains_digit(self.basis_value_var.get()):
            decimals = int(self.decimals_var.get()) if self.decimals_var.get() != 'Auto' else 6
            multiplier = float(self.unit_price_var.get()) / float(self.basis_value_var.get())
            self.multiplier_var.set(f'*{round(multiplier, decimals)}')
            self.discount_var.set(f'{round((multiplier - 1) * 100, decimals):-}')
            if multiplier:
                self.markup_var.set(f'D{round(1 / multiplier, decimals)}')
                numeric_part = (1.1 - 1 / multiplier) * 100
                if numeric_part < 100:
                    self.gross_profit_var.set(f'GP{round((1.0 - 1 / multiplier) * 100.0, decimals)}')
                else:
                    self.gross_profit_var.set('')
            else:
                self.gross_profit_var.set('')
        else:
            self.multiplier_var.set('')
            self.discount_var.set('')
            self.markup_var.set('')
            self.gross_profit_var.set('')


class UnitFormulaFrame(ttk.Frame):
    """Ttk Frame with a predefined set of widgets

        See class definition for a layout of the widgets
    """
    """
    +-----------------------------------------------+
    |           +----------------++----------------+|
    |Unit Price |                ||                ||
    |           +----------------++----------------+|
    |           +----------------++----------------+| 
    |Formula    |                ||                ||
    |           +----------------++----------------+|
    |           +----------------++----------------+|
    |Basis Value|                ||                ||
    |           +----------------++----------------+|
    |                             +----------------+|
    |                             |                ||
    |                             +----------------+|
    +-----------------------------------------------+
    """

    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.master = master

        # create text variables
        self.unit_price_var = tk.StringVar()
        self.formula_var = tk.StringVar()
        self.calculated_basis_var = tk.StringVar()
        self.multiplier_var = tk.StringVar()
        self.discount_var = tk.StringVar()
        self.markup_var = tk.StringVar()
        self.gross_profit_var = tk.StringVar()

        # validation functions
        nvcmd = (self.master.register(validate_number), '%P')
        fvcmd = (self.master.register(validate_formula), '%P')
        ivcmd = (self.master.register(self.on_invalid), '%W')

        # create the widgets
        self.unit_price_label = ttk.Label(self, text='Unit Price', font=('TkDefaultFont', 18))
        self.formula_label = ttk.Label(self, text='Formula', font=('TkDefaultFont', 18))
        self.calculated_basis_label = ttk.Label(self, text='Basis Value', font=('TkDefaultFont', 18))

        self.unit_price_entry = ttk.Entry(
            self, font=('TkDefaultFont', 18),
            textvariable=self.unit_price_var,
            validate='key',
            validatecommand=nvcmd,
            invalidcommand=ivcmd,
        )
        self.unit_price_entry.bind('<KeyRelease>', self.update_display)
        self.formula_entry = ttk.Entry(
            self, font=('TkDefaultFont', 18),
            textvariable=self.formula_var,
            validate='key',
            validatecommand=fvcmd,
            invalidcommand=ivcmd,
        )
        self.formula_entry.bind('<KeyRelease>', self.update_display)
        self.calculated_basis_entry = ttk.Entry(
            self, font=('TkDefaultFont', 18),
            textvariable=self.calculated_basis_var,
            state='readonly',
        )
        self.multiplier_entry = ttk.Entry(
            self,
            font=('TkDefaultFont', 18),
            textvariable=self.multiplier_var,
            state='readonly',
        )
        self.discount_entry = ttk.Entry(
            self,
            font=('TkDefaultFont', 18),
            textvariable=self.discount_var,
            state='readonly',
        )
        self.markup_entry = ttk.Entry(
            self,
            font=('TkDefaultFont', 18),
            textvariable=self.markup_var,
            state='readonly',
        )
        self.gross_profit_entry = ttk.Entry(
            self,
            font=('TkDefaultFont', 18),
            textvariable=self.gross_profit_var,
            state='readonly',
        )

        self.unit_price_label.grid(row=0, column=0, sticky='w', pady=10, padx=10)
        self.unit_price_entry.grid(row=0, column=1, sticky='we', pady=10, padx=10)

        self.formula_label.grid(row=1, column=0, sticky='w', pady=10, padx=10)
        self.formula_entry.grid(row=1, column=1, sticky='we', pady=10, padx=10)

        self.calculated_basis_label.grid(row=2, column=0, sticky='w', pady=10, padx=10)
        self.calculated_basis_entry.grid(row=2, column=1, sticky='we', pady=10, padx=10)

        self.multiplier_entry.grid(row=0, column=2, sticky='ew', pady=10, padx=10)
        self.discount_entry.grid(row=1, column=2, sticky='ew', pady=10, padx=10)
        self.markup_entry.grid(row=2, column=2, sticky='ew', pady=10, padx=10)
        self.gross_profit_entry.grid(row=3, column=2, sticky='ew', pady=10, padx=10)

    def update_display(self, _):
        unit_price = self.unit_price_var.get()
        formula = self.formula_var.get()
        if valid_formula(formula):
            multiplier = find_multiplier(formula)
            self.multiplier_var.set(f'*{round(multiplier, 6)}')
            self.discount_var.set(f'{round((multiplier-1)*100,6):-}')
            if multiplier != 0:
                self.markup_var.set(f'D{round(1/multiplier,6)}')
                self.gross_profit_var.set(f'GP{round((1-1/multiplier)*100, 6)}')
                if contains_digit(unit_price):
                    self.calculated_basis_var.set(round(float(self.unit_price_var.get()) / multiplier, 3))
                    self.multiplier_var.set(f'*{multiplier}')
                else:
                    self.calculated_basis_var.set('')
            else:
                self.markup_var.set('')
                self.gross_profit_var.set('')
        else:
            self.calculated_basis_var.set('')

    def on_invalid(self, _):
        self.bell()


class View(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        s = ttk.Style()
        s.configure('TNotebook.Tab', font=('TkDefaultFont', '18', 'bold'))

        # create the container to hold the frames
        self.tabs = ttk.Notebook(self)
        self.tabs.pack(pady=10, expand=True)

        self.unit_basis_frame = UnitBasisFrame(self)
        self.unit_formula_frame = UnitFormulaFrame(self)

        self.unit_basis_frame.pack(fill='both', expand=True)
        self.unit_formula_frame.pack(fill='both', expand=True)

        self.tabs.add(self.unit_basis_frame, text='Unit Price/Basis Value')
        self.tabs.add(self.unit_formula_frame, text='Unit Price/Formula')

        self.pack()


if __name__ == "__main__":
    app = tk.Tk()
    app.title('Special Calculator')
    app.resizable(False, False)
    view = View(master=app)

    app.mainloop()
