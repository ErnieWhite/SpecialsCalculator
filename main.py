import tkinter as tk
from tkinter import ttk
import re
import sys


def validate_number(value: str) -> bool:
    """Returns a boolean indicating if value is in the form [-|+]{0..9}[.]{0..9}"""
    if re.fullmatch(r"^[-,+]?\d*\.?\d*$", value) is None:
        return False
    else:
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


def find_multiplier(formula: str) -> float:
    """Converts a string formula to a float multiplier"""



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
        ┌───────────────────────────────────────────────┐
        │           ┌────────────────┐┌────────────────┐│
        │Unit Price │                ││                ││
        │           └────────────────┘└────────────────┘│
        │           ┌────────────────┐┌────────────────┐│
        │Basis Value│                ││                ││
        │           └────────────────┘└────────────────┘│
        │           ┌────────────────┐┌────────────────┐│
        │Decimals   │Auto           v││                ││
        │           └────────────────┘└────────────────┘│
        │                             ┌────────────────┐│
        │                             │                ││
        │                             └────────────────┘│
        └───────────────────────────────────────────────┘
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

        # create the widgets
        self.unit_price_label = ttk.Label(self, text='Unit Price')
        self.basis_value_label = ttk.Label(self, text='Basis Value')
        self.decimals_label = ttk.Label(self, text='Decimals')

        self.unit_price_entry = ttk.Entry(
            self,
            textvariable=self.unit_price_var,
            validate='key',
            validatecommand=vcmd,
            invalidcommand=ivcmd,
        )
        self.unit_price_entry.bind('<KeyRelease>', self.update_display)
        self.basis_value_entry = ttk.Entry(
            self,
            textvariable=self.basis_value_var,
            validate='key',
            validatecommand=vcmd,
            invalidcommand=ivcmd,
        )
        self.basis_value_entry.bind('<KeyRelease>', self.update_display)
        self.decimals_combo = ttk.Combobox(
            self,
            values=('Auto', '1', '2', '3', '4', '5', '6'),
        )
        self.decimals_combo.set('Auto')

        self.multiplier_formula_entry = ttk.Entry(
            self,
            textvariable=self.multiplier_var,
            state='readonly',
        )
        self.discount_formula_entry = ttk.Entry(
            self,
            textvariable=self.discount_var,
            state='readonly',
        )
        self.markup_formula_entry = ttk.Entry(
            self,
            textvariable=self.markup_var,
            state='readonly',
        )
        self.gross_profit_formula_entry = ttk.Entry(
            self,
            textvariable=self.gross_profit_var,
            state='readonly',
        )

        self.unit_price_label.grid(row=0, column=0, sticky='w')
        self.unit_price_entry.grid(row=0, column=1, sticky='ew')
        self.multiplier_formula_entry.grid(row=0, column=2, sticky='ew')

        self.basis_value_label.grid(row=1, column=0, sticky='w')
        self.basis_value_entry.grid(row=1, column=1, sticky='ew')
        self.discount_formula_entry.grid(row=1, column=2, sticky='ew')

        self.decimals_label.grid(row=2, column=0, sticky='w')
        self.decimals_combo.grid(row=2, column=1, sticky='ew')
        self.markup_formula_entry.grid(row=2, column=2, sticky='ew')

        self.gross_profit_formula_entry.grid(row=3, column=2, sticky='ew')
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=2)

    def on_invalid(self):
        self.bell()

    def update_display(self, _):
        if self.unit_price_var.get() and self.basis_value_var.get():
            print('hello')
            multiplier = float(self.unit_price_var.get()) / float(self.basis_value_var.get())
            self.multiplier_var.set(f'*{multiplier}')
            self.discount_var.set(f'{(multiplier - 1) * 100:-}')
            if multiplier:
                self.markup_var.set(f'D{1 / multiplier}')
            if multiplier:
                numeric_part = (1 - 1 / multiplier) * 100
                if 0 <= numeric_part < 100:
                    self.gross_profit_var.set(f'GP{(1 - 1 / multiplier) * 100}')
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
    ┌───────────────────────────────────────────────┐
    │           ┌────────────────┐                  │
    │Unit Price │                │                  │
    │           └────────────────┘                  │
    │           ┌────────────────┐                  │ 
    │Formula    │                │                  │
    │           └────────────────┘                  │
    │           ┌────────────────┐                  │
    │Basis Value│                │                  │
    │           └────────────────┘                  │
    │                                               │
    │                                               │
    │                                               │
    └───────────────────────────────────────────────┘
    """

    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.master = master

        # create text variables
        self.unit_price_var = tk.StringVar()
        self.formula_var = tk.StringVar()
        self.calculated_basis_var = tk.StringVar()

        # validation functions
        nvcmd = (self.master.register(validate_number), '%P')
        fvcmd = (self.master.register(validate_formula), '%P')
        ivcmd = (self.master.register(self.on_invalid), '%W')

        # create the widgets
        self.unit_price_label = ttk.Label(self, text='Unit Price')
        self.formula_label = ttk.Label(self, text='Formula')
        self.calculated_basis_label = ttk.Label(self, text='Basis Value')

        self.unit_price_entry = ttk.Entry(
            self,
            validate='key',
            validatecommand=nvcmd,
            invalidcommand=ivcmd,
        )
        self.unit_price_entry.bind('<KeyRelease>', self.update_display)
        self.formula_entry = ttk.Entry(
            self,
            validate='key',
            validatecommand=fvcmd,
            invalidcommand=ivcmd,
        )
        self.formula_entry.bind('<KeyRelease>', self.update_display)
        self.calculated_basis_entry = ttk.Entry(
            self,
            state='readonly',
        )

        self.unit_price_label.grid(row=0, column=0, sticky='w')
        self.unit_price_entry.grid(row=0, column=1, sticky='we')

        self.formula_label.grid(row=1, column=0, sticky='w')
        self.formula_entry.grid(row=1, column=1, sticky='we')

        self.calculated_basis_label.grid(row=2, column=0, sticky='w')
        self.calculated_basis_entry.grid(row=2, column=1, sticky='we')

    def update_display(self):
        unit_price = self.unit_price_var.get()
        formula = self.formula_var.get()
        if validate_number(unit_price) and validate_formula(formula):
            multiplier = find_multiplier(formula)
        else:
            self.calculated_basis_var.set('')

    def on_invalid(self):
        self.bell()


class View(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

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
