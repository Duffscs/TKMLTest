from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET

class RadiobuttonWidget(IWidget):
    name = 'radiobutton'

    def create(self, element : ET.Element, parent : tk.Tk):
        text = self.pageAssembler.resolve_template(element.get('text', ''))
        group = element.get('group', 'default')
        var = self.pageAssembler.get_or_create_variable(group, tk.IntVar, '')
        value = int(element.get('value', 0))
        return tk.Radiobutton(parent, text=text, variable=var, value=value)