from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET

class TextWidget(IWidget):
    name = 'text'

    def create(self, element : ET.Element, parent : tk.Tk | tk.Toplevel | tk.Frame, text : str):
        return tk.Label(parent, text=text)