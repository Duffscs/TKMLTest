from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET

class ScrollbarWidget(IWidget):
    name = 'scrollbar'

    def create(self, element : ET.Element, parent : tk.Tk | tk.Toplevel | tk.Frame):
        orient = element.attrib.get('orient', 'vertical')
        target = element.attrib.get('target', None)
        targetWidget = self.getComponent(target)
        widget = tk.Scrollbar(parent, orient=orient)
        if orient == 'horizontal' and targetWidget:
            widget.config(xscrollcommand=targetWidget.xview)
            targetWidget.config(xscrollcommand=widget.set)
        elif orient == 'vertical' and targetWidget:
            widget.config(yscrollcommand=targetWidget.yview)
            targetWidget.config(yscrollcommand=widget.set)
        return widget