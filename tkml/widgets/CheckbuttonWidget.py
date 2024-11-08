from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET

class CheckbuttonWidget(IWidget):
    name = 'checkbutton'
    
    def create(self, element : ET.Element, parent : tk.Tk):
        text = self.pageAssembler.resolve_template(element.get('text', ''))
        bool_var = self.pageAssembler.handle_bindable_attribute_variable(element, parent, 'value', tk.BooleanVar, False)
        return tk.Checkbutton(parent, text=text, variable=bool_var)