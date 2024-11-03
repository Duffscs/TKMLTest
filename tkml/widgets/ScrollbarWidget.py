from tkml.widgets.IWidget import IWidget
import tkinter as tk
import xml.etree.ElementTree as ET

class ScrollbarWidget(IWidget):
    name = 'scrollbar'

    def create(self, element : ET.Element, parent : tk.Tk):
        if element.get('padx', None) is not None:
            element.set('padx', 0)
        if element.get('pady', None) is not None:
            element.set('pady', 0)
        orient = element.get('orient', 'vertical')
        target = element.get('target', None)
        targetWidget = self.pageAssembler.getComponent(target)
        widget = tk.Scrollbar(parent, orient=orient)
        if orient == 'horizontal' and targetWidget:
            widget.config(command=targetWidget.xview)
            targetWidget.config(xscrollcommand=widget.set)
        elif orient == 'vertical' and targetWidget:
            widget.config(command=targetWidget.yview)
            targetWidget.config(yscrollcommand=widget.set)
        return widget