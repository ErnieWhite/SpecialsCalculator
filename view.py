import tkinter as tk
from tkinter import ttk
from unitbasisframe import UnitBasisFrame
from userformulaframe import UnitFormulaFrame


class View(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        s = ttk.Style()
        s.configure(
            'TNotebook.Tab',
            # font=('TkDefaultFont', '18', 'bold'),
        )

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
