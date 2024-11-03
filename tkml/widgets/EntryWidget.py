from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET

class EntryWidget(IWidget):
    name = 'entry'

    def create(self, element : ET.Element, parent : tk.Tk):
        entry_var = self.pageAssembler.handle_bindable_attribute_variable(element, parent, 'value', tk.StringVar, '')
        return tk.Entry(parent, textvariable=entry_var)