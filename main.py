import tkinter as tk
from tkinter import ttk
import re


class Controller:
    def __init__(self, master, model, view):
        self.model = model
        self.view = view
        self.master = master

        self.init_unit_base_frame()
        self.init_unit_formula_frame()
        self.add_unit_base_event_handlers()
        self.add_unit_formula_event_handlers()

    def init_unit_base_frame(self):
        float_vcmd = (self.master.register(self.validate_number), '%P')
        ivcmd = (self.master.register(self.on_invalid),)
        self.view.unit_basis_frame.unit_price_entry.configure(
            validate='key',
            validatecommand=float_vcmd,
            invalidcommand=ivcmd,
            textvariable=self.model.ub_unit_price_var,
        )
        self.view.unit_basis_frame.basis_value_entry.configure(
            validate='key',
            validatecommand=float_vcmd,
            invalidcommand=ivcmd,
            textvariable=self.model.ub_basis_value_var,
        )

    def init_unit_formula_frame(self):
        formula_vcmd = (self.master.register(self.validate_formula), '%P')
        float_vcmd = (self.master.register(self.validate_number), '%P')
        ivcmd = (self.master.register(self.on_invalid),)
        self.view.unit_formula_frame.unit_price_entry.configure(
            validate='key',
            validatecommand=float_vcmd,
            invalidcommand=ivcmd,
            textvariable=self.model.uf_formula_var,
        )
        self.view.unit_formula_frame.formula_entry.configure(
            validate='key',
            validatecommand=formula_vcmd,
            invalidcommand=ivcmd,
            textvariable=self.model.uf_unit_price_var,
        )
        self.view.unit_basis_frame.multiplier_formula_entry.configure(
            textvariable=self.model.ub_multilier_formula_var,
        )
        self.view.unit_basis_frame.discount_formula_entry.configure(
            textvariable=self.model.ub_discount_formula_var,
        )
        self.view.unit_basis_frame.markup_formula_entry.configure(
            textvariable=self.model.ub_markup_formula_var,
        )
        self.view.unit_basis_frame.gross_profit_formula_entry.configure(
            textvariable=self.model.ub_gross_profit_formula_var,
        )

    @staticmethod
    def validate_number(value):
        if re.fullmatch(r"^\$?\d*\.?\d*$", value) is None:
            return False
        else:
            return True

    @staticmethod
    def validate_formula(value):
        if re.fullmatch(r'^(\*|X|-|\+|D|GP)\d*\.?\d*$', value, flags=re.IGNORECASE) is not None or value == '':
            return True
        else:
            return False

    def on_invalid(self):
        print('invalid')
        self.master.bell()
        self.master.bell()

    def add_unit_base_event_handlers(self):
        self.view.unit_basis_frame.unit_price_entry.bind('<KeyRelease>', self.calculate_formulas)
        self.view.unit_basis_frame.basis_value_entry.bind('KeyRelease>', self.calculate_formulas)

    def add_unit_formula_event_handlers(self):
        pass

    def calculate_formulas(self):
        if self.model.ub_unit_price_var is not None and self.model.ub_basis_value_var is not None:
            multiplier = self.model.ub_unit_price_var / self.model.ub_basis_value_var


class UnitBasisFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.master = master

        # validation functions
        vcmd = (self.master.register(self.validate), '%P')
        ivcmd = (self.master.register(self.on_invalid),)

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

    @staticmethod
    def validate(value):
        if re.fullmatch(r"^\d*\.?\d*$", value) is None:
            return False
        else:
            return True

    def on_invalid(self):
        self.master.bell()
        self.master.bell()

    def update_display(self, e):

        print(self.unit_price_var.get())
        if self.unit_price_var.get() and self.basis_value_var.get():
            print('hello')
            multiplier = float(self.unit_price_var.get()) / float(self.basis_value_var.get())
            self.multiplier_var.set(f'*{multiplier}')
            self.discount_var.set(f'{(1-multiplier)*100:-}')
            self.markup_var.set(f'{1/multiplier}')
            self.gross_profit_var.set(f'#####')


class UnitFormulaFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master=master, **kwargs)

        self.master = master

        # validation functions
        nvcmd = (self.master.register(self.validate_number), '%P')
        fvcmd = (self.master.register(self.validate_formula), '%P')
        ivcmd = (self.master.register(self.on_invalid),)

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
        self.formula_entry = ttk.Entry(
            self,
            validate='key',
            validatecommand=fvcmd,
            invalidcommand=ivcmd,
        )
        self.calculated_basis_entry = ttk.Entry(self)

        self.unit_price_label.grid(row=0, column=0, sticky='w')
        self.unit_price_entry.grid(row=0, column=1, sticky='we')

        self.formula_label.grid(row=1, column=0, sticky='w')
        self.formula_entry.grid(row=1, column=1, sticky='we')

        self.calculated_basis_label.grid(row=2, column=0, sticky='w')
        self.calculated_basis_entry.grid(row=2, column=1, sticky='we')

    def validate_number(self, value):
        if re.fullmatch(r"^\$?\d*\.?\d*$", value) is None:
            return False
        else:
            return True

    def validate_formula(self, value):
        print(re.fullmatch(r'^(\*|X|-|\+|D|(?<G).*G)\d*\.?\d*$', value, flags=re.IGNORECASE))
        if re.fullmatch(r'^(\*|X|-|\+|D|GP)\d*\.?\d*$', value, flags=re.IGNORECASE) is not None or value == '':
            return True
        else:
            return False

    def on_invalid(self):
        print('invalid')
        self.master.bell()
        self.master.bell()


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
