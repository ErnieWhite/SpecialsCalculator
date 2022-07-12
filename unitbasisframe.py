import tkinter as tk
from tkinter import ttk
from utilities import *


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
        self.vcmd = (self.master.register(is_float_or_empty), '%P')
        self.ivcmd = (self.master.register(self.on_invalid), '%W')

        # text variables
        self.unit_price_var = tk.StringVar()
        self.basis_value_var = tk.StringVar()
        self.multiplier_var = tk.StringVar()
        self.discount_var = tk.StringVar()
        self.markup_var = tk.StringVar()
        self.gross_profit_var = tk.StringVar()
        self.decimals_var = tk.StringVar()

        # create the widgets
        self.unit_price_label = ttk.Label(self)
        self.basis_value_label = ttk.Label(self)
        self.decimals_label = ttk.Label(self)
        self.unit_price_entry = ttk.Entry(self)
        self.basis_value_entry = ttk.Entry(self)
        self.decimals_combo = ttk.Combobox(self)
        self.multiplier_formula_entry = ttk.Entry(self)
        self.discount_formula_entry = ttk.Entry(self)
        self.markup_formula_entry = ttk.Entry(self)
        self.gross_profit_formula_entry = ttk.Entry(self)
        self.button_copy_multiplier = tk.Button(self)
        self.button_copy_discount = tk.Button(self)
        self.button_copy_markup = tk.Button(self)
        self.button_copy_gross_profit = tk.Button(self)
        self.configure_widgets()
        self.place_widgets()

    def configure_widgets(self):
        self.unit_price_label.config(text='Unit Price')
        self.basis_value_label.config(text='Basis Value')
        self.decimals_label.config(text='Decimal Places')
        self.unit_price_entry.config(
            textvariable=self.unit_price_var,
            validate='key',
            # font=('TkDefaultFont', 18),
            validatecommand=self.vcmd,
            invalidcommand=self.ivcmd,
        )
        self.unit_price_entry.bind('<KeyRelease>', self.update_display)
        self.basis_value_entry.config(
            # font=('TkDefaultFont', 18),
            textvariable=self.basis_value_var,
            validate='key',
            validatecommand=self.vcmd,
            invalidcommand=self.ivcmd,
        )
        self.basis_value_entry.bind('<KeyRelease>', self.update_display)
        self.decimals_combo.config(
            # font=('TkDefaultFont', 18),
            values=('Auto', '0', '1', '2', '3', '4', '5', '6'),
            state='readonly',
            textvariable=self.decimals_var,
        )
        self.decimals_combo.bind(
            '<<ComboboxSelected>>',
            self.update_display
        )
        self.decimals_combo.set('Auto')

        self.multiplier_formula_entry.config(
            # font=('TkDefaultFont', 18),
            textvariable=self.multiplier_var,
            state='readonly',
        )
        self.discount_formula_entry.config(
            # font=('TkDefaultFont', 18),
            textvariable=self.discount_var,
            state='readonly',
        )
        self.markup_formula_entry.config(
            # font=('TkDefaultFont', 18),
            textvariable=self.markup_var,
            state='readonly',
        )
        self.gross_profit_formula_entry.config(
            # font=('TkDefaultFont', 18),
            textvariable=self.gross_profit_var,
            state='readonly',
        )
        self.button_copy_multiplier.config(
            text="Copy",
            command=self.copy_multiplier_formula_entry
        )
        self.button_copy_discount.config(
            text="Copy",
            command=self.copy_discount_formula_entry
        )
        self.button_copy_markup.config(
            text="Copy",
            command=self.copy_markup_formula_entry
        )
        self.button_copy_gross_profit.config(
            text="Copy",
            command=self.copy_gross_profit_formula_entry
        )

    def place_widgets(self):
        self.unit_price_label.grid(row=0, column=0, sticky='w', pady=10, padx=10)
        self.unit_price_entry.grid(row=0, column=1, sticky='ew', pady=10, padx=10)
        self.multiplier_formula_entry.grid(row=0, column=2, sticky='ew', pady=10, padx=(10, 0))
        self.button_copy_multiplier.grid(row=0, column=3, sticky='w')

        self.basis_value_label.grid(row=1, column=0, sticky='w', pady=10, padx=10)
        self.basis_value_entry.grid(row=1, column=1, sticky='ew', pady=10, padx=10)
        self.discount_formula_entry.grid(row=1, column=2, sticky='ew', pady=10, padx=(10, 0))
        self.button_copy_discount.grid(row=1, column=3, sticky='w')

        self.decimals_label.grid(row=2, column=0, sticky='w', pady=10, padx=10)
        self.decimals_combo.grid(row=2, column=1, sticky='ew', pady=10, padx=10)
        self.markup_formula_entry.grid(row=2, column=2, sticky='ew', pady=10, padx=(10, 0))
        self.button_copy_markup.grid(row=2, column=3, sticky='w')

        self.gross_profit_formula_entry.grid(row=3, column=2, sticky='ew', pady=10, padx=(10, 0))
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=2)
        self.button_copy_gross_profit.grid(row=3, column=3, sticky='w')

    def on_invalid(self, _):
        self.bell()

    def copy_multiplier_formula_entry(self):
        self.clipboard_clear()
        self.clipboard_append(self.multiplier_formula_entry.get())
        self.update()

    def copy_discount_formula_entry(self):
        self.clipboard_clear()
        self.clipboard_append(self.discount_formula_entry.get())
        self.update()

    def copy_markup_formula_entry(self):
        self.clipboard_clear()
        self.clipboard_append(self.markup_formula_entry.get())
        self.update()

    def copy_gross_profit_formula_entry(self):
        self.clipboard_clear()
        self.clipboard_append(self.gross_profit_formula_entry.get())
        self.update()

    def update_display(self, _):
        if is_float(self.unit_price_var.get()) and is_float(self.basis_value_var.get()):
            decimals = int(self.decimals_var.get()) if self.decimals_var.get() != 'Auto' else 6
            multiplier = float(self.unit_price_var.get()) / float(self.basis_value_var.get())
            self.multiplier_var.set(f'*{round(multiplier, decimals)}')
            self.discount_var.set(f'{round((multiplier - 1) * 100, decimals):-}')
            if multiplier:
                self.markup_var.set(f'D{round(1 / multiplier, decimals)}')
                numeric_part = (1.1 - 1 / multiplier) * 100
                if numeric_part < 100:
                    self.gross_profit_var.set(f'GP{(1.0 - 1 / multiplier) * 100.0}')
                else:
                    self.gross_profit_var.set('')
            else:
                self.gross_profit_var.set('')
        else:
            self.multiplier_var.set('')
            self.discount_var.set('')
            self.markup_var.set('')
            self.gross_profit_var.set('')
