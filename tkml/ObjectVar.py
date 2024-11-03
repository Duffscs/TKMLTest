import tkinter as tk
from typing import List

class ObjectVar(tk.Variable):

    def __init__(self, master=None, value=None, name=None):
        self.innerData = value
        super().__init__(master, value=value, name=name)

    def set(self, value):
        self.innerData = value
        super().set(value)

    def get(self):
        return self.innerData
