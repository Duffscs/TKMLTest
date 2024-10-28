from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET

class ButtonWidget(IWidget):
    name = 'button'

    def create(self, element : ET.Element, parent : tk.Tk | tk.Toplevel | tk.Frame):
        text = self.pageAssembler.resolve_template(element.attrib.get('text', ''))
        command_name = element.attrib.get('command', None)
        command = getattr(self.pageAssembler.tkml_page, command_name, None) if command_name else None
        return tk.Button(parent, text=text, command=command)