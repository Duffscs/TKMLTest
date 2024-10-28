from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET

class LabelWidget(IWidget):
    name = 'label'

    def create(self, element : ET.Element, parent : tk.Tk | tk.Toplevel | tk.Frame):
        text = self.pageAssembler.resolve_template(element.attrib.get('text', ''))
        return tk.Label(parent, text=text)