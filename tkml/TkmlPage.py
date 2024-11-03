import tkinter as tk
from tkinter import ttk
import xml.etree.ElementTree as ET
from tkml.TkmlPageAssembler import TkmlPageAssembler

class TkmlPage:
    def __init__(self, root=None, parent=None):
        self.widgets = {}
        self.named_widgets = {} 
        self.parent = parent
        if parent:
            root = tk.Toplevel(parent)
            root.transient(parent)
            root.grab_set()
        self.root = root or tk.Tk()

    def on_window_ready(self):
        pass

    def get_tkml(self):
        raise NotImplementedError("La méthode get_tkml doit être implémentée dans la classe dérivée.")

    def show(self):
        TkmlPageAssembler(self).assemble(self.get_tkml())
        self.root.mainloop()

    def close(self):
        self.root.destroy()
        self.root.quit()
        