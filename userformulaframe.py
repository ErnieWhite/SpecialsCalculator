import tkinter as tk
from utilities import *


class UnitFormulaFrame(tk.Frame):
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
        self.formula_var = tk.StringVar()
        self.calculated_basis_var = tk.StringVar()
        self.unit_price_var = tk.StringVar()
        self.nvcmd = (self.master.register(is_float_or_empty), '%P')
        self.fvcmd = (self.master.register(validate_formula), '%P')
        self.ivcmd = (self.master.register(self.on_invalid), '%W')

        # create the widgets
        self.unit_price_label = tk.Label(self)
        self.formula_label = tk.Label(self)
        self.calculated_basis_label = tk.Label(self)

        self.unit_price_entry = tk.Entry(self)
        self.formula_entry = tk.Entry(self)
        self.calculated_basis_entry = tk.Entry(self)

        self.setup_widgets()
        self.place_widgets()

    def setup_widgets(self):
        # create the widgets
        self.unit_price_label.config(text='Unit Price')
        self.formula_label.config(text='Formula')
        self.calculated_basis_label.config(text='Basis Value')
        self.unit_price_entry.config(
            textvariable=self.unit_price_var,
            validate='key',
            validatecommand=self.nvcmd,
            invalidcommand=self.ivcmd,
        )
        self.unit_price_entry.bind('<KeyRelease>', self.update_display)
        self.formula_entry.config(
            textvariable=self.formula_var,
            validate='key',
            validatecommand=self.fvcmd,
            invalidcommand=self.ivcmd,
        )
        self.formula_entry.bind('<KeyRelease>', self.update_display)
        self.calculated_basis_entry.config(
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
            if multiplier > 0:
                if is_float(unit_price):
                    self.calculated_basis_var.set(round(float(self.unit_price_var.get()) / multiplier, 3))
                else:
                    self.calculated_basis_var.set('')
        else:
            self.calculated_basis_var.set('')

    def on_invalid(self, _):
        self.bell()
