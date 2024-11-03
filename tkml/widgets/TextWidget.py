from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET

class TextWidget(IWidget):
    name = 'text'

    def create(self, element : ET.Element, parent : tk.Tk):
        text = self.pageAssembler.resolve_template(element.get('text', ''))
        return tk.Label(parent, text=text)