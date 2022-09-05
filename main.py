import tkinter as tk
from view import View


if __name__ == "__main__":
    app = tk.Tk()
    app.title('Special Calculator')
    app.resizable(False, False)
    view = View(master=app)

    app.mainloop()
